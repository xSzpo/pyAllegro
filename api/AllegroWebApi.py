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
from suds.client import Client
import hashlib
import base64
import webbrowser


os.chdir('/Users/xszpo/Google Drive/DataScience/Projects/201808_allegro')


class AllegroWebApi():
    """
    https://developer.allegro.pl/auth/
    """

    def __init__(self,
                 credentialsFilePath='../credentials/credentials.json',
                 appNameField='nazwaAplikacji',
                 clientIdField='clientId',
                 clientSecredField='clientSecred',
                 redirectField='redirect',
                 appPasswordFiels='appPassword'
                 ):
        self.credentialsFilePath = credentialsFilePath
        self.Credentials = self.__load_credentials(self.credentialsFilePath)
        self.appName = self.Credentials[appNameField]
        self.clientId = self.Credentials[clientIdField]
        self.clientSecred = self.Credentials[clientSecredField]
        self.redirect = self.Credentials[redirectField]
        self.appPassword = self.Credentials[appPasswordFiels]

    def __load_credentials(self, file_path: str = 'credentials.json'):
        try:
            assert os.path.exists(file_path)
            with open(file_path, 'r') as file:
                credentials = file.readlines()

            credentials = json.loads(" ".join(credentials))
            return credentials

        except AssertionError:
            raise Exception('Path {} doesn\'exist'.format(
                                                self.credentialsFilePath))

        except Exception as e:
            print(e)
            raise

    def __create_login_link(self):
        return "https://allegro.pl/auth/oauth/authorize?response_type=" + \
                "code&client_id={clientId}&redirect_uri={redirectUri}".format(
                        **{
                            "clientId": self.clientId,
                            "redirectUri": self.redirect
                        })

    def web_api_start_sesion(self):
        self.Client = Client(
                'https://webapi.allegro.pl/service.php?wsdl')
        self.Response = self.Client.service.doQueryAllSysStatus(
                webapiKey=self.clientId, countryId=1)
        self.Version_key = self.Response.item[0].verKey
        self.Sha256_application_password = hashlib.sha256(
                self.appPassword.encode('utf-8')).digest()

        self.Auth = self.Client.service.doLoginEnc(
            userLogin='nicke1',
            userHashPassword=base64.b64encode(
                    self.Sha256_application_password).decode('utf-8'),
            countryCode=1,
            webapiKey=self.clientId,
            localVersion=self.Version_key
        )

        self.Session = self.Auth.sessionHandlePart
        pass

    def web_api_help(self):
        return webbrowser.open('https://allegro.pl/webapi/documentation.php')

    def doGetMyData(self):
        return self.Client.service.doGetMyData(sessionHandle=self.Session)

    def doGetUserID(self, userLogin: str, countryId: int = 1):
        return self.Client.service.doGetUserID(
                countryId=countryId,
                userLogin=userLogin,
                userEmail='',
                webapiKey=self.clientId
                )

    def doGetUserLogin(self, userId: int, countryId: int = 1):
        return self.Client.service.doGetUserLogin(
                countryId=countryId,
                userId=userId,
                webapiKey=self.clientId
                )

    def doShowUser(self, userId: int = 0, userLogin: str = '',
                   countryId: int = 1):
        if userId != 0 and userLogin == '':
            return self.Client.service.doShowUser(
                    countryId=countryId,
                    userId=userId,
                    webapiKey=self.clientId
                    )
        elif userId == 0 and userLogin != '':
            return self.Client.service.doShowUser(
                    countryId=countryId,
                    userLogin=userLogin,
                    webapiKey=self.clientId
                    )
        elif userId == 0 and userLogin == '':
            return self.Client.service.doShowUser(
                    countryId=countryId,
                    userLogin=userLogin,
                    webapiKey=self.clientId
                    )
        else:
            raise Exception('You should provide userId or userLogin')

"""
WebApi.web_api_start_sesion()
WebApi.doGetMyData()
WebApi.doGetUserID(userLogin='nicke1')
WebApi.doGetUserLogin(userId=1091465)
WebApi.doShowUser(userLogin='wwwprogres24pl')
"""