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


from suds.client import Client
import hashlib
import base64
import webbrowser
import json
import os


class AllegroWebApi():
    """
    https://developer.allegro.pl/auth/
    """

    def __init__(self,
                 config_file_dir=os.path.join(
                         os.path.expanduser("~"), '.allegroApiConfig')
                 ):
        self.config_file_dir = config_file_dir

        """jezeli folder config nie istnieje - utworz go"""
        if not os.path.exists(config_file_dir):
            os.makedirs(config_file_dir)

        """jezeli folder config nie istnieje - zatrzymaj program"""
        if not os.path.exists(config_file_dir):
            raise AssertionError("directory {} does not exists".
                                 format(config_file_dir))

    def __credentials_read(self):
        with open(os.path.join(self.config_file_dir,
                               "allegro_credentials_webapi.json"), 'r') as file:
            self.Credentials = json.load(file)

        pass

    def __credentials_write(self):
        with open(os.path.join(self.config_file_dir,
                               "allegro_credentials_webapi.json"), 'w') \
                               as file:
            json.dump(self.Credentials, file)

        pass

    def credentials_set(self,
                        appName,
                        clientId,
                        clientSecred,
                        userLogin,
                        redirectUrl,
                        appPassword,
                        countryId=1):
        self.Credentials = {
                "appName": appName,
                "clientId": clientId,
                "clientSecred": clientSecred,
                "userLogin": userLogin,
                "redirectUrl": redirectUrl,
                "appPassword": appPassword,
                "countryId": countryId
                }

        self.__credentials_write()

        pass

    def __create_login_link(self):
        return "https://allegro.pl/auth/oauth/authorize?response_type=" + \
                "code&client_id={clientId}&redirect_uri={redirectUri}".format(
                        **{
                            "clientId": self.Credentials['clientId'],
                            "redirectUri": self.Credentials['redirectUrl']
                        })
        pass

    def start_sesion(self):
        if not hasattr(self, 'Credentials'):
            self.__credentials_read()

        self.Client = Client(
                'https://webapi.allegro.pl/service.php?wsdl')
        self.Response = self.Client.service.doQueryAllSysStatus(
                webapiKey=self.Credentials['clientId'],
                countryId=self.Credentials['countryId'])
        self.Version_key = self.Response.item[0].verKey
        self.Sha256_application_password = hashlib.sha256(
                self.Credentials['appPassword'].encode('utf-8')).digest()

        self.Auth = self.Client.service.doLoginEnc(
            userLogin=self.Credentials['userLogin'],
            userHashPassword=base64.b64encode(
                    self.Sha256_application_password).decode('utf-8'),
            countryCode=self.Credentials['countryId'],
            webapiKey=self.Credentials['clientId'],
            localVersion=self.Version_key
        )

        self.Session = self.Auth.sessionHandlePart
        pass

    def credentials_load(self):
        self.__credentials_read()

        pass

    def credentials_field_set(self, key, value, ifWriteToFile=True):

        self.Credentials[key] = value

        if ifWriteToFile:
            self.__credentials_write()

    def web_api_help(self):
        return webbrowser.open('https://allegro.pl/webapi/documentation.php')

    def client_service(self):
        return self.Client.service

    def doGetMyData(self):
        return self.Client.service.doGetMyData(sessionHandle=self.Session)

    def doGetUserID(self, userLogin: str, countryId: int = 1):
        return self.Client.service.doGetUserID(
                countryId=countryId,
                userLogin=userLogin,
                userEmail='',
                webapiKey=self.Credentials['clientId']
                )

    def doGetUserLogin(self, userId: int, countryId: int = 1):
        return self.Client.service.doGetUserLogin(
                countryId=countryId,
                userId=userId,
                webapiKey=self.Credentials['clientId']
                )

    def doShowUser(self, userId: int = 0, userLogin: str = '',
                   countryId: int = 1):
        if userId != 0 and userLogin == '':
            return self.Client.service.doShowUser(
                    countryId=countryId,
                    userId=userId,
                    webapiKey=self.Credentials['clientId']
                    )
        elif userId == 0 and userLogin != '':
            return self.Client.service.doShowUser(
                    countryId=countryId,
                    userLogin=userLogin,
                    webapiKey=self.Credentials['clientId']
                    )
        elif userId == 0 and userLogin == '':
            return self.Client.service.doShowUser(
                    countryId=countryId,
                    userLogin=userLogin,
                    webapiKey=self.Credentials['clientId']
                    )
        else:
            raise Exception('You should provide userId or userLogin')


'''
WebApi = AllegroWebApi()

WebApi.config_file_dir

#WebApi.credentials_set(
#        appName='<credentials from allegro>',
#        clientId='<credentials from allegro>',
#        clientSecred='<credentials from allegro>',
#        userLogin='<allegro login>',
#        redirectUrl='<redirect uri - the same you provided during app registration on allegro >',
#        appPassword='<app password>'
#        )


WebApi.start_sesion()
WebApi.doGetMyData()
WebApi.doGetUserID(userLogin='nicke1')
WebApi.doGetUserLogin(userId=1091465)
WebApi.doShowUser(userLogin='wwwprogres24pl')
'''
