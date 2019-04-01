import unicodecsv
from .base import ImporterBase


class CSVImporter(ImporterBase):
    name = 'csv'
    name_verbose = 'CSV'

    def load(self, *args, **kwargs):
        rows = list()

        with open(self._arguments.csv_file, 'rb') as file_object_csv:
            reader = unicodecsv.DictReader(file_object_csv)

            for row in reader:
                rows.append(row)

        return rows

    @classmethod
    def add_subparser(cls, subparsers):
        subparser_csv = subparsers.add_parser(cls.name)
        subparser_csv.add_argument(
            '--csv-file'
            , help='path of csv file'
            , action='store'
        )
