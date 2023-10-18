import mysql.connector
import txt
import os


try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dziennik"
    )
    mycursor = mydb.cursor(buffered=True)
except:
    print("Błąd połączenia z bazą danych.")
    quit()


def zgodnosc_znakow(do_sprawdzenia):
    znaki = ["\"", "'"]
    for znak in znaki:
        if znak in do_sprawdzenia:
            input("Podałeś niedozwolony znak. Naciśnij enter i spróbuj ponownie.")
            os.system("cls")
            return True


def wyslij_wiadomosc(id_nadawcy, rodzaj):
    os.system("cls")
    if rodzaj == "u" or rodzaj == "r":
        rodzaj_odbiorcy = "n"
    else:
        rodzaj_odbiorcy = "u' or rodzaj = 'r"
    mycursor.execute(
        f"SELECT konta.id, imie, nazwisko, rodzaj from konta join uzytkownicy on konta.id_uzytkownika = uzytkownicy.id WHERE rodzaj = '{rodzaj_odbiorcy}' ORDER BY nazwisko")
    myresult = mycursor.fetchall()
    konta = []
    for num, row in enumerate(myresult):
        print(f"{num + 1} {row[3]} {row[1]} {row[2]}")
        konta.append(int(row[0]))
    try:
        numer_odbiorcy = int(input("Podaj numer osoby do której chcesz zaadresować wiadomość: "))
        if numer_odbiorcy < 1 or numer_odbiorcy > len(konta):
            input(txt.bledne_dane)
            wyslij_wiadomosc(id_nadawcy, rodzaj)
        id_odbiorcy = konta[numer_odbiorcy-1]
        temat = input(f"Podaj temat wiadomości(max 100 znakow). ")
        tresc = input(f"Podaj tresc wiadomosci(max 500 znakow): ")
        if len(temat) > 100 or len(tresc) > 500 or len(temat) < 1 or len(tresc) < 1:
            input(txt.bledne_dane)
            wyslij_wiadomosc(id_nadawcy, rodzaj)
        if zgodnosc_znakow(temat) or zgodnosc_znakow(tresc):
            wyslij_wiadomosc(id_nadawcy, rodzaj)
        mycursor.execute(
            f"INSERT INTO `wiadomosci` (`id`, `id_nadawcy`, `id_odbiorcy`, `temat`, `tresc`) VALUES (NULL, '{id_nadawcy}', '{id_odbiorcy}', '{temat}', '{tresc}');")
        mydb.commit()
        input("Wysłano wiadomość.")
    except:
        input(txt.bledne_dane)


def skrzynka_odbiorcza(id_zalogowanego, rodzaj):
    os.system("cls")
    mycursor.execute(
        f"SELECT nazwisko, imie, temat, tresc FROM `wiadomosci` join konta on konta.id = wiadomosci.id_nadawcy join uzytkownicy on uzytkownicy.id = konta.id_uzytkownika WHERE wiadomosci.id_odbiorcy = {id_zalogowanego}")
    myresult = mycursor.fetchall()
    tresci = []
    for num, row in enumerate(myresult):
        print(f"{num + 1} {row[0]} {row[1]} {row[2]}")
        tresci.append(row[3])
    numer = input("Podaj numer wiadomosci ktorej tresci chcesz zobaczyc lub wpisz b aby cofnac: ")
    if numer.lower() == "b":
        menu(id_zalogowanego, rodzaj)
    try:
        numer = int(numer)
        if numer < 1 or numer > len(tresci):
            input(txt.bledne_dane)
            skrzynka_odbiorcza(id_zalogowanego, rodzaj)
        input(tresci[numer - 1])
        skrzynka_odbiorcza(id_zalogowanego, rodzaj)
    except:
        input(txt.bledne_dane)


def menu(id_zalogowanego, rodzaj):
    os.system("cls")
    u_choice = input(txt.wiadomosci_menu).lower()
    if u_choice == "n":
        wyslij_wiadomosc(id_zalogowanego, rodzaj)
    elif u_choice == "o":
        skrzynka_odbiorcza(id_zalogowanego, rodzaj)
    else:
        return False
