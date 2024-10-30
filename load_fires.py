import pandas as pd
import psycopg
from psycopg import sql
from datetime import datetime

def delete_all_data(conn):
    tables = [
        'fireincidentmeans', 'vehicle', 'firefighter', 'fireincidents',
        'firestation', 'fireweatherconditions', 'location_info', 'parishes',
        'municipality', 'sourcealert', 'burntarea', 'datetime', 'district',
        'firecauses'
    ]
    
    with conn.cursor() as cur:
        for table in tables:
            cur.execute(sql.SQL("DELETE FROM {}").format(sql.Identifier(table)))
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
                if row_count >= 30:
                    break

                try:
                    # Insert into District table
                    cur.execute("SELECT id FROM District WHERE districtname = %s", (row['Distrito'],))
                    result = cur.fetchone()
                    district_id = result[0] if result else cur.execute("""
                        INSERT INTO District (districtname)
                        VALUES (%s) RETURNING id
                    """, (row['Distrito'],)).fetchone()[0]

                    # Insert into Municipality table
                    cur.execute("SELECT id FROM Municipality WHERE MunicipalityName = %s", (row['Concelho'],))
                    result = cur.fetchone()
                    municipality_id = result[0] if result else cur.execute("""
                        INSERT INTO Municipality (MunicipalityName, district_id)
                        VALUES (%s, %s) RETURNING id
                    """, (row['Concelho'], district_id)).fetchone()[0]

                    # Insert into Parishes table
                    cur.execute("SELECT id FROM Parishes WHERE parishname = %s", (row['Freguesia'],))
                    result = cur.fetchone()
                    parish_id = result[0] if result else cur.execute("""
                        INSERT INTO Parishes (parishname, municipality_id)
                        VALUES (%s, %s) RETURNING id
                    """, (row['Freguesia'], municipality_id)).fetchone()[0]

                    # Insert into DateTime table
                    try:
                        # Check the data types and content for debugging
                        print(f"Inserting row: {row.to_dict()}")
                        print(f"DataHoraAlerta type: {type(row['DataHoraAlerta'])}, value: {row['DataHoraAlerta']}")

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
                            float(row['Duracao_Horas'].replace(',', '.')),
                            bool(row['IncSup24horas'])
                        ))
                        datetime_id = cur.fetchone()[0]
                        print("Inserted DateTime ID:", datetime_id)

                    except Exception as e:
                        print(f"Error inserting DateTime row: {row.to_dict()}")
                        print(e)
                        conn.rollback()
                        continue

                    # Convert CodCausa to integer if not NULL
                    cod_causa = row['CodCausa']
                    cause_code = int(cod_causa) if cod_causa else None

                    if cause_code is not None:
                        cur.execute("SELECT CauseCode FROM FireCauses WHERE CauseCode = %s", (cause_code,))
                        result = cur.fetchone()

                        if result is None:
                            print("Inserting new fire cause:", cod_causa)
                            cur.execute("""
                                INSERT INTO FireCauses (CauseCode, CauseType, CauseGroup, CauseDescription)
                                VALUES (%s, %s, %s, %s)
                                RETURNING CauseCode
                            """, (cause_code, row['TipoCausa'], row['GrupoCausa'], row['DescricaoCausa']))
                            cause_code = cur.fetchone()[0]
                        else:
                            cause_code = result[0]
                    else:
                        cause_code = None
                        
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

# Example usage
# conn = psycopg.connect("dbname=your_db user=your_user password=your_password")
# delete_all_data(conn)
# insert_data(conn, "path_to_your_csv_file.csv")
# conn.close()
