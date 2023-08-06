# tablify-csv

![Build Status](https://github.com/ralphqq/tablify-csv/workflows/ralphqq-tablify-csv-ci/badge.svg)

CLI tool to convert data in a CSV file into an HTML table with basic formatting.

The tool lets you:

- Specify column headings to be displayed on the final HTML table
- Assign class names to any column (assign to `td` tags that fall under a given column)
- Save the output (prettified) HTML into a file and/or copy to clipboard

## Requirements
- [Python](https://www.python.org/downloads/release/python-380/) >= 3.8
- [lxml](https://lxml.de/) >= 4.5.2
- [prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) >= 3.0.6
- [pyperclip](https://pyperclip.readthedocs.io/en/latest/) >= 1.8.0
- [typer](https://github.com/tiangolo/typer-cli) >= 0.3.2

Please see `requirements.txt` and `dev-requirements.txt` for full list of dependencies.

## Installation
It's recommended to create and activate a virtual environment before installing.

For the latest stable release, install from [PyPI package](https://pypi.org/project/tablify-csv/) with `pip`:

```console
$ pip install tablify-csv
```

To install the latest development version, run the following:

```console
$ pip install git+https://github.com/ralphqq/tablify-csv
```

## Usage
Once installed, `tablify-csv` can now be used without any additional configuration required. If applicable, make sure that the virtual environment where you pip installed `tablify-csv` is activated.

### Valid CSV File
The current version of `tablify-csv` assumes the CSV file to be parsed has:

- A header row with the column names in the first line of the file
- No empty lines between the header row and the first data row (i.e., the first data row immediately follows the header row)

### Usage Examples
To convert a CSV file:

```console
$ tablify-csv CSV_FILENAME
```

This will save the HTML table in a file with the same name as the CSV file except the extension will be `.html`.

To specify a filename for the output file:

```console
$ tablify-csv CSV_FILENAME --output-file OUTPUT_FILENAME
```

To copy the resulting HTML table to the clipboard (without saving to an output file):

```console
$ tablify-csv CSV_FILENAME --clip
```

To copy the resulting HTML table to the clipboard and save it to an output file:

```console
$ tablify-csv CSV_FILENAME --output-file OUTPUT_FILENAME --clip
```

## Development Setup
1. Clone this repo at https://github.com/ralphqq/tablify-csv
2. Create and activate a virtual environment
3. Install the development dependencies:
    ```console
    $ pip install -r dev-requirements.txt
    ```
4. Run the test suite:
    ```console
    $ pytest
    ```

**Note:** To ensure coding style consistency, this project uses pre-commit hooks. You may also want to initialize pre-commits into your local development clone (this is strongly recommended if you want to contribute, see `Contributing` section).

```console
$ pre-commit install
```

## Contributing
1. Fork this repo at https://github.com/ralphqq/tablify-csv
2. Clone your fork into your local machine
3. Follow steps in Development Setup but skip step 1
4. Initialize pre-commit hooks
    ```console
    $ pre-commit install
    ```
5. Create your feature branch:
    ```console
    $ git checkout -b feature/some-new-thing
    ```
6. Commit your changes:
    ```console
    $ git commit -m "Develop new thing"
    ```
7. Push to the branch:
    ```console
    $ git push origin feature/some-new-thing
    ```
8. Create a pull request

## License
`tablify-csv` is available under the [MIT License](https://opensource.org/licenses/MIT).
