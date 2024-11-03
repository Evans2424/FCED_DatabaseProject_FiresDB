# FCED_DatbaseProject_FiresDB
This project involves creating a database to manage detailed data on fire incidents in Portugal. The database is designed to store detailed information about each fire incident and provide tools for data querying and visualization. The project includes tasks to design the database, load data, and implement both command-line and graphical interfaces for user interaction with the database.
Files Included in this Zip
UML_diagram.pdf
Contains the UML diagram that represents the database structure. This diagram defines the tables and relationships for storing data on fire incidents, including details on the incidents themselves and any associated metadata.
relational.pdf
Specifies the relational model based on the UML diagram, detailing the database schema, including table structures, keys, and relationships.
create.sql
A SQL script used to set up the database structure in PostgreSQL by creating all necessary tables.
load_fires.py
A Python script designed to load fire incident data into the database. It performs the following operations:
Deletes any existing data in the relevant tables to ensure a clean slate.
Reads data from a CSV file containing fire incident information.
Inserts the data into the appropriate tables.
Provides editable fields for easy modification of database credentials and schema settings.
GUI.py
A Python script that offers a graphical user interface (GUI) for querying the database. It allows users to view detailed information about fire incidents, search for specific records, and access relevant data stored in the database.
Dataframeplotter.py
A Python script used to generate graphs and visualizations for specific database queries. This is particularly useful for analysis and insights based on the dataset.
      7.   DatabaseManager.py
Main.py
The main script for starting the project. This script should be edited to include the correct database connection credentials. It initializes the database connection and coordinates the functionality of the other scripts.
Group Member Contributions
José Pedro Evans de Carvalho Nobre João (up202108818):
Pooja Muchnur Muneswarappa (up202308623):
Ricardo Jorge Correia Pinto (up201202477):
Vitor Souza Piña (up202400084):