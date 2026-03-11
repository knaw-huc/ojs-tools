# OJS Native XML Generator

A toolkit for batch-importing article metadata into **OJS 3.4** using the NativeImportExportPlugin. It converts article metadata from a standardized CSV into OJS-compatible XML files — one per issue — making it well-suited for archive migrations, back-issue imports, or any large-scale content ingestion.

## Overview

The pipeline works in three stages:

```
┌───────────┐    ┌─────────────┐    ┌────────────────┐    ┌────────────────────┐    ┌────────────────┐
│source data├───►│csv processor├───►│intermediate.csv├───►│ojs_xml_processor.py├───►│ojs native xml's│
└───────────┘    └─────────────┘    └────────────────┘    └────────────────────┘    └────────────────┘
```

1. Your source data (in any format) is converted into a standardized intermediate CSV.
2. The intermediate CSV is validated against the required schema.
3. The validated CSV is converted into OJS-ready XML files, one per issue.

## Getting Started

### Create and activate the Conda environment

```bash
conda env create -f environment.yaml
conda activate ojs-tools
```

---

## Step 1 — Prepare Your CSV

### Intermediate CSV format

The core of the pipeline is a semicolon-delimited CSV file conforming to the schema below. You can produce this file however suits your data — from a spreadsheet export, a database query, or a custom script.

> ⚠️ If you use one of the included processor: Do not open or save the CSV in spreadsheet software (e.g., Excel) after it has been generated. This can silently alter delimiters, encodings, and special characters, causing errors during XML generation.

### Field reference

| Field | Description | Required? |
|-------|-------------|-----------|
| `id` | Numeric ID | Yes |
| `title` | Article title | Yes |
| `publication` | Issue title (if applicable) | Yes |
| `abstract` | Article abstract | Yes |
| `file` | Full path or Base64-encoded content of the article file | Yes |
| `publication_date` | `YYYY-MM-DD` format | Yes |
| `volume` | Volume number | Yes |
| `year` | Year of publication | Yes |
| `issue` | Issue number (as a string) | Yes |
| `page_number` | Page numbers | Yes |
| `section_title` | Title of the section | Yes |
| `section_policy` | Section policy (used internally by OJS) | Yes |
| `section_reference` | Short section code (used internally by OJS) | Yes |
| `doi` | DOI, if available | No |
| `keywords` | Semicolon-separated keywords using `[;sep;]` as delimiter | No |
| `author_given_name_x` | Author first name (zero-indexed, e.g. `author_given_name_0`) | Yes |
| `author_family_name_x` | Author last name | Yes |
| `author_affiliation_x` | Author institutional affiliation | No |
| `author_email_x` | Author email address | No |
| `author_country_x` | Author country code (ISO 3166) | No |

Multiple authors are supported by incrementing the `_x` suffix (`_0`, `_1`, `_2`, …).

### Sample CSV

```
id;title;publication;abstract;file;publication_date;volume;year;issue;page_number;section_title;section_policy;section_reference;doi;keywords;author_given_name_0;author_family_name_0;author_affiliation_0;author_email_0;author_country_0;author_given_name_1;author_family_name_1;author_affiliation_1;author_email_1;author_country_1
1;"Machine Learning Applications in Healthcare Diagnostics";"Journal of Medical Informatics";"This study explores the implementation of machine learning algorithms for early disease detection in clinical settings.";"./articles/ml_healthcare_2024.pdf";"2024-03-15";45;2024;3;"123-145";"Research Articles";"peer-reviewed";"RA";"10.1016/j.jmedinf.2024.03.015";"machine learning[;sep;]healthcare[;sep;]diagnostics";"Sarah";"Johnson";"Stanford University Medical Center";"s.johnson@stanford.edu";"US";"Michael";"Chen";"MIT Computer Science Lab";"m.chen@mit.edu";"US"
```

### Writing a custom CSV processor

If your source data is not already in the intermediate format, you will need to write a script to convert it. The output must pass validation (see Step 2) before proceeding.

A reference implementation is included in `tvho_csv_processor.py`, which you can use as a starting point and adapt to your own data structure.

---

## Step 2 — Validate Your CSV

Before generating XML, run the validator to confirm your CSV conforms to the required schema:

```bash
python output_csv_validator.py --csv /path/to/data.csv
```

Fix any reported errors before continuing. Common issues include missing required fields, incorrectly formatted dates, and malformed author columns.

---

## Step 3 — Generate OJS XML

```bash
python ojs-xml-generator.py --csv_file /path/to/data.csv --output_path /path/to/output/folder --journal_name "Your Journal Name"
```

This produces one XML file per issue in the output folder, ready for import via OJS's NativeImportExportPlugin.

### Optional parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--author_group` | OJS user group label for authors (localize as needed, e.g. `Auteur`) | `Author` |
| `--submission_file_genre` | File genre label (localize as needed, e.g. `Artikeltekst`) | `Article Text` |
| `--locale` | Locale code used in the XML output | `en` |
| `--file_input` | How files are referenced: `file_path` or `base64` | `file_path` |

> 💡 The `--author_group` and `--submission_file_genre` values must match the labels configured in your OJS installation. If your OJS is set to a language other than English, check the OJS interface for the exact strings to use.

#### Example — Dutch locale with Base64-encoded files

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

---

## Step 4 — Import into OJS

Use `ojs_import.sh` to upload the generated XML files to your OJS installation. Alternatively, you can drag the generated XML into the ImportExport plugin screen in OJS yourself, negating the need to access the root folder.

> 📍 Place this script in the **root directory** of your OJS installation before running it.

```bash
./ojs_import.sh /path/to/xmls journal_path
```

- `/path/to/xmls` — the folder containing your generated XML files
- `journal_path` — the journal path as configured in OJS (found under **Settings → Journal → Masthead**)

---

## Notes on the default CSV delimiter

By default, `ojs-xml-generator.py` expects a **semicolon-delimited** CSV. If your data uses a different delimiter (e.g. a comma), this can be changed on line 302 of the script.
