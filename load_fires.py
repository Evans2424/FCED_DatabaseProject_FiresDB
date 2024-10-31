import csv
import psycopg
from psycopg import sql
from datetime import datetime
import math
import pandas as pd

def delete_all_data(conn):
    tables = [
        'firefighter', 'vehicle_fireincident',
        'firestation', 'firefighter_fireincident', 'vehicle','fireincidents','fireweatherconditions', 'location_info', 'parishes',
        'municipality', 'sourcealert', 'burntarea', 'datetime', 'district',
        'firecauses'
    ]
    
    with conn.cursor() as cur:
        for table in tables:
            cur.execute(sql.SQL("DELETE FROM {}").format(sql.Identifier(table)))
            if (table != 'firefighter_fireincident' and table != 'vehicle_fireincident' and table != 'firecauses'):
                print("LLGLGL")
                cur.execute(sql.SQL("ALTER SEQUENCE {} RESTART WITH 1").format(sql.Identifier(f"{table}_id_seq")))
        conn.commit()
    print("All data deleted from the database.")

def insert_data(conn, csv_file):
    try:
        # Load CSV data, parse datetime columns
        data = pd.read_csv(csv_file, delimiter=';', parse_dates=['DataHoraAlerta', 'DataHora_PrimeiraIntervencao', 'DataHora_Extincao'], dayfirst=True)
        
        row_count = 0
        print("Inserting data into the database...")

        with conn.cursor() as cur:
            for _, row in data.iterrows():
               
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
                        break

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
                        break

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
                        break

                    # Check if Duracao_Horas is not NULL
                    duracao_horas = row['Duracao_Horas']
                    duracao_horas_value = float(duracao_horas.replace(',', '.')) if duracao_horas else None

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
                        print("Inserted DateTime ID:", datetime_id)
                    except Exception as e:
                        print(f"Error inserting DateTime row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        break

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
                            break
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
                        break

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
                        print("Inserted BurntArea ID:", burnt_area_id)
                    except Exception as e:
                        print(f"Error inserting BurntArea row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        break

                    # Insert into FireWeatherConditions table
                    try:
                        cur.execute("""
                            INSERT INTO FireWeatherConditions (DSR, FWI, ISI, DC, DMC, FFMC, BUI)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            RETURNING id
                        """, (
                            float(row['DSR'].replace(',', '.')),
                            float(row['FWI'].replace(',', '.')),
                            float(row['ISI'].replace(',', '.')),
                            float(row['DC'].replace(',', '.')),
                            float(row['DMC'].replace(',', '.')),
                            float(row['FFMC'].replace(',', '.')),
                            float(row['BUI'].replace(',', '.'))
                        ))
                        fire_weather_conditions_id = cur.fetchone()[0]
                        print("Inserted FireWeatherConditions ID:", fire_weather_conditions_id)
                    except Exception as e:
                        print(f"Error inserting FireWeatherConditions row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        break

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
                        print("Inserted Location_Info ID:", location_info_id)
                    except Exception as e:
                        print(f"Error inserting Location_Info row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        break

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
                        print("Inserted FireIncident ID:", fire_incident_id)
                    except Exception as e:
                        print(f"Error inserting FireIncidents row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        break

                    row_count += 1
                    print(f'Row count: {row_count}')

                except Exception as e:
                    print(f"Error inserting row: {row.to_dict()}")
                    print(e)
                    conn.rollback()
                    continue

            conn.commit()
        print("Data inserted into the database.")
    except Exception as e:
        print("Error reading CSV file or inserting data into the database.")
        print(e)

