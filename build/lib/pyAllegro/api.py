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

from datetime import datetime
from suds.client import Client
from suds.sudsobject import asdict
import hashlib
import base64
import webbrowser
import json
import os
import requests
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import webbrowser


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

    def __recursive_dict(self, d):
        out = {}
        for k, v in asdict(d).items():
            if hasattr(v, '__keylist__'):
                out[k] = self.__recursive_dict(v)
            elif isinstance(v, list):
                out[k] = []
                for item in v:
                    if hasattr(item, '__keylist__'):
                        out[k].append(self.__recursive_dict(item))
                    else:
                        out[k].append(item)
            else:
                out[k] = v
        return out

    def __myconverter(self, o):
        if isinstance(o, datetime):
            return o.__str__()
        
    def response2JSON(self, response):
        return json.loads(json.dumps(self.__recursive_dict(response), default = self.__myconverter))

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

class AllegroRestApi():
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
                               "allegro_credentials_rest.json"), 'r') as file:
            self.Credentials = json.load(file)

        pass

    def __credentials_write(self):
        with open(os.path.join(self.config_file_dir,
                               "allegro_credentials_rest.json"), 'w') as file:
            json.dump(self.Credentials, file)

        pass

    def __token_read(self):
        with open(os.path.join(self.config_file_dir,
                               "allegro_rest_token.json"), 'r') as file:
            self.Authorization = json.load(file)

        pass

    def __token_write(self):
        with open(os.path.join(self.config_file_dir,
                               "allegro_rest_token.json"), 'w') as file:
            json.dump(self.Authorization, file)

    def __get_access_code(self, client_id, redirect_uri, oauth_url):

        auth_url = '{}/authorize' \
                   '?response_type=code' \
                   '&client_id={}' \
                   '&redirect_uri={}'.format(oauth_url, client_id,
                                             redirect_uri)

        # uzywamy narzędzia z modułu requests - urlparse - służy do spardowania
        # podanego url (oddzieli hostname od portu)
        parsed_redirect_uri = requests.utils.urlparse(redirect_uri)

        # definiujemy nasz serwer - który obsłuży odpowiedź allegro
        # (redirect_uri)
        server_address = parsed_redirect_uri.hostname, parsed_redirect_uri.port

        # Ta klasa pomoże obsłużyć zdarzenie GET na naszym lokalnym serwerze
        # - odbierze żądanie (odpowiedź) z serwisu allegro
        class AllegroAuthHandler(BaseHTTPRequestHandler):
            def __init__(self, request, address, server):
                super().__init__(request, address, server)

            def do_GET(self):
                self.send_response(200, 'OK')
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                self.server.path = self.path
                self.server.access_code = self.path.rsplit('?code=', 1)[-1]

        # Wyświetli nam adres uruchomionego lokalnego serwera
        print('server_address:', server_address)

        # Uruchamiamy przeglądarkę, przechodząc na adres zdefiniowany do
        # uzyskania kodu dostępu wyświetlić się powinien formularz logowania
        # do serwisu Allegro.pl
        webbrowser.open(auth_url)

        # Uruchamiamy nasz lokalny web server na maszynie na której uruchomiony
        # zostanie skrypt taki serwer dostępny będzie pod adresem
        # http://localhost:8000 (server_address)
        httpd = HTTPServer(server_address, AllegroAuthHandler)
        print('Waiting for response with access_code from Allegro.pl '
              '(user authorization in progress)...')

        # Oczekujemy tylko jednego żądania
        httpd.handle_request()

        # Po jego otrzymaniu zamykamy nasz serwer
        # (nie obsługujemy już żadnych żądań)
        httpd.server_close()

        # Klasa HTTPServer przechowuje teraz nasz access_code - wyciągamy go
        _access_code = httpd.access_code

        # Dla jasności co się dzieje - wyświetlamy go na ekranie
        print('Got an authorize code')  # , _access_code

        # i zwracamy jako rezultat działania naszej funkcji
        return _access_code

    def __sign_in(self, client_id, client_secret, access_code, redirect_uri,
                  oauth_url):

        token_url = oauth_url + '/token'

        access_token_data = {'grant_type': 'authorization_code',
                             'code': access_code,
                             'redirect_uri': redirect_uri}

        response = requests.post(url=token_url,
                                 auth=requests.auth.HTTPBasicAuth(
                                         client_id, client_secret),
                                 data=access_token_data)

        return response.json()

    def __refresh_token(self, client_id, client_secret, refresh_token,
                        redirect_uri, oauth_url):

        token_url = oauth_url + '/token'

        access_token_data = {'grant_type': 'refresh_token',
                             'refresh_token': refresh_token,
                             'redirect_uri': redirect_uri}

        response = requests.post(url=token_url,
                                 auth=requests.auth.HTTPBasicAuth(
                                         client_id, client_secret),
                                 data=access_token_data)

        return response.json()

    def credentials_set(self,
                        appName,
                        clientId,
                        clientSecred,
                        redirectUrl="http://localhost:8000",
                        DEFAULT_OAUTH_URL="https://allegro.pl/auth/oauth",
                        DEFAULT_REDIRECT_URI="http://localhost:8000",
                        DEFAULT_API_URL="https://api.allegro.pl"
                        ):
        self.Credentials = {
                "appName": appName,
                "clientId": clientId,
                "clientSecred": clientSecred,
                "redirectUrl": redirectUrl,
                "DEFAULT_OAUTH_URL": DEFAULT_OAUTH_URL,
                "DEFAULT_REDIRECT_URI": DEFAULT_REDIRECT_URI,
                "DEFAULT_API_URL": DEFAULT_API_URL,
                }

        if self.Credentials["redirectUrl"] != self.Credentials["DEFAULT_"
                                                               "REDIRECT_URI"]:
            raise ValueError('redirectUrl sholud be the same as'
                             'DEFAULT_REDIRECT_URI')

        self.__credentials_write()

        pass

    def credentials_load(self):
        self.__credentials_read()

        pass

    def credentials_field_set(self, key, value, ifWriteToFile=True):

        self.Credentials[key] = value

        if ifWriteToFile:
            self.__credentials_write()

    def rest_api_help(self):
        return webbrowser.open('https://developer.allegro.pl/')

    def get_token(self, writeDownToken=True):

        if not hasattr(self, 'Credentials'):
            self.__credentials_read()

        access_code = self.__get_access_code(
                client_id=self.Credentials['clientId'],
                redirect_uri=self.Credentials['DEFAULT_REDIRECT_URI'],
                oauth_url=self.Credentials['DEFAULT_OAUTH_URL'])

        self.Authorization = self.__sign_in(
                client_id=self.Credentials['clientId'],
                client_secret=self.Credentials['clientSecred'],
                access_code=access_code,
                redirect_uri=self.Credentials['DEFAULT_REDIRECT_URI'],
                oauth_url=self.Credentials['DEFAULT_OAUTH_URL'])

        self.Authorization["expires_time_sec"] = \
        		self.Authorization["expires_in"]+datetime.now().timestamp()

        if writeDownToken:
            self.__token_write()

        pass

    def load_token(self):

        if not hasattr(self, 'Credentials'):
            self.__credentials_read()

        self.__token_read()

        if self.Authorization["expires_time_sec"] < datetime.now().timestamp():
        	self.refresh_token()

        pass

    def refresh_token(self, writeDownToken=True, if_load_token=True,):

        if not hasattr(self, 'Credentials'):
            self.__credentials_read()

        if not hasattr(self, 'Authorization'):
            self.__token_read()

        if if_load_token:
            self.__token_read()

        self.Authorization = self.__refresh_token(
                client_id=self.Credentials['clientId'],
                client_secret=self.Credentials['clientSecred'],
                refresh_token=self.Authorization['refresh_token'],
                redirect_uri=self.Credentials['DEFAULT_REDIRECT_URI'],
                oauth_url=self.Credentials['DEFAULT_OAUTH_URL'])

        self.Authorization["expires_time_sec"] = \
        		self.Authorization["expires_in"]+datetime.now().timestamp()

        if writeDownToken:
            self.__token_write()

        pass

    def resource_get(self, resource_name, params, print_error=True):

        if not hasattr(self, 'Credentials'):
            self.__credentials_read()

        if not hasattr(self, 'Authorization'):
            self.__token_read()

        if self.Authorization["expires_time_sec"] < datetime.now().timestamp():
        	self.refresh_token()

        headers = {
                'charset': 'utf-8',
                'Accept-Language': 'pl-PL',
                'Content-Type': 'application/json',
                'Accept': 'application/vnd.allegro.public.v1+json',
                'Authorization': "Bearer {}".format(
                        self.Authorization['access_token'])
                }

        with requests.Session() as session:
            session.headers.update(headers)
            response = session.get(self.Credentials['DEFAULT_API_URL'] +
                                   resource_name,
                                   params=params)

            if response.status_code == 200:
                return response.status_code, response.json()
            else:
                if print_error:
                    print("Error code {}".format(str(response.status_code)))
                return response.status_code, json.loads(json.dumps({}))


"""
RestApi = AllegroRestApi()

RestApi.credentials_set(
        appName='xszpo_rest',
        clientId='5b28dba1eb26446db2f2834e3354346e',
        clientSecred='HByQO2Em9QP8YnRS9iDf6g4iN66fRLiEV2u'
                     '7kKpybUjt5qD4yOtpTOWjKuxMITLY',
        redirectUrl='http://localhost:8000'
        )

RestApi.credentials_field_set('test', 666, ifWriteToFile=False)

RestApi.get_token()

RestApi.load_token()

RestApi.refresh_token()

RestApi.resource_get(
        resource_name='/users/{userId}/ratings-summary'.format(
                **{'userId': 11791190}),
        params={}
        )

RestApi.resource_get(
        resource_name='/sale/user-ratings',
        params={'user.id': '11791190', 'limit': 100}
        )

RestApi.resource_get(
        resource_name='/sale/user-ratings',
        params={'user.id': '1091465', 'limit': 100}
        )

RestApi.resource_get(
        resource_name='/offers/listing',
        params={'phrase': 'samsung'}
        )
"""

