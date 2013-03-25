#!/bin/bash

# Edit the following variables
access_token="<put_your_token_here>" # Change this to your access token
account_id="<account_id>" # Change this to your account ID
domain="<domain_here>" # Change this to your account subdomain (i.e. cwt for cwt.instructure.com)
SOURCE_FOLDER="/path/to/source_folder"
path_to_python_parser=""

############################################################################# 
#### Stop.  Don't edit anything after here unless you know what you are doing
############################################################################# 

# TODO do we need a way to detect python, and optionally python versions?  If we 
# do that, then we can write out the python script and use it.  If python doesn't exist
# then we need another option.  (ruby, perl, etc?)

CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ -e "$CUR_DIR/localconfig.sh" ]];then
  . "$CUR_DIR/localconfig.sh"
fi

DIVIDER_START="#############################################################"
DIVIDER="-------------------------------------------------------------"

# Specify at least one argument
if [ $# -lt 1 ] ; then
  echo "You must specify at least 1 argument."
  echo "-e production|test|beta"
  exit 1
fi

echo $DIVIDER_START
echo "Starting the SIS import with the following variables:"
echo " domain:$domain"
echo " SOURCE_FOLDER:$SOURCE_FOLDER"
echo " path_to_python_parser:$path_to_python_parser"

if [ "$path_to_python_parser" = "" ]; then
  echo $DIVIDER 
  echo "You're not using the python json processor.  It's ok, " 
  echo "I just recommend you looking at your system to determine " 
  echo "if it would be possible.  All you need is Python 2.6 or higher."
  #path_to_python_parser="$CUR_DIR/python_parser.py"
fi
# If $SOURCE_FOLDER is blank, then use the current directory
if [ "$SOURCE_FOLDER" = "" ]; then
  echo $DIVIDER 
  echo "SOURCE_FOLDER was blank"
  SOURCE_FOLDER="$CUR_DIR/csv"
fi



while getopts e:h: opt
do
  case "$opt" in
    e) if [ $OPTARG != "production" ]; then domain=$domain.$OPTARG; fi;;
    h) usage;;
  esac
done


# This creates a zip file with all the .csv files in the source folder
_date=`date "+%Y-%m-%d_%H-%M-%S"`

zip_file="$SOURCE_FOLDER/$_date.zip"

# If there are no CSV files to process, exit the script
if [ ! -e "$SOURCE_FOLDER/new/"*.csv ]; 
then 
  echo $DIVIDER
  echo 'There are no csv files in $SOURCE_FOLDER/new/'; 
  exit 1
fi

echo "creating $zip_file with $SOURCE_FOLDER/new/*.csv"
zip -q "$zip_file" "$SOURCE_FOLDER/new/"*.csv

# make a folder for this run
echo "creating a folder for this import at $SOURCE_FOLDER/archive/$_date/"
mkdir -p "$SOURCE_FOLDER/archive/$_date/"

#echo $json

# Bash function to pull out a json value.  This function is VERY tempermental.  If you
# can, use the python parser.  It works with Python >= 2.6
function bashjsonval {
  temp=`echo $json | sed 's/\\\\\//\//g' | sed 's/[{}]//g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' | grep -w $prop`
  echo ${temp##*|}
}

jsonval () {
  # -r makes the read function disable interpretation of backslashes and whatnot. It had
  # me stuck for several minutes until I found that
  read -r json_string

  if [ "$path_to_python_parser" = "" ]; then
    prop=$1
    local myresult=`bashjsonval`
    #echo "myresult $myresult"
    #exit 1
    #if [ "$prop" = "id" ]; then
    myresult=`echo $myresult | sed "s/$prop://"`
  else
    local myresult=`echo $json_string | "$path_to_python_parser" $1`
  fi
  echo $myresult
}

echo $DIVIDER
echo "Starting the import...now"
json=`curl -s -F attachment=@"$zip_file" -F "extension=zip" -F "import_type=instructure_csv" -H "Authorization: Bearer $access_token" "https://$domain.instructure.com/api/v1/accounts/$account_id/sis_imports.json"`

id=$(echo $json | jsonval id) 
echo $DIVIDER
echo "SIS Import ID: "  "$id"
# Do a check on the ID.  It should be a number, if it isn't then stop the script now
# before anything else happens
if [ -z "${id##*[!0-9]*}" ]; then
  echo "Something was wrong with the initial sis import...stopping now"
  echo $json
  exit 1
else
  #mv the *.csv files into a folder for this time and day
  echo "Initial import was successfull, moving $SOURCE_FOLDER/new/"*.csv to "$SOURCE_FOLDER/archive/$_date/"
  mv "$SOURCE_FOLDER/new/"*.csv "$SOURCE_FOLDER/archive/$_date/"
fi
workflow_state=$(echo $json | jsonval workflow_state) 
progress=$(echo $json | jsonval progress) 

#echo $workflow_state
echo "checking status at https://$domain.instructure.com/api/v1/accounts/$account_id/sis_imports/$id"
while [[ $progress -lt 100 && $workflow_state != "imported" ]]; do
  sleep 3
  json=`curl -s -H "Authorization: Bearer $access_token" "https://$domain.instructure.com/api/v1/accounts/$account_id/sis_imports/$id"`
  #$json = $(echo $json | sed 's/\\/\\\\/g')
  workflow_state=$(echo $json | jsonval workflow_state) 
  progress=$(echo $json | jsonval progress) 
  echo "$workflow_state, $progress%"
done

echo $DIVIDER
echo "Results are in"
echo "The final Workflow State for this import is \"$workflow_state\""
if [[ $workflow_state = "imported_with_errors" ]];
then
  echo "Here are the errors"
  errors=$(echo $json | jsonval errors) 
  # For some reason this is truncated when not using the python processor.  Why, I don't know.  let's just print
  # out the full $json for now
  if [ "$path_to_python_parser" = "" ]; then
    echo $json
  else
    echo $errors
  fi

fi
if [[ $workflow_state = "imported_with_messages" ]];
then
  echo "Here are the messages"
  messages=$(echo $json | jsonval processing_warnings) 
  # For some reason this is truncated when not using the python processor.  Why, I don't know.  let's just print
  # out the full $json for now
  if [ "$path_to_python_parser" = "" ]; then
    echo $json
  else
    echo "warning messages: $messages"
  fi
fi

# Move the zip file to the archive folder
echo $DIVIDER
echo "All done, now moving $zip_file to $SOURCE_FOLDER/archive/$_date/$_date.zip"
mv "$zip_file" "$SOURCE_FOLDER/archive/$_date/$_date.zip"
