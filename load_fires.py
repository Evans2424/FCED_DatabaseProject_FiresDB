import csv
import psycopg
from psycopg import sql

def delete_all_data(conn):
    """Delete all data from all tables in the database."""
    tables = [
        'fireincidentmeans', 'vehicle', 'firefighter', 'fireincidents',
        'firestation', 'fireweatherconditions', 'location_info', 'municipality',
        'parishes', 'sourcealert', 'burntarea', 'datetime', 'district',
        'firecauses'
    ]
    
    with conn.cursor() as cur:
        for table in tables:
            cur.execute(sql.SQL("DELETE FROM {}").format(sql.Identifier(table)))

            # Reset the serial value
            cur.execute(sql.SQL("ALTER SEQUENCE {} RESTART WITH 1").format(sql.Identifier(f"{table}_id_seq")))
            print("OLA")
        conn.commit()
    print("All data deleted from the database.")

def insert_data(conn, csv_file):
    """Read data from CSV and insert into appropriate tables."""
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        
        row_count = 0
        
        for row in csv_reader:
            if row_count >= 20:
                break
        
            print(">>>>>>>>>>>>")
            print(row['Distrito'])
        
            # Insert data into appropriate tables
            # This is a simplified example. You'll need to adapt this to your specific CSV structure and table relationships
            
            with conn.cursor() as cur:
                # Insert into District table
                cur.execute("SELECT id FROM District WHERE districtname = %s", (row['Distrito'],))
                result = cur.fetchone()
                print(">>>>>>>>>>>>>>><")
                print(result)
        
                if result is None:
                    cur.execute("""
                        INSERT INTO District (districtname)
                        VALUES (%s)
                        RETURNING id
                    """, (row['Distrito'],))
                    district_id = cur.fetchone()[0]
                else:
                    district_id = result[0]
            
            row_count += 1
        
        conn.commit()
        print("Data inserted into the database.")