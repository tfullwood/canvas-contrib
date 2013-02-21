#!/bin/bash

# Edit the following variables
access_token="put_your_token_here" # Change this to your access token
account_id=26 # Change this to your account ID
domain="cwt" # Change this to your account subdomain (i.e. cwt for cwt.instructure.com)
SOURCE_FOLDER=""
if [ $SOURCE_FOLDER="" ]; then
  SOURCE_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/csv"
fi


# 
# Stop.  Don't edit anything after here unless you know what you are doing

if [ $# -lt 1 ] ; then
  echo "You must specify at least 1 argument."
  echo "-e production|test|beta"
  exit 1
fi

while getopts e:h: opt
do
  case "$opt" in
    e) domain=$domain.$OPTARG;;
    h) usage;;
  esac
done

#SOURCE_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/csv"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# This creates a zip file with all the .csv files in the source folder
_date=`date "+%Y-%m-%d_%H-%M-%S"`

#echo $_date

zip_file="$SOURCE_FOLDER/$_date.zip"

zip -q "$zip_file" "$SOURCE_FOLDER/new/"*.csv

# make a folder for this run
mkdir "$SOURCE_FOLDER/archive/$_date/"

#mv the *.csv files into a folder for this time and day
mv "$SOURCE_FOLDER/new/"*.csv "$SOURCE_FOLDER/archive/$_date/"

txt=`curl -s -F attachment=@"$zip_file" -F "extension=zip" -F "import_type=instructure_csv" -H "Authorization: Bearer $access_token" "https://$domain.instructure.com/api/v1/accounts/$account_id/sis_imports.json"`

function jsonval {
    temp=`echo $json | sed 's/\\\\\//\//g' | sed 's/[{}]//g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' | grep -w $prop`
    echo ${temp##*|}
}

json="$txt"
prop='id'
id=`jsonval`
id=`echo $id | sed 's/id://'`
echo "results.id: "  "$id"
prop='workflow_state'
workflow_state=`jsonval`
prop='progress'
progress=`jsonval`

#echo $workflow_state
while [[ $workflow_state != "imported" && $workflow_state != "imported_with_messages" ]]; do
  echo "https://$domain.instructure.com/api/v1/accounts/$account_id/sis_imports/$id"
  json=`curl -s -H "Authorization: Bearer $access_token" "https://$domain.instructure.com/api/v1/accounts/$account_id/sis_imports/$id"`
  #echo $json
  prop='workflow_state'
  workflow_state=`jsonval`
  echo "workflow_state: $workflow_state"
done

# Move the zip file to the archive folder
mv "$zip_file" "$SOURCE_FOLDER/archive/$_date/$_date.zip"
