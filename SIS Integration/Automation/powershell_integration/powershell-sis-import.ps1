$sourceDir = ".\" #this is source directory literal path
$outputPath = ".\" #output path for the zip file creation
$outputZip = ".\courses1.csv.zip" # name of the zip file
$url = "https://cwt.test.instructure.com/api/v1/accounts/82726/sis_imports.json?import_type=instructure_csv&access_token="
$token = "h3xyPlREWirj4FDjJTzlpAWPakHgVzCx0nJlwYA4XcX2tvqa6j6YEBo7AoOfvSQW" # access_token
$contentType = "application/zip" # don't change
$InFile = $outputPath+$outputZip # don't change
$uri = $url+$token # don't change


#write-zip -Path $sourceDir"*.csv" -OutputPath $outputPath$outputZip

$t = get-date -format M_d_y_h

$results = invoke-RestMethod -InFile $InFile -Method POST -PassThru -ContentType $contentType -uri $uri -OutFile $outputPath$t"-status.log"

Write-Host "output here"

Write-Host $results.workflow_state




Move-Item $outputPath$outputZip $outputPath$t-$outputZip
Remove-Item $sourceDir*.csv
