import psycopg

class menu:

    def show_menu():
        print("--------------------------------")
        print("Select Your Option")
        print("--------------------------------")
        print("[1] Fire Incidents By District")
        print("[2] Average Burned Area by Municipality")
        print("[3] Identify Long-Duration Fires")
        print("[4] Number of Firefighters by Station")
        print("[5] Most Common Cause of Fire")
        print("[6] Fire Incidents by Source Alert Description")
        print("[7] Identify Potential High-Risk Areas for Fire Incidents")
        print("[8] Total Response Time Comparison Between Districts")
        print("[9] Total Burned area By date")
        print("[10] Burned area and fire duration of that district")
        print("--------------------------------")
        print("[0] to exit the program")
        print()
        print("What is your choice:")
    
    
    def execute_query(x,**kwargs):
        print(x)
    
    

