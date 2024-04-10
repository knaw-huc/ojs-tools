# OJS tools

This project contains multiple tools that help generate OJS native xml files.

## Getting started

### Create the conda environment
```commandline
conda env create -f environment.yaml
```

### Activate the conda environment
```commandline
conda activate ojs-tools
```

## TVHO CSV processor

Is a custom csv processor for the tvho project.
It will create input for `ojs-xml-generator`.

### Typical calls
```commandline
python tvho_csv_processor.py --input_csv /path/to/input.csv --output_csv /path/to/output.csv --files_path /path/to/documents
```
* `files_path`, a folder that should contain all the files mentioned in the `csv_file`-file.

Opening the output of this processor might alter its contents, causing errors when using the 'OJS XML Generator'.

## OJS XML Generator

Creates XML-files for the OJS `NativeImportExportPlugin`.
The XML-files are self-contained.

### Typical call
```commandline
python ojs-xml-generator.py --csv_file /path/to/data.csv --output_path /path/to/output/folder --journal_name "name of journal"
```
* `csv_file` should be in the structure created by `ojs-csv-processor`.
* `output_path` should point an existing folder.
* `journal_name` is included in the XML as '<title>' element and should be the full title of the journal.
This is where the XMLs are stored.
Optional parameters
* `author_group` describes the group within the system the authors of the articles are part of.
This property has a default value `Author`.
This default value is the English variant each language has its own.
The Dutch variant is `Auteur`.
* `submission_file_genre` is used for the `genre`-field of the `submission_file`-element
The default value is `Article Text`, the English variant.
The Dutch variant is `Artikeltekst`.
* `locale` the locale used when importing, default value is 'en'.
Make sure the `locale`, `author_group` and `submission_file_genre` are the same language.

A call for a Dutch-language journal would then look like this:
```commandline
python ojs-xml-generator.py --csv_file /path/to/data.csv --output_path /path/to/output/folder --journal_name "name of journal" --author_group Auteur --submission_file_genre Artikeltekst --locale nl
```

