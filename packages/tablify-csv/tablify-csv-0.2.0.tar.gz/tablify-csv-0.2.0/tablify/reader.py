"""
Classes and methods to handle reading and parsing the CSV file

Classes:
    CSVTableReader
"""
import csv


class CSVTableReader:
    """Handles reading and parsing of CSV file."""

    def __init__(self, csv_file: str) -> None:
        """Initializes CSVTable object and executes file reading.

        Args:
            csv_file (str): path to CSV file

        Raises:
            ValueError: if any errors are raised during reading/parsing
        """
        try:
            self.csv_file = csv_file
            self.data = self._get_csv_data()
            self.columns = list(self.data[0].keys())
        except Exception as e:
            raise ValueError(f"Error during CSV reading/parsing: {e}")

    def _get_csv_data(self) -> list:
        """Reads rows in CSV file and returns them as list of dicts."""
        data = []
        with open(self.csv_file, "r", encoding="utf-8") as fp:
            reader = csv.DictReader(fp)
            data = list(reader)

        if not data:
            raise ValueError("CSV file has no data")

        return data
