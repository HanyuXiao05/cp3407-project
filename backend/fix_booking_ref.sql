-- Fix BOOKING_Ref column length to accommodate longer booking references
-- This script updates the booking table to allow longer booking reference numbers

USE jcu_gym_ms_db;

-- Alter the BOOKING_Ref column to allow longer strings
ALTER TABLE booking MODIFY COLUMN BOOKING_Ref VARCHAR(20) NOT NULL;

-- Update the BOOKING_Status enum to include 'Confirmed' status
ALTER TABLE booking MODIFY COLUMN BOOKING_Status ENUM('Booked', 'Deleted', 'Attended', 'No-Show', 'Confirmed', 'Cancelled') NOT NULL;

-- Verify the changes
DESCRIBE booking; 