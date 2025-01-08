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

## Pipeline
```
┌───────────┐    ┌─────────────┐    ┌────────────────┐    ┌────────────────────┐    ┌────────────────┐
│source data├───►│csv processor├───►│intermediate.csv├───►│ojs_xml_processor.py├───►│ojs native xml's│
└───────────┘    └─────────────┘    └────────────────┘    └────────────────────┘    └────────────────┘
```
* The `source data` can be in every format.
* The `CSV processor` should convert the data to the `intermediate.csv`-format.
* The `ojs_xml_processor.py` will process the intermediate-format to several `ojs native xml's`.
An xml-file is created for each issue described in the `intermediate.csv`.

## CSV processors
For each archive a custom CSV processor should be created. 
This processor should be found valid by `output_csv_validator.py`.

### `tvho_csv_processor.py`

Is a custom csv processor for the tvho project.
It will create input for `ojs-xml-generator`.

#### Typical call
```commandline
python tvho_csv_processor.py --input_csv /path/to/input.csv --output_csv /path/to/output.csv --files_path /path/to/documents
```
* `files_path`, a folder that should contain all the files mentioned in the `csv_file`-file.

Opening the output of this processor might alter its contents, causing errors when using the 'OJS XML Generator'.

## `output_csv_validator.py`
Makes sure the output from CSV processors complies to all the requirements of the OJS XML Generator.
It contains a method `validate_csv` that can be used in your CSV processor.

### Typical call
```commandline
python output_csv_validator.py --csv /path/to/data.csv
```

### Explanation of intermediate CSV fields
| Field  | Contents  | Required?  |
|---|---|---|
| id  | A numberical ID, from 1 to X  | Yes  |
| title  | The title of the article  | Yes  |
| publication | The title of the issue, if it has one (e.g. themed issues) | Yes |
| abstract  | The abstract of the article  | Yes  |
| file  | A full path to the file corresponding with the article text  | Yes  |
| publication_date  | the date of publication, structured as yyyy-mm-dd | Yes  |
| volume  | the volume number | Yes  |
| year  | year of the issue  | Yes  |
| issue  | the issue number, as a string  | Yes  |
| page_number  |  the page numbers | Yes  |
| section_title  | the title of the section  | Yes  |
| section_policy  | the section policy (won't be shown)  | Yes  |
| section_reference  |  the short code for the section (won't be shown, but should be the same for every instance of section title x) | Yes  |
| doi  |  the full DOI | no  |
| author_given_name_x  | first name of the author. Make sure they're empty if there is no author x. Starts at 0. | Yes  |
| author_family_name_x | last name of the author. Make sure they're empty if there is no author x. Starts at 0. | Yes  |

## `ojs-xml-generator.py` 

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


## `ojs_import.sh`
Uploads the xml's to a journal. 
Place the script in the root-folder of your OJS installation.

### Typical call
```commandline
./ojs_import.sh /path/to/folder/of/xmls path_of_journal
```
* `/path/to/folder/of/xmls` contains the OJS native xml files.
* `path_of_journal` the path property of the magazine configured in OJS.


