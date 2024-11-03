from tabulate import tabulate
from dataframeplotter import query_plotter

class Menu:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def show_menu(self):
        print("--------------------------------")
        print("Select Your Option")
        print("--------------------------------")
        print("[1] Fire Incidents By District")
        print("[2] Average Burned Area by District")
        print("[3] Identify Long-Duration Fires")
        print("[4] Number of Firefighters by Station")
        print("[5] Most Common Cause of Fire")
        print("[6] Fire Incidents by Source Alert Description")
        print("[7] Identify Potential High-Risk Areas for Fire Incidents")
        print("[8] Total Response Time Comparison Between Districts")
        print("[9] Total Burned area By Month/Year")
        print("[10] Burned by type and fire duration of that district")
        print("--------------------------------")
        print("[0] to exit the program")
        print()
        print("What is your choice:")
    
    def show_options(self,plot_option):
        print("--------------------------------")
        print("Select Your Option")
        print("--------------------------------")
        print("[1] export the response as CSV")
        if plot_option in ['1', '2','8', '9']:
            print("[2] Plot the reponse")
        print("--------------------------------")
        print("[0] return to the mais menu")


    def main_menu(self):
        while True:
            self.show_menu()
            choice = input()
            print("--------------------------------")
            match choice:
                case '0':
                    print("Exiting...")
                    break
                case '1':
                    query = """
                                SELECT d.DistrictName, COUNT(fi.id) AS TotalFireIncidents
                                FROM FireIncidents fi
                                JOIN Location_Info li ON fi.Location_id = li.id
                                JOIN Parishes p ON li.Parish_id = p.id
                                JOIN Municipality m ON p.Municipality_id = m.id
                                JOIN District d ON m.District_id = d.id
                                GROUP BY d.DistrictName
                                ORDER BY TotalFireIncidents DESC;
                            """
                    print(self.db_manager.show_in_pandas(self.db_manager.run_select(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                self.db_manager.export_to_csv(df)
                            case '2':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                plotter = query_plotter()
                                plotter.setfigize(20,10)
                                plotter.setplottitle('Districts vs FireIncidents')
                                plotter.bar_plot(df,'districtname','totalfireincidents')
                case '2':
                    query = """
                                SELECT d.DistrictName, AVG(b.AreaTotal_ha) AS AverageBurnedArea
                                FROM BurntArea b
                                JOIN FireIncidents fi ON b.id = fi.Area_info_id
                                JOIN Location_Info li ON fi.Location_id = li.id
                                JOIN Parishes p ON li.Parish_id = p.id
                                JOIN Municipality m ON p.Municipality_id = m.id
                                JOIN District d ON m.District_id = d.id
                                GROUP BY d.DistrictName
                                ORDER BY AverageBurnedArea DESC;
                            """
                    print(self.db_manager.show_in_pandas(self.db_manager.run_select(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                self.db_manager.export_to_csv(df)
                            case '2':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                plotter = query_plotter()
                                plotter.setfigize(20,10)
                                plotter.setplottitle('Districts vs AverageBurnedArea')
                                plotter.bar_plot(df,'districtname','averageburnedarea')
                case '3':
                    query = """
                                SELECT 
                                    fi.Codigo_SGIF,
                                    fi.Codigo_ANEPC,
                                    dt.DataHoraAlerta,
                                    dt.DataHora_PrimeiraIntervenc,
                                    dt.DataHora_Extincao,
                                    dt.Duracao_Horas
                                FROM FireIncidents fi
                                JOIN DateTime dt ON fi.DateTime_info_id = dt.id
                                WHERE dt.Duracao_Horas > 24
                                ORDER BY dt.Duracao_Horas DESC;
                            """
                    print(self.db_manager.show_in_pandas(self.db_manager.run_select(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                self.db_manager.export_to_csv(df)
                case '4':
                    query = """SELECT FireStation_id, COUNT(*) AS NumberOfFirefighters 
                               FROM Firefighter 
                               GROUP BY FireStation_id
                               """
                    print(self.db_manager.show_in_pandas(self.db_manager.run_select(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                self.db_manager.export_to_csv(df)
                case '5':
                    query = """SELECT FireCauses.CauseDescription, COUNT(FireIncidents.FireCause_id) AS NumberOfOccurrences 
                                FROM FireIncidents JOIN FireCauses ON FireIncidents.FireCause_id = FireCauses.CauseCode
                                GROUP BY FireCauses.CauseDescription
                                HAVING COUNT(FireIncidents.FireCause_id) >= ALL (SELECT COUNT(FireIncidents.FireCause_id)
                                FROM FireIncidents JOIN FireCauses ON FireIncidents.FireCause_id = FireCauses.CauseCode
                                GROUP BY FireCauses.CauseDescription)
                                   """
                    print(self.db_manager.show_in_pandas(self.db_manager.run_select(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                self.db_manager.export_to_csv(df)
                case '6':
                    query = """SELECT SourceAlert.description, COUNT(FireIncidents.SourceAlert_id) AS NumberOfIncidents
                               FROM FireIncidents JOIN SourceAlert ON FireIncidents.SourceAlert_id = SourceAlert.id
                               GROUP BY SourceAlert.description
                               ORDER BY NumberOfIncidents DESC
                               """
                    print(self.db_manager.show_in_pandas(self.db_manager.run_select(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                self.db_manager.export_to_csv(df)
                case '7':
                    query = """SELECT M.MunicipalityName, COUNT(FireIncidents.Codigo_SGIF) AS NumberOfIncidents
                               FROM FireIncidents JOIN Location_info ON FireIncidents.Location_id = Location_info.id
                               JOIN Parishes P ON Location_info.Parish_id = P.id
                               JOIN Municipality M ON P.Municipality_id = M.id
                               GROUP BY M.MunicipalityName
                               ORDER BY NumberOfIncidents DESC
                    """
                    print(self.db_manager.show_in_pandas(self.db_manager.run_select(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                self.db_manager.export_to_csv(df)
                case '8':
                    query = """
                    with CTE as (SELECT d.DistrictName, EXTRACT(EPOCH FROM AGE(dt.DataHora_primeiraIntervenc, dt.datahoraalerta)) / 3600  AS hours_diff
                    FROM FireIncidents fi
                    join DateTime as dt on dt.id = fi.DateTime_info_id                                 
                    JOIN Location_Info li ON fi.Location_id = li.id
                    JOIN Parishes p ON li.Parish_id = p.id
                    JOIN Municipality m ON p.Municipality_id = m.id
                    JOIN District d ON m.District_id = d.id)
                    SELECT DistrictName,
                    ROUND(cast(sum(hours_diff) as numeric),2) as TIME_TO_RESPONSE
                    from CTE group by DistrictName
                    """
                    print(self.db_manager.show_in_pandas(self.db_manager.run_select(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                self.db_manager.export_to_csv(df)
                            case '2':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                plotter = query_plotter()
                                plotter.setfigize(20,10)
                                plotter.setplottitle('Districts vs TIME_TO_RESPONSE')
                                plotter.bar_plot(df,'districtname','time_to_response')

                case '9':
                    query = '''
                    select SUM(b.AreaTotal_ha) AS TOTAL,TO_CHAR(dt.datahoraalerta, 'MM/YYYY') as DATE
                    from burntarea as b 
                    join Fireincidents as fi on fi.Area_info_id = b.id 
                    join DateTime as dt on dt.id = fi.DateTime_info_id
                    group by TO_CHAR(dt.datahoraalerta, 'MM/YYYY'), 
                            EXTRACT(YEAR FROM dt.datahoraalerta), 
                            EXTRACT(MONTH FROM dt.datahoraalerta)
                    ORDER BY EXTRACT(YEAR FROM dt.datahoraalerta), 
                            EXTRACT(MONTH FROM dt.datahoraalerta);
                    '''
                    
                    print(self.db_manager.show_in_pandas(self.db_manager.run_select(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                self.db_manager.export_to_csv(df)
                            case '2':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                plotter = query_plotter()
                                plotter.setfigize(20,10)
                                plotter.setplottitle('Line Chart total vs Date')
                                plotter.line_plot(df,'date','total')

                case '10':
                    districts = ["Aveiro","Vila Real","Viseu","Bragança","Braga","Viana do Castelo","Porto","Lisboa","Coimbra","Beja","Castelo Branco","Setúbal","Guarda","Faro","Santarém","Portalegre","Leiria","Évora"]
                    print("Your Options:")
                    print(districts)
                    district = input("Select your district: ")
                    if district not in districts:
                        print("Invalid District Name")
                        continue
                    print(district)
                    query = f"""
                    SELECT fi.Codigo_SGIF, 
                    Duracao_Horas,
                    AreaPov_ha,
                    AreaMato_ha,
                    AreaAgric_ha,
                    Districtname 
                    FROM fireIncidents as fi
                    Join burntarea as ba on fi.Area_info_id = ba.id 
                    join Location_info as li on li.id = fi.Location_id
                    join Parishes as pa on pa.id = li.parish_id
                    join Municipality as mu on mu.id = pa.Municipality_id
                    join District on District.id = mu.District_id
                    join Datetime as dt on dt.id = fi.DateTime_info_id
                    where District.DistrictName = '{district}'
                    """
                    print(self.db_manager.show_in_pandas(self.db_manager.run_select(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.db_manager.run_select(query))
                                self.db_manager.export_to_csv(df)
                case _:
                    print("Invalid choice. Please try again.")
