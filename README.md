# Symulacja dziennika elektronicznego w terminalu
Mała symulacja działania dziennika elektronicznego w pythonie, z wykorzystaniem bazy danych mysql. 

## Instalacja

Zainstaluj mysql connector za pomocą pip, pythonowego menadżera do pobierania bibliotek.

```bash
pip install mysql-connector-python
```

Stwórz bazę danych "dziennik" i zaimportuj do niej dane z pliku dziennik.sql

## Funkcje
main.py
```python
#Pozwala użytkownikowi, który został dodany do tabeli użytkownicy przez administratora, stworzyć konto.
rejestracja()
#Pobiera dane od użytkownika i łączy z odpowiednim kontem.
logowanie()

#Panele służą do rozdzielenia funkcjonalności w zależności od rodzaju konta(nauczyciel, rodzic, uczen, administrator).
panel_ucznia()
panel_rodzica()
panel_nauczyciela()
panel_admin()

#Główne menu, użytkownik wybiera tu między logowaniem i rejestracją.
start()  
```
admin.py
```python
#Sprawdza czy w podanym  wyrazie x znajują się znaki niedozwolone takie jak "\" lub "'"
zgodnosc_znakow(x)

#Pozwala usuwać rekordy z tabeli konta.
zarzadzanie_katami()

#Łączy id konta ucznia i id konta rodzica co pozwala rodzicowi wyświetlać oceny dziecka na swoim koncie.
dziecko_rodzic()

#Łączy konto nauczyciela z klasą i przedmiotami jakich uczy.
nauczyciel_przedmiot_klasa()

#Dodawanie uzytkownika do tabeli uzytkownicy (bez tego uzytkownik nie  moze zalozyc konta).
dodaj_uzytkownika()
```

oceny.py
```python
#Pozwala wpisywać oceny klasom i z przedmiotów z jakimi powiązane jest id konta(nauczyciela) przekazane do funkcji.
wpisz_oceny(id_konta)

#Wyświetla oceny (tylko dla konkretnego ucznia).
wyswietl_oceny(dane)

#Pozwala wyswietlac oceny klas i z przedmiotów z jakimi powiązane jest id konta(nauczyciela) przekazane do funkcji.
wyswietl_wszystkie_oceny(id_konta)

#Pozwala nauczycielowi usuwać oceny z przedmiotów i w klasach z którymi jest połączony.
usun_ocene(uczniowie, przedmioty)

#Menu dla nauczyciela, pozwala wybrać międzu przeglądaniem i dodawaniem ocen.
menu(id_konta)
```

wiadomosci.py
```python
#Sprawdza czy w podanym  wyrazie do_sprawdzenia znajują się znaki niedozwolone takie jak "\" lub "'".
zgodnosc_znakow(do_sprawdzenia)

#Wysyła wiadomość do id konta wybranego przez nadawce.
wyslij_wiadomosc(id_nadawcy, rodzaj)

#Pozwala przegladac otrzymane wiadomosci.
skrzynka_odbiorcza(id_zalogowanego, rodzaj):

#Mozliwosc wybrania miedzy skrzynka odbiorczą i wysłaniem nowej wiadomości.
menu(id_zalogowanego, rodzaj)
```

txt.py

Plik zawiera komunikaty tekstowe dla wszystkich uzytkownikow przeniesione z plików z kodem dla zwiększenia przejrzystości.
