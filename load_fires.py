import csv
import psycopg
from psycopg import sql
import datetime

def delete_all_data(conn):
    """Delete all data from all tables in the database."""
    tables = [
        'fireincidentmeans', 'vehicle', 'firefighter', 'fireincidents',
        'firestation', 'fireweatherconditions', 'location_info', 'parishes',
        'municipality', 'sourcealert', 'burntarea', 'datetime', 'district',
        'firecauses'
    ]
    
    with conn.cursor() as cur:
        for table in tables:
            cur.execute(sql.SQL("DELETE FROM {}").format(sql.Identifier(table)))

            # Reset the serial value
            cur.execute(sql.SQL("ALTER SEQUENCE {} RESTART WITH 1").format(sql.Identifier(f"{table}_id_seq")))
        conn.commit()
    print("All data deleted from the database.")

def insert_data(conn, csv_file):
    """Read data from CSV and insert into appropriate tables."""
    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            
            row_count = 0
            print("Inserting data into the database...")
            print(csv_reader.fieldnames)
            for row in csv_reader:
                if row_count >= 30:
                    break
            
                # Insert data into appropriate tables
                with conn.cursor() as cur:
                    try:
                        # Insert into District table
                        cur.execute("SELECT id FROM District WHERE districtname = %s", (row['Distrito'],))
                        result = cur.fetchone()
                
                        if result is None:
                            print("Inserting new district:", row['Distrito'])
                            cur.execute("""
                                INSERT INTO District (districtname)
                                VALUES (%s)
                                RETURNING id
                            """, (row['Distrito'],))
                            district_id = cur.fetchone()[0]
                        else:
                            district_id = result[0]
                                          
                        #Insert into Municipality table
                        cur.execute("SELECT id FROM Municipality WHERE MunicipalityName = %s", (row['Concelho'],))
                        result = cur.fetchone()

                        if result is None:
                            print("Inserting new municipality:", row['Concelho'])
                            cur.execute("""
                                INSERT INTO Municipality (MunicipalityName, district_id)
                                VALUES (%s, %s)
                                RETURNING id
                            """, (row['Concelho'], district_id))
                            municipality_id = cur.fetchone()[0]
                        else:
                            municipality_id = result[0]
                        
                        #Insert into Parishes table
                        cur.execute("SELECT id FROM Parishes WHERE parishname = %s", (row['Freguesia'],))
                        result = cur.fetchone()

                        if result is None:
                            print("Inserting new parish:", row['Freguesia'])
                            cur.execute("""
                                INSERT INTO Parishes (parishname, municipality_id)
                                VALUES (%s, %s)
                                RETURNING id
                            """, (row['Freguesia'], municipality_id))
                            parish_id = cur.fetchone()[0]
                        else:
                            parish_id = result[0]
                        
                        # Insert into DateTime table
                        try:
                            cur.execute("""
                                INSERT INTO DateTime (Year, Month, DataHoraAlerta, DataHora_PrimeiraIntervenc, DataHora_Extincao, Duracao_Horas, IncSup24horas)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                RETURNING id
                            """, (
                                int(row['Year']),
                                int(row['Month']),
                                datetime.strptime(row['DataHoraAlerta'], '%Y-%m-%d %H:%M:%S'),
                                datetime.strptime(row['DataHora_PrimeiraIntervenc'], '%Y-%m-%d %H:%M:%S'),
                                datetime.strptime(row['DataHora_Extincao'], '%Y-%m-%d %H:%M:%S'),
                                float(row['Duracao_Horas']),
                                row['IncSup24horas'].lower() in ['true', '1', 't', 'y', 'yes']
                            ))
                            datetime_id = cur.fetchone()[0]
                            print("Inserted DateTime ID:", datetime_id)
                            
                        except Exception as e:
                            print(f"Error inserting DateTime row: {row}")
                            print(e)
                            conn.rollback()
                            continue


                        # Insert into FireCauses table
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
                        print(f"Error inserting row: {row}")
                        print(e)
                        conn.rollback()
                        continue
                    
            conn.commit()
        print("Data inserted into the database.")
    except Exception as e:
        print("Error reading CSV file or inserting data into the database.")
        print(e)



# Example usage
# conn = psycopg.connect("dbname=test user=postgres password=secret")
# delete_all_data(conn)
# insert_data(conn, 'your_file.csv')