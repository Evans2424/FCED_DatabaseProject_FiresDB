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
        conn.commit()
    print("All data deleted from the database.")

def insert_data(conn, csv_file):
    """Read data from CSV and insert into appropriate tables."""
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            print(row.keys())  # This will help you see the actual column names in the CSV

            # Insert data into appropriate tables
            # This is a simplified example. You'll need to adapt this to your specific CSV structure and table relationships
            
            with conn.cursor() as cur:
                # Insert into District table
                cur.execute("""
                    INSERT INTO District (districtname)
                    VALUES (%s)
                    ON CONFLICT (districtname) DO NOTHING
                    RETURNING id
                """, (row['Distrito'],))
                district_id = cur.fetchone()[0]
                
                # Insert into Municipality table
                cur.execute("""
                    INSERT INTO Municipality (MunicipalityName, District_id)
                    VALUES (%s, %s)
                    ON CONFLICT (MunicipalityName) DO NOTHING
                    RETURNING id
                """, (row['MunicipalityName'], district_id))
                municipality_id = cur.fetchone()[0]
                
                # Continue with other tables...
                
                # Insert into FireIncidents table
                cur.execute("""
                    INSERT INTO FireIncidents (Codigo_SGIF, Codigo_ANEPC)
                    VALUES (%s, %s)
                """, (row['Codigo_SGIF'], row['Codigo_ANEPC']))
                
                # Add more INSERT statements for other tables as needed
        
        conn.commit()
    print("Data inserted into the database.")