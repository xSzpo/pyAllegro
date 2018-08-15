#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 16:03:18 2018

@author: xszpo
https://www.python.org/dev/peps/pep-0008/
* Use 4 spaces per indentation level
* Limit all lines to 72 characters, maximum of 79 characters.
* Imports should usually be on separate lines, always at the top of the file
* income = (gross_wages
           + taxable_interest
* Yes: spam(ham[1], {eggs: 2})
* Modules should have short, all-lowercase names. Underscores can be used
* Class names should normally use the CapWords convention
* Variables shuold CapWords preferring short names: T, AnyStr, Num
* Function names - lowercase, separated by underscores as necessary
* Constants - all capital letters

"""

import json
import os
import request
import webbrowser

os.chdir('/Users/xszpo/Google Drive/DataScience/Projects/201808_allegro')

os.path.exists('../credentials/credentials.json')

class Authorize():
    """
    https://developer.allegro.pl/auth/
    """

    def __init__(self,
                 credentialsFilePath='../credentials/credentials.json',
                 appNameField='nazwaAplikacji',
                 clientIdField='clientId',
                 clientSecredField='clientSecred',
                 redirectField='redirect'
                 ):
        self.credentialsFilePath = credentialsFilePath
        self.appNameField = appNameField
        self.clientIdField = clientIdField
        self.clientSecredField = clientSecredField
        self.redirectField = redirectField
        self.Credentials = self.__load_credentials(self.credentialsFilePath)

    def __load_credentials(self, file_path: str = 'credentials.json'):
        with open(file_path, 'r') as file:
            credentials = file.readlines()

        credentials = json.loads(" ".join(credentials))
        return credentials

    def __create_login_link(self):
        return "https://allegro.pl/auth/oauth/authorize?response_type=" + \
                "code&client_id={clientId}&redirect_uri={redirectUri}".format(
                        **{
                            "clientId": self.Credentials[self.clientIdField],
                            "redirectUri": self.Credentials[self.redirectField]
                        })

    def open_autorization_page(self):
        webbrowser.open(self.__create_login_link())
        self.autCode = input("wprowadz klucz: ")
        pass

Aut = Authorize()
Aut.open_autorization_page()





from oauth2client.client import OAuth2WebServerFlow


flow = OAuth2WebServerFlow(client_id=Aut.Credentials[Aut.clientIdField],
                           client_secret=Aut.Credentials[Aut.clientSecredField],
                           scope='https://www.googleapis.com/auth/calendar',
                           redirect_uri='http://example.com/auth_return')






#curl -X POST -H "Authorization: Basic YTI...Hg=" https://allegro.pl/auth/oauth/token?grant_type=authorization_code&code=pOPEy9Tq94aEss540azzC7xL6nCJDWto&redirect_uri=http://exemplary.redirect.uri
