-- Insert data into FireStation table
INSERT INTO FireStation (id, StationName, Parish) VALUES 
(1, 'Central Station', 1),
(2, 'North Station', 2),
(3, 'South Station', 3),
(4, 'East Station', 4),
(5, 'West Station', 5);

-- Insert data into Firefighter table
INSERT INTO Firefighter (id, FirstName, LastName, Rank, FireStation_id) VALUES 
(1, 'John', 'Doe', 'Lieutenant', 1),
(2, 'Jane', 'Smith', 'Captain', 2),
(3, 'Carlos', 'Gomez', 'Firefighter', 1),
(4, 'Anna', 'Johnson', 'Chief', 3),
(5, 'Emily', 'Davis', 'Firefighter', 4),
(6, 'Michael', 'Brown', 'Lieutenant', 5),
(7, 'Sophia', 'Wilson', 'Firefighter', 2),
(8, 'Daniel', 'Taylor', 'Captain', 4),
(9, 'Olivia', 'Anderson', 'Firefighter', 3),
(10, 'Lucas', 'Martinez', 'Firefighter', 5);

-- Insert data into Vehicle table
INSERT INTO Vehicle (id, VehicleType, LicensePlate, FireStation_id) VALUES 
(1, 'Fire Truck', 'FT-1234', 1),
(2, 'Ambulance', 'AMB-5678', 2),
(3, 'Ladder Truck', 'LT-9012', 3),
(4, 'Fire Truck', 'FT-3456', 4),
(5, 'Water Tanker', 'WT-7890', 5),
(6, 'Rescue Vehicle', 'RV-1122', 1),
(7, 'Fire Truck', 'FT-3344', 2),
(8, 'Ambulance', 'AMB-5566', 3),
(9, 'Fire Truck', 'FT-7788', 4),
(10, 'Rescue Vehicle', 'RV-9900', 5);

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