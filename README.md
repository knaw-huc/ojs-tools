# OJS tools

This project contains multiple tools that help generate OJS native XML files.

## Getting Started

### Create the Conda environment
```bash
conda env create -f environment.yaml
```

### Activate the Conda environment
```bash
conda activate ojs-tools
```

## Pipeline
```
┌───────────┐    ┌─────────────┐    ┌────────────────┐    ┌────────────────────┐    ┌────────────────┐
│source data├───►│csv processor├───►│intermediate.csv├───►│ojs_xml_processor.py├───►│ojs native xml's│
└───────────┘    └─────────────┘    └────────────────┘    └────────────────────┘    └────────────────┘
```
* The `source data` can be in any format.
* The `CSV processor` converts the data into the `intermediate.csv` format.
* `ojs_xml_processor.py` converts `intermediate.csv` into multiple OJS native XML files—one per issue.

## CSV Processors

Custom CSV processors are needed for each archive. The output must be validated by `output_csv_validator.py`.

### `tvho_csv_processor.py`

This is a custom CSV processor for the TVHO project. It generates input for `ojs-xml-generator`.

#### Typical Call
```bash
python tvho_csv_processor.py --input_csv /path/to/input.csv --output_csv /path/to/output.csv --files_path /path/to/documents
```
* `--files_path` points to a directory containing the files listed in the input CSV.

> ⚠️ Opening the output in spreadsheet tools (e.g., Excel) might alter its contents and cause errors during XML generation.

## `output_csv_validator.py`

Ensures that the CSV output conforms to the required schema.

### Typical Call
```bash
python output_csv_validator.py --csv /path/to/data.csv
```

### Explanation of `intermediate.csv` Fields

| Field  | Description | Required? |
|--------|-------------|-----------|
| id | Numeric ID | Yes |
| title | Article title | Yes |
| publication | Issue title (if applicable) | Yes |
| abstract | Article abstract | Yes |
| file | Full path or Base64-encoded content of the file | Yes |
| publication_date | `YYYY-MM-DD` format | Yes |
| volume | Volume number | Yes |
| year | Year of publication | Yes |
| issue | Issue number (as a string) | Yes |
| page_number | Page numbers | Yes |
| section_title | Title of the section | Yes |
| section_policy | Section policy (internal use) | Yes |
| section_reference | Short section code (internal use) | Yes |
| doi | DOI (if available) | No |
| keywords | Keywords (semicolon-separated with `[;sep;]`) | No |
| author_given_name_x | Author first name (starts at 0) | Yes |
| author_family_name_x | Author last name (starts at 0) | Yes |
| author_affiliation_x | Author affiliation | No |
| author_email_x | Author email | No |
| author_country_x | Author country code (ISO 3166) | No |

## `ojs-xml-generator.py`

Generates self-contained XML files for the OJS NativeImportExportPlugin.

### Typical Call
```bash
python ojs-xml-generator.py \
  --csv_file /path/to/data.csv \
  --output_path /path/to/output/folder \
  --journal_name "Journal Full Name"
```

### Optional Parameters

| Parameter | Description | Default |
|----------|-------------|---------|
| `--author_group` | OJS user group (localized: `Author` / `Auteur`) | `Author` |
| `--submission_file_genre` | File genre (localized: `Article Text` / `Artikeltekst`) | `Article Text` |
| `--locale` | Locale used in XML (`en`, `nl`, etc.) | `en` |
| `--file_input` | Input mode for files: `file_path` or `base64` | `file_path` |

#### Example for Dutch:
```bash
python ojs-xml-generator.py \
  --csv_file /path/to/data.csv \
  --output_path /path/to/output/folder \
  --journal_name "Journal Name" \
  --author_group Auteur \
  --submission_file_genre Artikeltekst \
  --locale nl \
  --file_input base64
```

## `ojs_import.sh`

Uploads XML files to OJS.

> 📍 Place the script in the root directory of your OJS installation.

### Typical Call
```bash
./ojs_import.sh /path/to/xmls journal_path
```
* `/path/to/xmls` contains the generated OJS XML files.
* `journal_path` is the OJS-configured journal path.
