# Conversion of implicit textual damage locations of bridge inspection data in geometrical representations using Linked Data
In this project, an approach was created to automatically convert textual damage information into geometrical representations using Linked Data. The project bases on the definitions of the ASB-ING (basis for collecting and managing bridge inspection data in Germany) and  works with data which has been entered in the database application "SIB-Bauwerke".

## Requirements:
- Damage inspection information converted into .ttl file
- IFC model of bridge 
- IFC model of bridge converted into LBD format

## Procedure:
1. Run file "01_Building_Component_Location" to associate building components in the data file to their geometrical representation
2. Run file "02_Damage_Location" to locate damages in the data file in the IFC model
3. Run file "03_Damage_Representation" to create:

   - BCF file with damages in form of issues 
   - IFC file with point representation of damages
