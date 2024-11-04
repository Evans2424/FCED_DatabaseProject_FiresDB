-- Drop existing tables if they exist
DROP TABLE IF EXISTS Vehicle CASCADE;
DROP TABLE IF EXISTS Firefighter CASCADE;
DROP TABLE IF EXISTS FireStation CASCADE;
DROP TABLE IF EXISTS FireWeatherConditions CASCADE;
DROP TABLE IF EXISTS FireIncidents CASCADE;
DROP TABLE IF EXISTS BurntArea CASCADE;
DROP TABLE IF EXISTS FireCauses CASCADE;
DROP TABLE IF EXISTS SourceAlert CASCADE;
DROP TABLE IF EXISTS DateTime CASCADE;
DROP TABLE IF EXISTS Location_Info CASCADE;
DROP TABLE IF EXISTS Parishes CASCADE;
DROP TABLE IF EXISTS Municipality CASCADE;
DROP TABLE IF EXISTS District CASCADE;
DROP TABLE IF EXISTS Vehicle_fireIncident CASCADE;
DROP TABLE IF EXISTS Firefighter_fireIncident CASCADE;




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
    Local VARCHAR(200),
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
    CauseType VARCHAR(300),
    CauseGroup VARCHAR(300),
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

-- Create FireWeatherConditions table
CREATE TABLE FireWeatherConditions (
    id SERIAL PRIMARY KEY,
    DSR DECIMAL(10,4),
    FWI DECIMAL(10,4),
    ISI DECIMAL(10,4),
    DC DECIMAL(10,4),
    DMC DECIMAL(10,4),
    FFMC DECIMAL(10,4),
    BUI DECIMAL(10,4)
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
    FireWeatherConditions_id INT,
    FOREIGN KEY (Area_info_id) REFERENCES BurntArea(id),
    FOREIGN KEY (DateTime_info_id) REFERENCES DateTime(id),
    FOREIGN KEY (SourceAlert_id) REFERENCES SourceAlert(id),
    FOREIGN KEY (Location_id) REFERENCES Location_Info(id),
    FOREIGN KEY (FireCause_id) REFERENCES FireCauses(CauseCode),
    FOREIGN KEY (FireWeatherConditions_id) REFERENCES FireWeatherConditions(id)
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
CREATE TABLE Vehicle_fireIncident (
    Vehicle_id INT,
    FireIncident_id INT,
    PRIMARY KEY (Vehicle_id, FireIncident_id),
    FOREIGN KEY (Vehicle_id) REFERENCES Vehicle(id),
    FOREIGN KEY (FireIncident_id) REFERENCES FireIncidents(id)
);

-- Create Firefighter_FireIncident join table
CREATE TABLE Firefighter_fireIncident (
    Firefighter_id INT,
    FireIncident_id INT,
    PRIMARY KEY (Firefighter_id, FireIncident_id),
    FOREIGN KEY (Firefighter_id) REFERENCES Firefighter(id),
    FOREIGN KEY (FireIncident_id) REFERENCES FireIncidents(id)
);

