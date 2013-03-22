<#
 You will need to edit several variables here at the top of this script. 
 $token = the access token from Canvas
 $workingPath = the full working path to where the csv files are created.  
    This is where the logs and archive folders will be created
 $CSVFileName = the name of course copy CSV file as it will be created in
    the $workingPath.
 $domain = the full domain name you use to access canvas. (i.e. something.instructure.com)
#>

$token = "<access_token>" # access_token
$workingPath = "C:\path\to\working\folder\"; # Important! Make sure this ends with a backslash
$CSVFileName = "csvfile.csv" # The name of the course copy CSV file.  Not the full path
$domain = "<schoolname_test>.instructure.com"
$source_course_id_column = "source_id"
$destination_course_id_column = "destination_id"


<# ------------- Don't edit anything past here unless you know what you are doing.
    NOTE: No offense, you probably do know what you're doing.  This is for those that
    do not.  
#>

# Just in case $workinPath doesn't end with a \, add it.
if(!($workingPath.EndsWith('\'))){
    $workingPath += "\"
    Write-Host "You path didn't end with a \ so I added one.  It really is important"
}
if($CSVFileName.Contains('\')){
    Write-Host "The CSVFilename should not contain backslashes.  You are warned"
}

$CSVFilePath = $workingPath + $CSVFileName
$archivePath = $workingPath + "archives\"
$logPath = $workingPath + "logs\"
$timestamp = get-date -format yyyy_MM_dd_HH
$logFilePath = $logPath + $timestamp + ".log"
$cacheFilePath = $logPath + "copy_cache.json"
<# Create several paths that are needed for the script to run.
These paths may exist already, but this is a check #>
if(!(Test-Path -Path $archivePath)){
    mkdir $archivePath
}
if(!(Test-Path -Path $logPath)){
    mkdir $logPath
}
if(!(Test-Path -Path $logFilePath))
  {
   new-item -Path $logFilePath –itemtype file
  }
 
if(!(Test-Path -Path $cacheFilePath))
  {
   new-item -Path $cacheFilePath –itemtype file
   $copyCache = [ordered]@{}
   $copyCache.sources = @{}
   $copyCache.ToString() | ConvertTo-Json | Set-Content -Path $cacheFilePath
  }else{
    <# 
        TODO: Load cache from file
    #>  
    Write-Host "loading cache from file"
    $cacheContents = (Get-Content -Path $cacheFilePath )
    $copyCache = $cacheContents | Out-String | ConvertFrom-Json
    #Write-Host $copyCache.sources
  }


Write-Host "Cache File: " + $cacheFilePath
Write-Host "Log File: " + $logFilePath
#$copyCache = ConvertFrom-Json -InputObject $cacheContents

$headers = @{"Authorization"="Bearer "+$token}
$t = get-date -format yyyyMMddHHmmssfff
if(!(Test-Path $CSVFilePath)){
    Write-Host $CSVFilePath
	Write-Host "There was no csv file.  I won't do anything"
    $output = "`r`n " + $t +":: There was no CSV file.  I won't do anything"
	Add-Content -Path $logFilePath -Value $output
}else{    
	Import-Csv $CSVFilePath |foreach {
	  <# TODO: If course::destination is in the cache, don't do it #>
	  # Check $obj.sources contains $_.source_id

	  
	  $source_id = ""+$_.$source_course_id_column
	  if($copyCache.sources -eq $null){
	    $copyCache.Add("sources",@{$source_id=@()})
	  }
	  if($copyCache.sources.$source_id -lt 1){
	    $copyCache.sources | Add-Member -MemberType NoteProperty -Name $source_id -Value New-Object #System.Collections.ArrayList
	  }
	  
	  if(!($copyCache.sources.$source_id -contains $_.destination_id)){
	    $uri = "https://"+$domain+"/api/v1/courses/" + $_.destination_id + "/course_copy?source_course=" + $_.$source_course_id_column
	    Write-Host $uri
	  
	    $result = Invoke-RestMethod -Method POST -uri $uri -Headers $headers

	    #Write-Host $result
	    $output = "`r`n" + $result
	    Add-Content -Path $logFilePath -Value $output
	    $copyCache.sources.$source_id +=$_.$destination_course_id_column
	  }
	  
	}

	# TODO Write out the json cache again
	$copyCache | ConvertTo-Json | Set-Content -Path $cacheFilePath


	$processed_path = $archivePath+$t+"."+$CSVFileName+".processed"
    #Move-Item $CSVFilePath $processed_path
}


