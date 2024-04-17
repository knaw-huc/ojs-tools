#!/bin/bash


if [[ -z $1 ]]; then
	echo "expected folder of xmls to import as first parameter"
	exit
fi

if [[ -z $2 ]]; then
	echo "expect path of journal as second parameter"
	exit
fi


files=$(find $1 -name "*.xml" | sort)

for xml in $files; do
	echo $xml
	php tools/importExport.php NativeImportExportPlugin import $xml $2
done
