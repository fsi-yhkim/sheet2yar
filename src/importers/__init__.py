from .csv import CSVImporter
from .google_spreadsheet import GoogleSpreadsheetImporter


__all__ = [
    'CSVImporter',
    'GoogleSpreadsheetImporter',
]

IMPORTER_CLASSES = dict()

for entry in __all__:
    klass = locals()[entry]    
    IMPORTER_CLASSES[klass.name] = klass
