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
    id SERIAL PRIMARY KEY,
    DistrictName VARCHAR(100)
);

-- Create Municipality table
CREATE TABLE Municipality (
    id SERIAL PRIMARY KEY,
    MunicipalityName VARCHAR(100),
    District_id INT,
    FOREIGN KEY (District_id) REFERENCES District(id)
);

-- Create Parishes table
CREATE TABLE Parishes (
    id SERIAL PRIMARY KEY,
    ParishName VARCHAR(100),
    Municipality_id INT,
    FOREIGN KEY (Municipality_id) REFERENCES Municipality(id)
);

-- Create Location_Info table
CREATE TABLE Location_Info (
    id SERIAL PRIMARY KEY,
    Parish_id INT,
    Local VARCHAR(100),
    RNAP VARCHAR(100),
    RNMPF VARCHAR(100),
    Latitude DECIMAL(9,6),
    Longitude DECIMAL(9,6),
    FOREIGN KEY (Parish_id) REFERENCES Parishes(id)
);

CREATE TABLE DateTime (
    id SERIAL PRIMARY KEY,
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
    id SERIAL PRIMARY KEY,
    description VARCHAR(255)
);

-- Create FireCauses table
CREATE TABLE FireCauses (
    CauseCode INT PRIMARY KEY,
    CauseType VARCHAR(100),
    CauseGroup VARCHAR(100),
    CauseDescription TEXT
);

-- Create BurntArea table
CREATE TABLE BurntArea (
    id SERIAL PRIMARY KEY,
    AreaPov_ha DECIMAL(10,2),
    AreaMato_ha DECIMAL(10,2),
    AreaAgric_ha DECIMAL(10,2),
    AreaTotal_ha DECIMAL(10,2),
    ClasseArea VARCHAR(50)
);

-- Create FireIncidents table
CREATE TABLE FireIncidents (
    id SERIAL PRIMARY KEY,
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
    id SERIAL PRIMARY KEY,
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
    id SERIAL PRIMARY KEY,
    StationName VARCHAR(100),
    Parish INT,
    FOREIGN KEY (Parish) REFERENCES Parishes(id)
);

-- Create Firefighter table
CREATE TABLE Firefighter (
    id SERIAL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Rank VARCHAR(50),
    FireStation_id INT,
    FOREIGN KEY (FireStation_id) REFERENCES FireStation(id)
);

-- Create Vehicle table
CREATE TABLE Vehicle (
    id SERIAL PRIMARY KEY,
    VehicleType VARCHAR(50),
    LicensePlate VARCHAR(20),
    FireStation_id INT,
    FOREIGN KEY (FireStation_id) REFERENCES FireStation(id)
);

-- Create Vehicle_FireIncident join table
CREATE TABLE Vehicle_FireIncident (
    Vehicle_id INT,
    FireIncident_id INT,
    PRIMARY KEY (Vehicle_id, FireIncident_id),
    FOREIGN KEY (Vehicle_id) REFERENCES Vehicle(id),
    FOREIGN KEY (FireIncident_id) REFERENCES FireIncident(id)
);

-- Create Firefighter_FireIncident join table
CREATE TABLE Firefighter_FireIncident (
    Firefighter_id INT,
    FireIncident_id INT,
    PRIMARY KEY (Firefighter_id, FireIncident_id),
    FOREIGN KEY (Firefighter_id) REFERENCES Firefighter(id),
    FOREIGN KEY (FireIncident_id) REFERENCES FireIncident(id)
);

