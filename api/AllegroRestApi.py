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

import requests
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import webbrowser
import json
import os

os.chdir('/Users/xszpo/Google Drive/DataScience/Projects/201808_allegro')
credentialsFilePath = '../credentials/allegro_credentials_rest.json'
tokenFilePath = '../credentials/allegro_rest_token.json'


class AllegroRestApi():
    """
    https://developer.allegro.pl/auth/
    """

    def __init__(self,
                 credentialsFilePath='../credentials/allegro_credentials'
                                     '_rest.json',
                 tokenFilePath='../credentials/allegro_rest_token.json',
                 appNameField='nazwaAplikacji',
                 clientIdField='clientId',
                 clientSecredField='clientSecred',
                 redirectField='redirect',
                 DEFAULT_OAUTH_URL='https://allegro.pl/auth/oauth',
                 DEFAULT_REDIRECT_URI='http://localhost:8000',
                 DEFAULT_API_URL = 'https://api.allegro.pl'
                 ):
        self.credentialsFilePath = credentialsFilePath
        self.tokenFilePath = tokenFilePath
        self.Credentials = self.__load_credentials(self.credentialsFilePath)
        self.appName = self.Credentials[appNameField]
        self.clientId = self.Credentials[clientIdField]
        self.clientSecred = self.Credentials[clientSecredField]
        self.redirect = self.Credentials[redirectField]
        self.DEFAULT_OAUTH_URL = DEFAULT_OAUTH_URL
        self.DEFAULT_REDIRECT_URI = DEFAULT_REDIRECT_URI
        self.DEFAULT_API_URL = DEFAULT_API_URL

    def rest_api_help(self):
        return webbrowser.open('https://developer.allegro.pl/')

    def __load_credentials(self, file_path: str = 'credentials.json'):
        try:
            assert os.path.exists(file_path)
            with open(file_path, 'r') as file:
                credentials = file.readlines()

            credentials = json.loads(" ".join(credentials))
            return credentials

        except AssertionError:
            raise Exception('Path {} doesn\'exist'.format(
                                                file_path))

        except Exception as e:
            print(e)
            raise

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
        print('Got an authorize code: ', _access_code)

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

    def __refresh_token(self,client_id, client_secret, refresh_token, 
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

    def get_token(self, writeDownToken=True):
        access_code = self.__get_access_code(
                client_id=self.clientId,
                redirect_uri=self.DEFAULT_REDIRECT_URI,
                oauth_url=self.DEFAULT_OAUTH_URL)

        self.Authorization = self.__sign_in(
                client_id=self.clientId,
                client_secret=self.clientSecred,
                access_code=access_code,
                redirect_uri=self.DEFAULT_REDIRECT_URI,
                oauth_url=self.DEFAULT_OAUTH_URL)

        if writeDownToken:
            with open(self.tokenFilePath, 'w') as file:
                json.dump(self.Authorization, file)

        pass

    def load_token(self):

        with open(self.tokenFilePath, 'r') as file:
            self.Authorization = json.load(file)

        pass

    def refresh_token(self, if_load_token=True, writeDownToken=True):

        if if_load_token:
            self.load_token()

        self.Authorization = self.__refresh_token(
                client_id=self.clientId,
                client_secret=self.clientSecred,
                refresh_token=self.Authorization['refresh_token'],
                redirect_uri=self.DEFAULT_REDIRECT_URI,
                oauth_url=self.DEFAULT_OAUTH_URL)

        if writeDownToken:
            with open(self.tokenFilePath, 'w') as file:
                json.dump(self.Authorization, file)

        pass

    def call_resource(self, resource_name, params):

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
            response = session.get(self.DEFAULT_API_URL +
                                   resource_name,
                                   params=params)
            return response.json()


RestApi = AllegroRestApi(credentialsFilePath=credentialsFilePath,
                         tokenFilePath=tokenFilePath)

RestApi.get_token(writeDownToken=True)
RestApi.load_token()
RestApi.refresh_token(if_load_token=True, writeDownToken=True)

RestApi.Authorization

RestApi.call_resource(
        resource_name='/after-sales-service-conditions/warranties',
        params={'sellerId': '1091465'}
        )

RestApi.call_resource(
        resource_name='/users/41952603/ratings-summary',
        params={}
        )

RestApi.call_resource(
        resource_name='/sale/user-ratings',
        params={'user.id': '1091465', 'limit':100}
        )


plik_json = RestApi.call_resource(
        resource_name='/offers/listing',
        params={'phrase': 'samsung'}
        )

with open('plik_json.json','w') as file:
    json.dump(plik_json,file)
