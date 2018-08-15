#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 18:42:42 2018

@author: xszpo
"""
#suds-jurko
#https://cwsi.pl/ecommerce/allegro/podstawy-obslugi-web-api-allegro-pl-web-services-i-modul-suds-jurko-w-pythonie/
#https://allegro.pl/webapi/general.php

#Ac5VInyGDrgLAy7

from suds.client import Client
import hashlib
import base64

client = Client('https://webapi.allegro.pl/service.php?wsdl')

response = client.service.doQueryAllSysStatus(webapiKey='888842ec14b14fb5bbc68c0bfd5f5d98', countryId=1)

version_key = response.item[0].verKey

sha256_application_password = hashlib.sha256('Ac5VInyGDrgLAy7'.encode('utf-8')).digest()

auth = client.service.doLoginEnc(
    userLogin='nicke1',
    userHashPassword=base64.b64encode(sha256_application_password).decode('utf-8'), 
    countryCode=1,
    webapiKey='888842ec14b14fb5bbc68c0bfd5f5d98', 
    localVersion=version_key
)

session = auth.sessionHandlePart

dir(client.service)