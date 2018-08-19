# allegro-api

pyAllegro is a framework, that provides a simple way to use Allegro [Web API](https://allegro.pl/webapi/general.php) and [Rest AP](https://developer.allegro.pl/about/). You don't need to know how RESTful, SOAP or oauth 2.0 works.    
<br/>
As for now it's prepared for getting data from allegro - not for managing your account or bidding.   


### Get started:   

1. Go to https://apps.developer.allegro.pl/ and register your app. **You need to setup redirecion url to ```http://localhost:8000```** - it will be your local server that recive your autorization data (oauth 2.0),
2. Generate your app password [here](https://allegro.pl/myaccount/Settings/security_settings.php/applicationPasswords),
3. Install pyAllegro with ```pip install pyAllegro```
4. Import ```from pyAllegro.api import AllegroRestApi, AllegroWebApi```
5. Setup credentials that you recived from allegro:
```
RestApi = AllegroRestApi()
#RestApi = AllegroRestApi(config_file_dir='/Users/xszpo/.allegroApiConfig')

RestApi.credentials_set(
        appName='<credentials from allegro>',
        clientId='<credentials from allegro>',
        clientSecred='<credentials from allegro>',
        redirectUrl='http://localhost:8000'
        )

RestApi = AllegroRestApi()
#RestApi = AllegroRestApi(config_file_dir='/Users/xszpo/.allegroApiConfig')

RestApi.credentials_set(
        appName='<credentials from allegro>',
        clientId='<credentials from allegro>',
        clientSecred='<credentials from allegro>',
        redirectUrl='http://localhost:8000'
        )
```




Tutorials:
* [RestApi](https://github.com/xSzpo/allegro/blob/master/tutorial_AllegroRestApi.ipynb)
* [WebApi](https://github.com/xSzpo/allegro/blob/master/tutorial_AllegroWebApi.ipynb)

Allegro api documentation:    
* [Rest Api](https://developer.allegro.pl/documentation/)    
* [Web Api](https://allegro.pl/webapi/documentation.php)
