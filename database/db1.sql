INSERT INTO License_Plate (
  License_Plate_Number,
  ID_Card,
  Time_IN,
  Time_OUT,
  Result,
  Status,
  Lane,
  IN_Background,
  IN_License,
  IN_License_Plate,
  OUT_Background,
  OUT_License,
  OUT_License_Plate
)
VALUES (
  '12-B1168.88',  -- Replace with actual license plate number
  123456,          -- Replace with actual ID card number
  GETDATE(),       -- Inserts current date and time
  GETDATE(),            -- Set Time_OUT if unknown
  'OK',            -- Replace with appropriate result (Ok/Fail)
  'IN',            -- Replace with appropriate status (IN/OUT)
  1,               -- Replace with actual lane number
  NULL, -- Replace with actual background image path
  NULL,   -- Replace with actual license data path
  NULL,
  NULL,
  NULL,
  NULL-- Replace with actual license plate image path
);
