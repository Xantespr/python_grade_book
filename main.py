import mysql.connector
import os
import base64
import txt
import wiadomosci
import oceny
import admin

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


def rejestracja(mycursor):
    os.system('cls')
    input(txt.rejestracja_info)
    imie = input("        REJESTRACJA\nPodaj swoje imię:\n").lower()
    nazwisko = input("Podaj swoje nazwisko:\n").lower()
    mycursor.execute(f"SELECT id FROM uzytkownicy WHERE imie='{imie}' AND nazwisko='{nazwisko}'")
    myresult = mycursor.fetchall()
    mycursor.execute(f"SELECT * FROM uzytkownicy join konta on konta.id_uzytkownika = uzytkownicy.id WHERE imie='{imie}' AND nazwisko='{nazwisko}'")
    myresult_check = mycursor.fetchall()
    if len(myresult) > 1:
        input(txt.rejestracja_baza_blad)
        start()
    if not myresult:
        input(txt.rejestracja_brak_rekordow)
        rejestracja(mycursor)
    if not myresult_check:
        login = input(txt.rejestracja_podaj_login)
        haslo = input(txt.rejestracja_podaj_haslo)
        znaki = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "{", "}", ":", ";", "[", "]", "\"", "'", "<", ",", ">", ".", "?", "/", "|"]
        for znak in znaki:
            if znak in login or znak in haslo:
                input("Użyłeś niedozwolonego znaku w loginie lub hasle.")
                rejestracja(mycursor)
        if len(haslo) < 4 or len(login) < 4:
            input("Za krótki login lub hasło, minimum 4 znaki.")
            rejestracja(mycursor)
        haslo = base64.b64encode(haslo.encode("utf-8"))
        haslo = str(haslo).replace("b'", "", 1)
        haslo = haslo[::-1].replace("'", "")
        haslo = haslo[::-1]
        mycursor.execute(
            f"SELECT * FROM konta WHERE haslo='{haslo}'")
        myresult_check2 = mycursor.fetchone()
        if not myresult_check2:
            mycursor.execute(f"INSERT INTO `konta` (`id`, `login`, `haslo`, `id_uzytkownika`) VALUES (NULL, '{login}', '{haslo}', '{myresult[0][0]}');")
            mydb.commit()
            input(txt.rejestracja_udana)
            logowanie(mycursor)
        else:
            input(txt.rejestracja_haslo_istnieje)
            rejestracja(mycursor)
    else:
        input(txt.rejestracja_konto_istnieje)
        start()


def logowanie(mycursor):
    os.system("cls")

    login = input(txt.logowanie1)

    haslo = base64.b64encode(input(txt.logowanie2).encode("utf-8"))
    haslo = str(haslo).replace("b'", "", 1); haslo = haslo[::-1].replace("'", ""); haslo = haslo[::-1]

    mycursor.execute(f"SELECT id, id_uzytkownika FROM konta WHERE login='{login}' AND haslo='{haslo}'")
    myresult = mycursor.fetchone()
    if not myresult:
        if str(input(txt.odrzucone_logowanie)).lower() == "r":
            rejestracja(mycursor)
        else:
            start()
    else:
        mycursor.execute(f"SELECT imie, nazwisko, rodzaj FROM uzytkownicy WHERE id={myresult[1]}")
        myresult1 = mycursor.fetchone()
        #dane = [id_konta, id_uzytkownika, imie, nazwisko, rodzaj_konta]
        dane = [myresult[0], myresult[1], myresult1[0], myresult1[1], myresult1[2]]
        os.system("cls")
        if myresult1[2] == "r":
            panel_rodzica(dane)
        elif myresult1[2] == "n":
            panel_nauczyciela(dane)
        elif myresult1[2] == "a":
            panel_admin()
        else:
            panel_ucznia(dane)


def panel_ucznia(dane):
    os.system("cls")
    print(f"Zalogowano jako uczen.\n{dane[2]} {dane[3]}")
    u_choice = str(input(txt.panel_ucznia)).lower()

    if u_choice == "l":
        start()
    elif u_choice == "o":
        oceny.wyswietl_oceny(dane)
    elif u_choice == "w":
        wiadomosci.menu(dane[0], "u")
    panel_ucznia(dane)


def panel_rodzica(dane):
    os.system("cls")
    print(f"Zalogowano jako rodzic.\n{dane[2]} {dane[3]}")
    u_choice = str(input(txt.panel_ucznia)).lower()

    if u_choice == "l":
        start()
    elif u_choice == "o":
        oceny.wyswietl_oceny(dane)
    elif u_choice == "w":
        wiadomosci.menu(dane[0], "r")
    panel_rodzica(dane)


def panel_nauczyciela(dane):
    os.system("cls")
    print(f"Zalogowano jako nauczyciel.\n{dane[2]} {dane[3]}")
    u_choice = str(input(txt.panel_ucznia)).lower()

    if u_choice == "l":
        start()
    elif u_choice == "o":
        oceny.menu(dane[0])
    elif u_choice == "w":
        wiadomosci.menu(dane[0], "n")
    panel_nauczyciela(dane)


def panel_admin():
    os.system("cls")
    u_choice = input(txt.admin_main).lower()

    if u_choice == "l":
        start()
    elif u_choice == "k":
        admin.zarzadzanie_katami()
    elif u_choice == "r":
        admin.dziecko_rodzic()
    elif u_choice == "u":
        admin.dodaj_uzytkownika()
    elif u_choice == "n":
        admin.nauczyciel_przedmiot_klasa()
    panel_admin()


def start():
    os.system("cls")
    user_in = str(input(txt.uruchamianie)).lower()
    if user_in == "r":
        rejestracja(mycursor)
    elif user_in == "q":
        quit()
    else:
        logowanie(mycursor)


start()
