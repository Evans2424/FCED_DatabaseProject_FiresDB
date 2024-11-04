-- Reset the sequence for FireStation table
ALTER SEQUENCE FireStation_id_seq RESTART WITH 1;

-- Reset the sequence for Firefighter table
ALTER SEQUENCE Firefighter_id_seq RESTART WITH 1;

-- Reset the sequence for Vehicle table
ALTER SEQUENCE Vehicle_id_seq RESTART WITH 1;

-- Insert data into FireStation table
INSERT INTO FireStation (StationName, Parish) VALUES 
('Central Station', 1),
('North Station', 2),
('South Station', 3),
('East Station', 4),
('West Station', 5);

-- Insert data into Firefighter table
INSERT INTO Firefighter (FirstName, LastName, Rank, FireStation_id) VALUES 
('John', 'Doe', 'Lieutenant', 1),
('Jane', 'Smith', 'Captain', 2),
('Carlos', 'Gomez', 'Firefighter', 1),
('Anna', 'Johnson', 'Chief', 3),
('Emily', 'Davis', 'Firefighter', 4),
('Michael', 'Brown', 'Lieutenant', 5),
('Sophia', 'Wilson', 'Firefighter', 2),
('Daniel', 'Taylor', 'Captain', 4),
('Olivia', 'Anderson', 'Firefighter', 3),
('Lucas', 'Martinez', 'Firefighter', 5);

-- Insert data into Vehicle table
INSERT INTO Vehicle (VehicleType, LicensePlate, FireStation_id) VALUES 
('Fire Truck', 'FT-1234', 1),
('Ambulance', 'AMB-5678', 2),
('Ladder Truck', 'LT-9012', 3),
('Fire Truck', 'FT-3456', 4),
('Water Tanker', 'WT-7890', 5),
('Rescue Vehicle', 'RV-1122', 1),
('Fire Truck', 'FT-3344', 2),
('Ambulance', 'AMB-5566', 3),
('Fire Truck', 'FT-7788', 4),
('Rescue Vehicle', 'RV-9900', 5);

-- Insert data into Vehicle_fireIncident table
INSERT INTO Vehicle_fireIncident (Vehicle_id, FireIncident_id) VALUES 
(1, 101),
(2, 102),
(3, 103),
(4, 104),
(5, 105),
(6, 106),
(7, 107),
(8, 108),
(9, 109),
(10, 110);

-- Insert data into Firefighter_fireIncident table
INSERT INTO Firefighter_fireIncident (Firefighter_id, FireIncident_id) VALUES 
(1, 101),
(2, 102),
(3, 103),
(4, 104),
(5, 105),
(6, 106),
(7, 107),
(8, 108),
(9, 109),
(10, 110);