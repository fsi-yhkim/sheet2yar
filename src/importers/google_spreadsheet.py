# coding: utf-8
import os
import argparse
from pprint import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from .base import ImporterBase


class GoogleSpreadsheetImporter(ImporterBase):
    name = 'google-spreadsheet'
    name_verbose = 'Google Spreadsheet'

    def __init__(self, arguments, *args, **kwargs):
        super().__init__(arguments, *args, **kwargs)

        if not os.path.exists(self._arguments.gs_credential_file):
            raise ValueError('service credential file required')

    def load(self, *args, **kwargs):
        credentials = service_account.Credentials.from_service_account_file(
            self._arguments.gs_credential_file
            , scopes=[
                'https://www.googleapis.com/auth/spreadsheets.readonly',
            ]
        )
        spreadsheets_service = build('sheets', 'v4', credentials=credentials)
        spreadsheets = spreadsheets_service.spreadsheets()
        response = spreadsheets.values().get(
            spreadsheetId=self._arguments.gs_id
            , range=self._arguments.gs_range
        ).execute()

        values = response.get('values', [])

        if not values:
            raise ValueError('Empty spreadsheet')
        
        rows = list()
        column_names = list()
        
        for idx, value in enumerate(values):
            if 0 == idx:
                column_names = value
                continue
            
            rows.append(
                dict(zip(column_names, value))
            )

        return rows

    @classmethod
    def add_subparser(cls, subparsers):
        argument_group_google_spreadsheet = subparsers.add_parser(cls.name)
        argument_group_google_spreadsheet.add_argument(
            '--gs-credential-file'
            , help='path of google api service credential file'
            , action='store'
            , default='./service_credential.json'
        )
        argument_group_google_spreadsheet.add_argument(
            '--gs-id'
            , help='id of spreadsheet'
            , required=True
        )
        argument_group_google_spreadsheet.add_argument(
            '--gs-range'
            , help='sheet\'s name / range of sheet'
            , required=True
        )
