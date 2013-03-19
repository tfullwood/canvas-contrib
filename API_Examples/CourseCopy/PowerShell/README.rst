This PowerShell script will programatically do course copies.  It
requires:

- Powershell version 3 or above

Setup
======

Step 1: Copy the `coursecopy.ps1` file to your sytem.  

Step 2: Edit `coursecopy.ps1` to change $token, $outputPath, $CSVFile,
and domain.  You could also change the $source_course_id_column and
$destination_course_id_column variables.  This will allow you to
customize the script to read the columns you add to the CSV file.

Step 3: Create a CSV file to match the format of the example
`csvfile.csv`.  The format is simple, actually, with only two columns:

	source_id,destination_id
	somecanvasid,someothercanvasid


