$sourceDir = "" #this is source directory literal path
$outputPath = "" #output path for the zip file creation
$outputZip = ".zip" # name of the zip file
$url = "https://<canvas domain>/api/v1/accounts/1/sis_imports.json?import_type=instructure_csv&access_token="
$token = "<Access token>" # access_token
$contentType = "application/zip" # don't change
$InFile = $outputPath+$outputZip # don't change
$uri = $url+$token # don't change


write-zip -Path $sourceDir"*.csv" -OutputPath $outputPath$outputZip

$t = get-date -format M_d_y_h

invoke-RestMethod -InFile $InFile -Method POST -ContentType $contentType -uri $uri -OutFile $outputPath$t"-status.log"

Move-Item $outputPath$outputZip $outputPath$t-$outputZip
Remove-Item $sourceDir*.csv
