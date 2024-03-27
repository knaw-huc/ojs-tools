# OJS tools

## The tools
### OJS CSV processor

Creates CSV-files for `ojs-xml-generator`.

### OJS XML Generator

Creates XML-files for the OJS `NativeImportExportPlugin`.
It uses the csv-files created by `ojs-csv-processor`.
The XML-files are self-contained.

## Getting started

```commandline
conda env create -f environment.yaml
```

## How to use

#### Before the first call
```commandline
conda activate ojs-tools
```

### Typical calls
OJS CSV processor
```commandline
python tvho_csv_processor.py --input_csv /path/to/input.csv --output_csv /path/to/output.csv --files_path /path/to/documents
```
`files_path`, a folder that should contain all the files mentioned in the `csv_file`-file.

OJS XML Generator
```commandline
c```
`csv_file` should be in the structure created by `ojs-csv-processor`.
`output_path` should point an existing folder.
This is where the XMLs are stored.
Optional parameters
`author_group` the user the group the authors of the articles are part of.
This property has a default value `Author`.
This default value is the English variant each language has its own.
The Dutch variant is `Auteur`.
`submission_file_genre` is used for the `genre`-field of the `submission_file`-element
The default value is `Article Text`, the English variant.
The Dutch variant is `Artikeltekst`.
