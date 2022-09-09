#!/usr/bin/env bash

FILE_NAME=AcoRecipes
FILE_TYPE="$1"
if [ -z "$1" ]; then
  { echo "usage: $0 <action>"
    echo "  e.g. $0 bacpac or dacpac"
  } >&2
  exit 1
fi

if [ $FILE_TYPE = "bacpac" ]; then
    ACTION=Export
elif [ $FILE_TYPE = "dacpac" ]; then
    ACTION=Extract
else
  { 
    echo "invalid action $0"
    echo "usage: $0 <action>"
    echo "  e.g. $0 bacpac or dacpac"
  } >&2
  exit 1
fi

echo $ACTION"ing to $FILE_NAME.$FILE_TYPE"

/opt/mssql-tools/sqlpackage/sqlpackage /Action:$ACTION /TargetFile:$FILE_NAME.$FILE_TYPE /SourceServerName:"." /SourceDatabaseName:"AcoRecipes"  /SourceUser:sa /SourcePassword:$SA_PASSWORD