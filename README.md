# OJS XML Generator

Creates XML-files for the OJS `NativeImportExportPlugin`.
It uses the csv-files created by `ojs-csv-processor`.
The XML-files are self-contained.

## Getting started

```commandline
conda create -f environment.yaml
```

## How to use

Before the first call
```commandline
conda activate ojs-xml-generator
```

Typical call
```commandline

python main.py --csv_file /path/to/data.csv --files_path /path/to/documents --output_path /path/to/output/folder 
```
`csv_file` should be in the structure created by `ojs-csv-processor`.
`files_path`, a folder that should contain all the files mentioned in the `csv_file`-file.
`output_path` should point an existing folder.
This is where the XMLs are stored.