-- Update BOOKING_Ref column to accommodate 16-character references
ALTER TABLE `booking` MODIFY COLUMN `BOOKING_Ref` varchar(20) NOT NULL; 