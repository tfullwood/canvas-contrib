$token = "<access_token>" # access_token
$outputPath = ".\archives\"
$CSVFile = ".\csvfile.csv"
$domain = "cwt.test.instructure.com"

Import-Csv $CSVFile |foreach {
  $uri = "https://"+$domain+"/api/v1/courses/" + $_.destination + "/course_copy?access_token=" + $token + "&source_course=" + $_.source
  #Write-Host $url
  $logpath = $outputPath+ "_" + $_.source + "_"+$_.destination+"-status.log"
  Write-Host $logpath
  $result = Invoke-RestMethod -Method POST -uri $uri -OutFile $logpath
  Write-Host $result
}

if(Test-Path -Path $outputPath){
}else{
    mkdir $outputPath
}

$t = get-date -format M_d_y_h
$processed_path = $outputPath+$CSVFILE+".processed_"+$t

#Move-Item $CSVFile $processed_path
