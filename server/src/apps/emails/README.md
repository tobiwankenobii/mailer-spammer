### Requirements 1

* Rejestracja użytkowników
* Panel administracyjny z możliwością wpisywania adresu mailowego, tytułu maila, treści maila, obrazków i godziny w
  jakiej ten mail ma zostać wysłany
* Serwer buduje maila o określonej godzinie dołącza treści, które zostały zdefiniowane przez użytkownika i wysyła maila
* Mail ma być budowany ad hoc. Nie chcemy optymalizacji na zasadzie zapisywania zrobionego maila do bazy.

### Requirements 2

* Zapisywanie adresu mailowego i linków z RSS'ami do bazy danych.
* Ściągniecie zawartości znajdującej się pod danymi RSS'ami zbudowanie na ich podstawie maila.
* Przycisk Preview ma wyświetlić zawartość maila w iframe na frontendzie
* Przycisk Send ma za zadanie wysłać maila za pomocą sendgrida do zapisanego maila.
