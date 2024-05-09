CREATE TABLE License_Plate (
  ID_Card int NOT NULL,
  Time_IN datetime,
  License_Plate_Number varchar(12) PRIMARY KEY,
  Result varchar(4),
  Status varchar(4),
  Lane int,
  Time_OUT datetime,
  IN_Background text,
  IN_License text,
  IN_License_Plate text,
  OUT_Background text,
  OUT_License text,
  OUT_License_Plate text,
);

--id_card, time_in, license_plate, status='IN', result='OK', lane=1, time_out=0, in_background= None,
--in_license = None, in_license_plate = None, out_background= None, out_license = None, out_license_plate = None
