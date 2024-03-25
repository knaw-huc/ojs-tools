# OJS XML Generator

Creates XML-files for the OJS `NativeImportExportPlugin`.
It uses the csv-files created by `ojs-csv-processor`.
The XML-files are self-contained.

## Getting started

```commandline
conda env create -f environment.yaml
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
Optional parameters
`author_group` the user the group the authors of the articles are part of.
This property has a default value `Author`.
This default value is the english variant each language has its own.
The dutch variant is `Auteur`.
`submission_file_genre` is used for the `genre`-field of the `submission_file`-element
The default value is `Article Text`, the english variant.
The dutch variant is `Artikeltekst`.