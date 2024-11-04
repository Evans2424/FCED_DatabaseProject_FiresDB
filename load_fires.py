import csv
import psycopg
from psycopg import sql
from datetime import datetime
import math
import pandas as pd
from tqdm import tqdm


def convert_to_float(value):
    """Convert a string with comma to float if possible; return None if not."""
    try:
        return float(value.replace(',', '.'))
    except (ValueError, AttributeError):
        return None

def delete_all_data(conn):
    tables = [
        'sourcealert', 'burntarea', 'firefighter_fireincident','vehicle_fireincident',
        'firefighter', 'firestation', 'vehicle','fireincidents','fireweatherconditions', 
        'location_info', 'parishes', 'municipality', 'datetime', 'district', 'firecauses'
    ]
    
    print("Deleting all data from the database...")
    try:
        with conn.cursor() as cur:
            for table in tables:
                print(f"Deleting data from table: {table}")
                
                # Attempt to delete all data from the table
                try:
                    cur.execute(sql.SQL("DELETE FROM {}").format(sql.Identifier(table)))
                except Exception as e:
                    print(f"Error deleting data from table {table}: {e}")
                    continue
                
                # Attempt to reset sequence, if it exists
                try:
                    cur.execute(sql.SQL("ALTER SEQUENCE {} RESTART WITH 1").format(sql.Identifier(f"{table}_id_seq")))
                except Exception as e:
                    print(f"Error resetting sequence for table {table}: {e}")
                    continue
                
            conn.commit()
            
    except Exception as e:
        print("Unexpected error during deletion.")
        print(e)

    print("All data deleted from the database.")

def insert_mock_data(conn):
    with open('SQL_Scripts/insert.sql', 'r') as file:
        sql_script = file.read()

    with conn.cursor() as cur:
        cur.execute(sql_script)
        conn.commit()

    print(f"Executed SQL mock data insertion script")



def insert_data(conn, csv_file):
    try:
        # Load CSV data, parse datetime columns
        data = pd.read_csv(csv_file, delimiter=';', parse_dates=['DataHoraAlerta', 'DataHora_PrimeiraIntervencao', 'DataHora_Extincao'], dayfirst=True)
        num_rows = len(data)

        row_count = 0
        print("Inserting data into the database...")

        with conn.cursor() as cur:
            for index, row in tqdm(data.iterrows(), total=num_rows, desc="Loading data", unit="row"):

                try:
                    # Insert into District table
                    try:
                        cur.execute("SELECT id FROM District WHERE districtname = %s", (row['Distrito'],))
                        result = cur.fetchone()
                        district_id = result[0] if result else cur.execute("""
                            INSERT INTO District (districtname)
                            VALUES (%s) RETURNING id
                        """, (row['Distrito'],)).fetchone()[0]
                    except Exception as e:
                        print(f"Error inserting District row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        continue

                    # Insert into Municipality table
                    try:
                        cur.execute("SELECT id FROM Municipality WHERE MunicipalityName = %s", (row['Concelho'],))
                        result = cur.fetchone()
                        municipality_id = result[0] if result else cur.execute("""
                            INSERT INTO Municipality (MunicipalityName, district_id)
                            VALUES (%s, %s) RETURNING id
                        """, (row['Concelho'], district_id)).fetchone()[0]
                    except Exception as e:
                        print(f"Error inserting Municipality row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        continue

                    # Insert into Parishes table
                    try:
                        cur.execute("SELECT id FROM Parishes WHERE parishname = %s", (row['Freguesia'],))
                        result = cur.fetchone()
                        parish_id = result[0] if result else cur.execute("""
                            INSERT INTO Parishes (parishname, municipality_id)
                            VALUES (%s, %s) RETURNING id
                        """, (row['Freguesia'], municipality_id)).fetchone()[0]
                    except Exception as e:
                        print(f"Error inserting Parishes row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        continue

                    # Check if Duracao_Horas is not NULL
                    duracao_horas = row['Duracao_Horas']
                    duracao_horas_value = convert_to_float(duracao_horas) if duracao_horas and (converted_duracao := convert_to_float(duracao_horas)) is not None and not math.isnan(converted_duracao) else None

                    # Insert into DateTime table
                    try:
                        cur.execute("""
                            INSERT INTO DateTime (Year, Month, DataHoraAlerta, DataHora_PrimeiraIntervenc, DataHora_Extincao, Duracao_Horas, IncSup24horas)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            RETURNING id
                        """, (
                            int(row['Ano']),
                            int(row['Mes']),
                            row['DataHoraAlerta'] if pd.notna(row['DataHoraAlerta']) else None,
                            row['DataHora_PrimeiraIntervencao'] if pd.notna(row['DataHora_PrimeiraIntervencao']) else None,
                            row['DataHora_Extincao'] if pd.notna(row['DataHora_Extincao']) else None,
                            duracao_horas_value,
                            bool(row['IncSup24horas'])
                        ))
                        datetime_id = cur.fetchone()[0]
                    except Exception as e:
                        print(f"Error inserting DateTime row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        continue

                    # Convert CodCausa to integer if not NULL
                    cod_causa = row['CodCausa']
                    if cod_causa and not math.isnan(float(cod_causa)):
                        cause_code = int(cod_causa)
                        try:
                            cur.execute("SELECT CauseCode FROM FireCauses WHERE CauseCode = %s", (cause_code,))
                            result = cur.fetchone()

                            if result is None:
                                cur.execute("""
                                    INSERT INTO FireCauses (CauseCode, CauseType, CauseGroup, CauseDescription)
                                    VALUES (%s, %s, %s, %s)
                                    RETURNING CauseCode
                                """, (cause_code, row['TipoCausa'], row['GrupoCausa'], row['DescricaoCausa']))
                                cause_code = cur.fetchone()[0]
                            else:
                                cause_code = result[0]
                        except Exception as e:
                            print(f"Error inserting FireCauses row: {row.to_dict()}")
                            print(e)
                            conn.rollback()
                            continue
                    else:
                        cause_code = None

                    # Insert into SourceAlert table
                    try:
                        fonte_alerta = row['FonteAlerta']
                        if isinstance(fonte_alerta, str) and fonte_alerta.lower() != 'nan':
                            cur.execute("SELECT id FROM SourceAlert WHERE description = %s", (row['FonteAlerta'],))
                            result = cur.fetchone()

                            source_alert_id = result[0] if result else cur.execute("""
                                INSERT INTO SourceAlert (description)
                                VALUES (%s) RETURNING id
                            """, (row['FonteAlerta'],)).fetchone()[0]
                        else:
                            source_alert_id = None

                    except Exception as e:
                        print(f"Error inserting SourceAlert row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        continue

                    # Insert into BurntArea table
                    try:
                        cur.execute("""
                            INSERT INTO BurntArea (AreaPov_ha, AreaMato_ha, AreaAgric_ha, AreaTotal_ha, ClasseArea)
                            VALUES (%s, %s, %s, %s, %s)
                            RETURNING id
                        """, (
                            float(row['AreaPov_ha'].replace(',', '.')),
                            float(row['AreaMato_ha'].replace(',', '.')),
                            float(row['AreaAgric_ha'].replace(',', '.')),
                            float(row['AreaTotal_ha'].replace(',', '.')),
                            row['ClasseArea']
                        ))
                        burnt_area_id = cur.fetchone()[0]
                    except Exception as e:
                        print(f"Error inserting BurntArea row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        continue
                               
                    # Check if FireWeatherConditions values are not NULL


                    dsr = row['DSR']
                    dsr_value = convert_to_float(dsr) if dsr and (converted_dsr := convert_to_float(dsr)) is not None and not math.isnan(converted_dsr) else None

                    fwi = row['FWI']
                    fwi_value = convert_to_float(fwi) if fwi and (converted_fwi := convert_to_float(fwi)) is not None and not math.isnan(converted_fwi) else None

                    isi = row['ISI']
                    isi_value = convert_to_float(isi) if isi and (converted_isi := convert_to_float(isi)) is not None and not math.isnan(converted_isi) else None

                    dc = row['DC']
                    dc_value = convert_to_float(dc) if dc and (converted_dc := convert_to_float(dc)) is not None and not math.isnan(converted_dc) else None

                    dmc = row['DMC']
                    dmc_value = convert_to_float(dmc) if dmc and (converted_dmc := convert_to_float(dmc)) is not None and not math.isnan(converted_dmc) else None

                    ffmc = row['FFMC']
                    ffmc_value = convert_to_float(ffmc) if ffmc and (converted_ffmc := convert_to_float(ffmc)) is not None and not math.isnan(converted_ffmc) else None

                    bui = row['BUI']
                    bui_value = convert_to_float(bui) if bui and (converted_bui := convert_to_float(bui)) is not None and not math.isnan(converted_bui) else None
                    try:
                        cur.execute("""
                            INSERT INTO FireWeatherConditions (DSR, FWI, ISI, DC, DMC, FFMC, BUI)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            RETURNING id
                        """, (
                            dsr_value,
                            fwi_value,
                            isi_value,
                            dc_value,
                            dmc_value,
                            ffmc_value,
                            bui_value
                        ))
                        fire_weather_conditions_id = cur.fetchone()[0]
                    except Exception as e:
                        print(f"Error inserting FireWeatherConditions row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        continue

                    # Insert into Location_Info table
                    try:
                        cur.execute("""
                            INSERT INTO Location_Info (Parish_id, Local, RNAP, RNMPF, Latitude, Longitude)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            RETURNING id
                        """, (
                            parish_id,
                            row['Local'],
                            row['RNAP'],
                            row['RNMPF'],
                            float(row['Latitude'].replace(',', '.')),
                            float(row['Longitude'].replace(',', '.'))
                        ))
                        location_info_id = cur.fetchone()[0]
                    except Exception as e:
                        print(f"Error inserting Location_Info row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        continue

                    # Insert into FireIncidents table
                    try:
                        cur.execute("""
                            INSERT INTO FireIncidents (Codigo_SGIF, Codigo_ANEPC, Area_info_id, DateTime_info_id, SourceAlert_id, Location_id, FireCause_id, FireWeatherConditions_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            RETURNING id
                        """, (
                            row['Codigo_SGIF'],
                            row['Codigo_ANEPC'],
                            burnt_area_id,
                            datetime_id,
                            source_alert_id,
                            location_info_id,
                            cause_code,
                            fire_weather_conditions_id
                        ))
                        fire_incident_id = cur.fetchone()[0]
                    except Exception as e:
                        print(f"Error inserting FireIncidents row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        continue

                    row_count += 1
                    

                except Exception as e:
                    print(f"Error inserting row: {row.to_dict()}")
                    print(f'Error is {e}')
                    conn.rollback()
                    break

            conn.commit()
        print("Data inserted into the database.")
    except Exception as e:
        print("Error reading CSV file or inserting data into the database.")
        print(e)

            
