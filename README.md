# allegro-api

The aim of this project is to create a python package to easily collect information about ofers and sellers through allegro APIs.     
<br/>
Allegro has two APIs, with different scope of methods available: 
* [Web API](https://allegro.pl/webapi/general.php)
>Allegro WebAPI to usługa sieciowa opierająca swoje działanie na protokole SOAP, wykorzystująca język XML jako format tworzenia komunikatów oraz protokół RPC do ich przenoszenia pomiędzy klientem (aplikacją), a serwerem WebAPI. Usługa jest w pełni zgodna z obecnie obowiązującymi standardami SOAP.    
>Pełny opis usługi zdefiniowany został za pomocą języka WSDL i znaleźć go można pod adresem (dostępnym wyłącznie za pośrednictwem kanału szyfrowanego): https://webapi.allegro.pl/service.php?wsdl. WSDL kodowany jest w stylu Document/Literal (Wrapped) - zgodnym ze standardami WS-I.    
>Wykorzystanie protokółu RPC determinuje architekturę usługi. Allegro WebAPI składa się z [szeregu metod](https://allegro.pl/webapi/documentation.php?cod=OGZkZlVlNmJk), które stanowią odwzorowanie poszczególnych funkcjonalności serwisu.

* [Rest AP](https://developer.allegro.pl/about/) 
>Platforma Allegro udostępnia klientom funkcjonalności w ramach API w oparciu o architekturę [REST](https://en.wikipedia.org/wiki/Representational_state_transfer). Wykorzystuje do tego celu protokół HTTP wraz z jego metodami: GET, POST, PUT, DELETE. Elementy platformy Allegro zostały podzielone na zasoby (np. /offers, /users, /categories, itd). Dostęp do poszczególnych zasobów następuje poprzez wywołanie wybranej metody HTTP na adres: https://api.allegro.pl, dodając ścieżkę do wybranego zasobu.    
>Dostęp do API uzyskasz po [zarejestrowaniu](https://apps.developer.allegro.pl/) swojej aplikacji.    
>Wszystkie żądania zasobów REST API wymagają przekazania tokena [OAuth](https://en.wikipedia.org/wiki/OAuth) w nagłówku Authorization. Więcej o autoryzacji za pomocą OAuth przeczytasz w dedykowanym temu tematowi [artykule](https://developer.allegro.pl/auth).

Tutorials:
* [RestApi](https://github.com/xSzpo/allegro/blob/master/tutorial_AllegroRestApi.ipynb)
* [WebApi](https://github.com/xSzpo/allegro/blob/master/tutorial_AllegroWebApi.ipynb)

Allegro api documentation:    
* [Rest Api](https://developer.allegro.pl/documentation/)    
* [Web Api](https://allegro.pl/webapi/documentation.php)
