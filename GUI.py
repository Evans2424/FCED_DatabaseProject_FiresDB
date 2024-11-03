from tabulate import tabulate


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
        print("[9] Total Burned area By date where alert was in 2022")
        print("[10] Burned area and fire duration of that district")
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

    def query_executor(self,option_query):
        db_response = self.db_manager.run_select(option_query)
        return db_response

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
                    query = "SELECT 'HELLO WORLD'"
                    print(self.db_manager.show_in_pandas(self.query_executor(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.query_executor(query))
                                self.db_manager.export_to_csv(df)
                case '2':
                    query = "SELECT 'HELLO WORLD'"
                    print(self.db_manager.show_in_pandas(self.query_executor(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.query_executor(query))
                                self.db_manager.export_to_csv(df)
                case '3':
                    query = "SELECT 'HELLO WORLD'"
                    print(self.db_manager.show_in_pandas(self.query_executor(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.query_executor(query))
                                self.db_manager.export_to_csv(df)
                case '4':
                    query = """SELECT FireStation_id, COUNT(*) AS NumberOfFirefighters 
                               FROM Firefighter 
                               GROUP BY FireStation_id
                               """
                    print(self.db_manager.show_in_pandas(self.query_executor(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.query_executor(query))
                                self.db_manager.export_to_csv(df)
                case '5':
                    query = """SELECT FireCauses.CauseDescription, COUNT(FireIncident.FireCause_id) AS NumberOfOccurrences 
                               FROM FireIncident JOIN FireCauses ON FireIncident.FireCause_id = FireCauses.CauseCode
                               GROUP BY FireCauses.CauseDescription
                               HAVING COUNT(FireIncident.FireCause_id) >= ALL (
                                   SELECT COUNT(FireIncident.FireCause_id)
                                   FROM FireIncident JOIN FireCauses ON FireIncident.FireCause_id = FireCauses.CauseCode
                                   GROUP BY FireCauses.CauseDescription)
                                   """
                    print(self.db_manager.show_in_pandas(self.query_executor(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.query_executor(query))
                                self.db_manager.export_to_csv(df)
                case '6':
                    query = """SELECT SourceAlert.description, COUNT(FireIncident.SourceAlert_id) AS NumberOfIncidents
                               FROM FireIncident JOIN SourceAlert ON FireIncident .SourceAlert_id = SourceAlert.id
                               GROUP BY SourceAlert.description
                               ORDER BY NumberOfIncidents DESC
                               """
                    print(self.db_manager.show_in_pandas(self.query_executor(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.query_executor(query))
                                self.db_manager.export_to_csv(df)
                case '7':
                    query = """SELECT Municipality.MunicipalityName, COUNT(FireIncident.Codigo_SGIF) AS NumberOfIncidents
                               FROM FireIncident JOIN Location ON FireIncident.Location_id = Location.id
                               JOIN Parish ON Location.Parish_id = Parish.id
                               JOIN Municipality M ON P.Municipality_id = M.id
                               GROUP BY Municipality.MunicipalityName
                               ORDER BY NumberOfIncidents DESC
                    """
                    print(self.db_manager.show_in_pandas(self.query_executor(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.query_executor(query))
                                self.db_manager.export_to_csv(df)
                case '8':
                    query = "SELECT 'HELLO WORLD'"
                    print(self.db_manager.show_in_pandas(self.query_executor(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.query_executor(query))
                                self.db_manager.export_to_csv(df)

                case '9':
                    query = '''
                    select SUM(b.AreaTotal_ha) AS TOTAL,TO_CHAR(dt.datahoraalerta, 'DD/MM/YYYY') as DATE
                    from burntarea as b 
                    join Fireincidents as fi on fi.Area_info_id = b.id 
                    join DateTime as dt on dt.id = fi.DateTime_info_id
                    group by TO_CHAR(dt.datahoraalerta, 'DD/MM/YYYY') 
                    HAVING RIGHT(TO_CHAR(dt.datahoraalerta, 'DD/MM/YYYY'),4) = '2022' 
                    '''
                    
                    print(self.db_manager.show_in_pandas(self.query_executor(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.query_executor(query))
                                self.db_manager.export_to_csv(df)
                case '10':
                    query = "SELECT 'HELLO WORLD'"
                    print(self.db_manager.show_in_pandas(self.query_executor(query)))
                    while True:
                        self.show_options(choice)
                        choice_options = input()
                        match choice_options:
                            case '0':
                                break
                            case '1':
                                df = self.db_manager.show_in_pandas(self.query_executor(query))
                                self.db_manager.export_to_csv(df)
                case _:
                    print("Invalid choice. Please try again.")
