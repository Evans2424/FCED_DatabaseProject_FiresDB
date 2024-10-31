def insert_data(conn, csv_file):
    """Read data from CSV and insert into appropriate tables."""
    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            
            row_count = 0
            
            for row in csv_reader:
                if row_count >= 20:
                    break

                print("Processing row:", row)
            
                # Insert data into appropriate tables
                with conn.cursor() as cur:
                    try:
                        # Convert CodCausa to integer if not NULL and not NaN
                        cod_causa = row['CodCausa']
                        if cod_causa and not math.isnan(float(cod_causa)):
                            cause_code = int(float(cod_causa))
                        else:
                            cause_code = None

                        if cause_code is not None:
                            cur.execute("SELECT CauseCode FROM FireCauses WHERE CauseCode = %s::text", (str(cause_code),))
                            result = cur.fetchone()

                            if result is None:
                                print("Inserting new fire cause:", cod_causa)
                                cur.execute("""
                                    INSERT INTO FireCauses (CauseCode, CauseType, CauseGroup, CauseDescription)
                                    VALUES (%s, %s, %s, %s)
                                    RETURNING CauseCode
                                """, (str(cause_code), row['TipoCausa'], row['GrupoCausa'], row['DescricaoCausa']))
                                cause_code = cur.fetchone()[0]
                            else:
                                cause_code = result[0]
                        else:
                            cause_code = None

                        # Check if FonteAlerta is not None or NaN
                        fonte_alerta = row['FonteAlerta']
                        if isinstance(fonte_alerta, str) and fonte_alerta.lower() != 'nan':
                            cur.execute("SELECT id FROM SourceAlert WHERE description = %s", (fonte_alerta,))
                            result = cur.fetchone()

                            source_alert_id = result[0] if result else cur.execute("""
                                INSERT INTO SourceAlert (description)
                                VALUES (%s) RETURNING id
                            """, (fonte_alerta,)).fetchone()[0]
                        else:
                            source_alert_id = None

                        # Check if Duracao_Horas is not NULL
                        duracao_horas = row['Duracao_Horas']
                        duracao_horas_value = float(duracao_horas.replace(',', '.')) if duracao_horas else None

                        # Insert into BurntArea table
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

                        # Insert into DateTime table
                        cur.execute("""
                            INSERT INTO DateTime (Year, Month, DataHoraAlerta, DataHora_PrimeiraIntervenc, DataHora_Extincao, Duracao_Horas, IncSup24horas)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            RETURNING id
                        """, (
                            int(row['Year']),
                            int(row['Month']),
                            datetime.strptime(row['DataHoraAlerta'], '%d/%m/%Y %H:%M'),
                            datetime.strptime(row['DataHora_PrimeiraIntervenc'], '%d/%m/%Y %H:%M'),
                            datetime.strptime(row['DataHora_Extincao'], '%d/%m/%Y %H:%M'),
                            duracao_horas_value,
                            row['IncSup24horas'].lower() in ['true', '1', 't', 'y', 'yes']
                        ))
                        datetime_id = cur.fetchone()[0]
                        print("Inserted DateTime ID:", datetime_id)

                        # Insert into FireWeatherConditions table
                        try:
                            fire_incident_id = int(row['FireIncident_id'])

                            dsr = row['DSR']
                            dsr_value = float(dsr.replace(',', '.')) if dsr else None

                            fwi = row['FWI']
                            fwi_value = float(fwi.replace(',', '.')) if fwi else None

                            isi = row['ISI']
                            isi_value = float(isi.replace(',', '.')) if isi else None

                            dc = row['DC']
                            dc_value = float(dc.replace(',', '.')) if dc else None

                            dmc = row['DMC']
                            dmc_value = float(dmc.replace(',', '.')) if dmc else None

                            ffmc = row['FFMC']
                            ffmc_value = float(ffmc.replace(',', '.')) if ffmc else None

                            bui = row['BUI']
                            bui_value = float(bui.replace(',', '.')) if bui else None

                            cur.execute("""
                                INSERT INTO FireWeatherConditions (FireIncident_id, DSR, FWI, ISI, DC, DMC, FFMC, BUI)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                RETURNING id
                            """, (
                                int(row['FireIncident_id']),
                                dsr_value,
                                fwi_value,
                                isi_value,
                                dc_value,
                                dmc_value,
                                ffmc_value,
                                bui_value
                            ))
                            fire_weather_conditions_id = cur.fetchone()[0]
                            print("Inserted FireWeatherConditions ID:", fire_weather_conditions_id)
                        except Exception as e:
                            print(f"Error inserting into FireWeatherConditions: {e}")
                            print(f"Row data: {row}")
                            conn.rollback()
                            continue

                        # Insert into Location_Info table
                        cur.execute("""
                            INSERT INTO Location_Info (Parish_id, Local, RNAP, RNMPF, Latitude, Longitude)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            RETURNING id
                        """, (
                            int(row['Parish_id']),
                            row['Local'],
                            row['RNAP'],
                            row['RNMPF'],
                            float(row['Latitude'].replace(',', '.')),
                            float(row['Longitude'].replace(',', '.'))
                        ))
                        location_info_id = cur.fetchone()[0]
                        print("Inserted Location_Info ID:", location_info_id)

                        # Insert into FireIncidents table
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
# insert_data(conn, 'your_file.csv')