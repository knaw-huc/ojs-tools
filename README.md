# OJS CSV processor

Creates CSV-files for `ojs-xml-generator`.

## Getting started
```commandline
conda env create -f environment.yaml
```

## How to use

Before the first call
```commandline
conda activate ojs-csv-processor
```

Typical call
```commandline
python tvho_csv_processor.py --input_csv /path/to/input.csv --output_csv /path/to/output.csv
```