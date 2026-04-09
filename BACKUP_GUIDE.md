# Vehicle Data Backup System

## Overview
BikeVault now automatically backs up all vehicle data to an Excel file whenever you add or modify a vehicle. This ensures you have a complete backup in case of database issues.

## Features

✅ **Automatic Backup**: Every vehicle added is automatically saved to an Excel file  
✅ **Complete Data**: All vehicle details are included in the backup  
✅ **Admin Access**: Only admins can download the backup  
✅ **Backup Location**: `backups/vehicles_backup.xlsx`  
✅ **Formatted Excel**: Professional formatting with colors, borders, and proper column widths  

## How It Works

1. **When You Add a Vehicle**:
   - Vehicle is saved to the database
   - Vehicle data is then added to `backups/vehicles_backup.xlsx`
   - A record appears in the sheet with all details

2. **Downloading the Backup**:
   - Go to Admin Panel
   - Click "📥 Download Backup" button
   - The Excel file downloads with timestamp: `vehicles_backup_YYYYMMDD_HHMMSS.xlsx`

3. **Excel File Structure**:
   - Header row with field names (bold, Bosch red background)
   - One row per vehicle with all details
   - Alternate row coloring for readability
   - Auto-fitted column widths

## Columns in Backup

The backup Excel file includes:
- ID, Vehicle Name, RC Number, Owner
- Bike Model, Chassis, Engine, Fuel Type
- Status, Received On, Insurance
- Number Plate, Registration Date, Manufacturing Date
- Inertia, CC, Gears, Road Load values
- Oil Grade, Coolant Grade, Start/End Dates
- Vehicle Condition (Keys, Scratches, Dents, Glass, Tire, Battery, Lights, Engine)
- Condition Notes, Timestamp

## Safety Benefits

✅ **Database Failure Protection**: If database corrupts, Excel file has all data  
✅ **Easy Data Recovery**: Open Excel file and re-enter if needed  
✅ **Offline Access**: Excel file can be viewed without the system running  
✅ **Audit Trail**: Timestamp shows when each vehicle was backed up  

## File Location

- **Main Backup File**: `backups/vehicles_backup.xlsx`
- **Auto-backed up after each**:
  - New vehicle added
  - Vehicle modified/updated
  - Vehicle status changed

## Usage Example

1. Admin adds a new vehicle → Automatically backed up
2. Admin goes to Admin Panel
3. Clicks "📥 Download Backup"
4. Excel file downloads with all vehicles
5. Can be saved securely as archive

---

**Note**: Backups are automatically created in the `/backups/` folder. Keep these files safe for disaster recovery.
