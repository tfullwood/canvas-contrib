<#
 You will need to edit several variables here at the top of this script. 
 $token = the access token from Canvas
 $workingPath = the full working path to where the csv files are created.  
    This is where the logs and archive folders will be created
 $CSVFileName = the name of course copy CSV file as it will be created in
    the $workingPath.
 $domain = the full domain name you use to access canvas. (i.e. something.instructure.com)
#>

$token = "<token_here>" # access_token
$workingPath = "C:\Users\kevinh\Desktop\CanvasImport\"; # Important! Make sure this ends with a backslash
$CSVFileName = "canvas.templates.csv" # The name of the course copy CSV file.  Not the full path
$domain = "yourdomain.test.instructure.com"


# These are good defaults if you base your file on the example file
$source_course_id_column = "source_id"
$destination_course_id_column = "destination_id"

$move_csv_file_to_archive = $false; # change this to $true if you want to move the CSV
                                    # file after the copy is completed

<# ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
    Don't edit anything past here unless you know what you are doing.  
    NOTE: No offense, you probably do know what you're doing.  This is for those that don't.  
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
   new-item -Path $logFilePath ¿itemtype file
  }
 
if(!(Test-Path -Path $cacheFilePath))
  {
   new-item -Path $cacheFilePath ¿itemtype file
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
  if($copyCache.sources -eq $null){
	    #$copyCache.Add("sources",@{$source_id=@()})
      $copyCache | Add-Member -MemberType NoteProperty -Name "sources" -Value (@())
	}
  if($copyCache.all_list -eq $nul1){
      #$copyCache.Add("all_list",@())
      $copyCache | Add-Member -MemberType NoteProperty -Name "all_list" -Value (@())
  }
	Import-Csv $CSVFilePath |foreach {
	  <# If course::destination is in the cache, don't do it #>
	  # Check $obj.sources contains $_.source_id

	  
	  $source_id = ""+$_.$source_course_id_column
    $destination_id = ""+$_.$destination_course_id_column

    # Question: Does it matter if this course already copied from another course?  Maybe
    # it should never receive an automated copy after the first copy.
	  
    
    if($copyCache.sources.$source_id -lt 1){
	    $copyCache.sources | Add-Member -MemberType NoteProperty -Name $source_id -Value (@())
	  }
    
	  
	  if(($copyCache.sources.$source_id -contains $destination_id) -or ($copyCache.all_list -contains $destination_id)){
      # Don't do the course copy, this course has already had a copy applied to it
      # via some automated script.
      Write-Host "I'm not doing the course copy for $destination_id from $source_id because this course has already received a copy."
    
    }else{
	    $uri = "https://"+$domain+"/api/v1/courses/" + $destination_id + "/course_copy?source_course=" + $source_id
	    Write-Host $uri
	  
	    $result = Invoke-RestMethod -Method POST -uri $uri -Headers $headers

	    #Write-Host $result
	    $output = "`r`n" + $result
	    Add-Content -Path $logFilePath -Value $output
        
	    # The following line is broken, not sure why
      # If someone figures out why please fix and submit the change
      # The script will run without it
      # $copyCache.sources.$source_id += $destination_id
      $copyCache.all_list += $destination_id
	  }
	  
	}

	# TODO Write out the json cache again
	$copyCache | ConvertTo-Json | Set-Content -Path $cacheFilePath

	$processed_path = $archivePath+$t+"."+$CSVFileName+".processed"
  if ($move_csv_file_to_archive -eq $true){
    Move-Item $CSVFilePath $processed_path
  }
}
