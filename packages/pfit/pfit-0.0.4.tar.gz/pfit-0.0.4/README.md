# Introduction
The Permafrost File Interoperability Toolkit (PFIT) is designed to promote interoperability and the adoption of standards for permafrost data files. This package currently supports the NTGS ground temperature standard. It includes tools to check and manipulate ground temperature data.

# File Data Checker
The `FileDataChecker` checks column names and values for CSV, XLS, and XLSX files. It logs issues with the files being read in if they do not conform to the NTGS standard.

The following errors may be reported:

- Invalid Time - Time does not follow a valid time in the format HH:MM:SS.
- Invalid Date - Date values should be formatted as YYYY-MM-DD.
- Unexpected Column - One of the first 6 column names is not from the expected list of column names (or is not in the correct order). If this warning occurs, the columns must be resolved in the correct name and order first, otherwise no other checking is done.
- Unexpected Metre - All following metre columns after the first 6 column names should be formatted as "<decimal>_m" only.
- No Measurements - No measurement columns are detected in the file.
- File Type - The file read in is not supported.
- Coordinate - A latitude or longitude value contains something that is not valid.
- Latitude - A latitude value is found that is not valid (Less than -90 or greater than 90).
- Longitude - A longitude value is found that is not valid (Less than -180 or greater than 180).
- Temperature - A temperature value is found that is not a valid temperature.


_XLS and XLSX files are **not recommended** as they can be problematic when parsing date/time values. Please consider saving data in CSV format._

_If you do decide to use XLS(X) files, ensure that the data is located in the first sheet as this is is the only sheet that is checked_.
 
# CSV Column Melter
The `CSVColMelter` accepts existing ground temperature data files that are in the **wide** format and converts it to the **long** CSV format through  transposition of depth columns. Files must conform to the NTGS-style ground temperature file format. This can be verified with the `FileDataChecker`.

# Conversion to NetCDF 
`NTGS_to_NetCDF` converts NTGS-style CSV files into NetCDF (`.nc`). Currently a work in progress.


