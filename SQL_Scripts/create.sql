-- Drop existing tables if they exist
DROP TABLE IF EXISTS FireIncidentMeans;
DROP TABLE IF EXISTS Vehicle;
DROP TABLE IF EXISTS Firefighter;
DROP TABLE IF EXISTS FireStation;
DROP TABLE IF EXISTS FireWeatherConditions;
DROP TABLE IF EXISTS FireIncidents;
DROP TABLE IF EXISTS BurntArea;
DROP TABLE IF EXISTS FireCauses;
DROP TABLE IF EXISTS SourceAlert;
DROP TABLE IF EXISTS DateTime;
DROP TABLE IF EXISTS Location_Info;
DROP TABLE IF EXISTS Parishes;
DROP TABLE IF EXISTS Municipality;
DROP TABLE IF EXISTS District;


-- Create District table
CREATE TABLE District (
    id INT PRIMARY KEY,
    DistrictName VARCHAR(100)
);

-- Create Municipality table
CREATE TABLE Municipality (
    id INT PRIMARY KEY,
    MunicipalityName VARCHAR(100),
    District_id INT,
    FOREIGN KEY (District_id) REFERENCES District(id)
);

-- Create Parishes table
CREATE TABLE Parishes (
    id INT PRIMARY KEY,
    ParishName VARCHAR(100),
    Municipality_id INT,
    FOREIGN KEY (Municipality_id) REFERENCES Municipality(id)
);

-- Create Location_Info table
CREATE TABLE Location_Info (
    id INT PRIMARY KEY,
    Parish_id INT,
    Local VARCHAR(100),
    RNAP VARCHAR(100),
    RNMPF VARCHAR(100),
    Latitude DECIMAL(9,6),
    Longitude DECIMAL(9,6),
    FOREIGN KEY (Parish_id) REFERENCES Parishes(id)
);

CREATE TABLE DateTime (
    id INT PRIMARY KEY,
    Year INT,
    Month INT,
    DataHoraAlerta TIMESTAMP,
    DataHora_PrimeiraIntervenc TIMESTAMP,
    DataHora_Extincao TIMESTAMP,
    Duracao_Horas DECIMAL(10,2),
    IncSup24horas BOOLEAN
);

-- Create SourceAlert table
CREATE TABLE SourceAlert (
    id INT PRIMARY KEY,
    description VARCHAR(255)
);

-- Create FireCauses table
CREATE TABLE FireCauses (
    id INT PRIMARY KEY,
    CauseCode VARCHAR(50),
    CauseType VARCHAR(100),
    CauseGroup VARCHAR(100),
    CauseDescription TEXT
);

-- Create BurntArea table
CREATE TABLE BurntArea (
    id INT PRIMARY KEY,
    AreaPov_ha DECIMAL(10,2),
    AreaMato_ha DECIMAL(10,2),
    AreaAgric_ha DECIMAL(10,2),
    AreaTotal_ha DECIMAL(10,2),
    ClasseArea VARCHAR(50)
);

-- Create FireIncidents table
CREATE TABLE FireIncidents (
    id INT PRIMARY KEY,
    Codigo_SGIF VARCHAR(50),
    Codigo_ANEPC VARCHAR(50),
    Area_info_id INT,
    DateTime_info_id INT,
    SourceAlert_id INT,
    Location_id INT,
    FireCause_id INT,
    FOREIGN KEY (Area_info_id) REFERENCES BurntArea(id),
    FOREIGN KEY (DateTime_info_id) REFERENCES DateTime(id),
    FOREIGN KEY (SourceAlert_id) REFERENCES SourceAlert(id),
    FOREIGN KEY (Location_id) REFERENCES Location_Info(id),
    FOREIGN KEY (FireCause_id) REFERENCES FireCauses(id)
);

-- Create FireWeatherConditions table
CREATE TABLE FireWeatherConditions (
    id INT PRIMARY KEY,
    FireIncident_id INT,
    DSR DECIMAL(5,2),
    FWI DECIMAL(5,2),
    ISI DECIMAL(5,2),
    DC DECIMAL(5,2),
    DMC DECIMAL(5,2),
    FFMC DECIMAL(5,2),
    BUI DECIMAL(5,2),
    FOREIGN KEY (FireIncident_id) REFERENCES FireIncidents(id)
);

-- Create FireStation table
CREATE TABLE FireStation (
    id INT PRIMARY KEY,
    StationName VARCHAR(100),
    Parish INT,
    FOREIGN KEY (Parish) REFERENCES Parishes(id)
);

-- Create Firefighter table
CREATE TABLE Firefighter (
    id INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Rank VARCHAR(50),
    FireStation_id INT,
    FOREIGN KEY (FireStation_id) REFERENCES FireStation(id)
);

-- Create Vehicle table
CREATE TABLE Vehicle (
    id INT PRIMARY KEY,
    VehicleType VARCHAR(50),
    LicensePlate VARCHAR(20),
    FireStation_id INT,
    FOREIGN KEY (FireStation_id) REFERENCES FireStation(id)
);

-- Create FireIncidentMeans table
CREATE TABLE FireIncidentMeans (
    id INT PRIMARY KEY,
    FireIncident_id INT,
    Firefighter_id INT,
    Vehicle_id INT,
    FOREIGN KEY (FireIncident_id) REFERENCES FireIncidents(id),
    FOREIGN KEY (Firefighter_id) REFERENCES Firefighter(id),
    FOREIGN KEY (Vehicle_id) REFERENCES Vehicle(id)
);
