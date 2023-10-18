import mysql.connector
import os
import txt


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
    znaki = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "{", "}", ":", ";", "[", "]", "\"", "'", "<", ",", ">",
             ".", "?", "/", "|"]
    for znak in znaki:
        if znak in do_sprawdzenia:
            input("Podałeś niedozwolony znak. Naciśnij enter i spróbuj ponownie.")
            os.system("cls")
            return True


def zarzadzanie_katami():
    os.system("cls")
    mycursor.execute(
        f"SELECT rodzaj, konta.id, imie, nazwisko FROM uzytkownicy join konta on konta.id_uzytkownika = uzytkownicy.id order by nazwisko")
    myresult = mycursor.fetchall()
    print(f"    id_konta rodzaj   imie   nazwisko")
    for num, row in enumerate(myresult):
        print(f"{num+1}       {row[1]}     {row[0]}       {row[3]}    {row[2]}")
    try:
        numer = int(input("Podaj id konta które chcesz usunąć: "))
        mycursor.execute(f"DELETE FROM `konta` WHERE id={numer}")
        mydb.commit()
        input("Przesłano żądanie do  bazy danych.")
    except:
        input("Podano zły numer.")


def dziecko_rodzic():
    os.system("cls")
    mycursor.execute(
        f"SELECT rodzaj, konta.id, imie, nazwisko FROM uzytkownicy join konta on konta.id_uzytkownika = uzytkownicy.id where rodzaj = 'r' or rodzaj = 'u' order by nazwisko")
    myresult = mycursor.fetchall()
    print(f"rodzaj  id  imie    nazwisko")
    id_i_rodzaj = {}
    for num, row in enumerate(myresult):
        print(f"{row[0]} {row[1]} {row[2]} {row[3]}")
        id_i_rodzaj[(int(row[1]))] = row[0]
    try:
        numer_r = int(input("Podaj id konta które chcesz wybrać jako rodzica: "))
        if numer_r not in id_i_rodzaj or id_i_rodzaj[numer_r] != "r":
            input("Nie ma takiego id konta lub nie jest ono zapisane jako rodzic.")
            return False
        numer_d = int(input("Podaj id konta które chcesz wybrać jako dziecko: "))
        if numer_d not in id_i_rodzaj or id_i_rodzaj[numer_d] != "u":
            input("Nie ma takiego id konta lub nie jest ono zapisane jako uczen.")
            return False

        mycursor.execute(
            f"SELECT id FROM rodzice where id_rodzica = '{numer_r}' and id_ucznia = '{numer_d}'")
        myresult = mycursor.fetchone()
        if myresult:
            input("Ten rodzic i uczeń są już połączeni.")
            return False
        mycursor.execute(
            f"SELECT id FROM rodzice where id_rodzica = '{numer_r}'")
        myresult = mycursor.fetchone()
        if myresult:
            input("Ten rodzic jest juz przypisany do konta dziecka, stwórz nowe konto aby połączyć je z innym dzieckiem.")
            return False
        mycursor.execute(f"INSERT INTO `rodzice` (`id`, `id_rodzica`, `id_ucznia`) VALUES (NULL, '{numer_r}', '{numer_d}')")
        mydb.commit()
        input("Przesłano żądanie do  bazy danych.")
    except:
        input("Error, spróbuj jeszcze raz.")


def nauczyciel_przedmiot_klasa():
    os.system("cls")
    mycursor.execute(
        f"SELECT konta.id, imie, nazwisko FROM uzytkownicy join konta on konta.id_uzytkownika = uzytkownicy.id where rodzaj='n' order by nazwisko")
    myresult = mycursor.fetchall()
    id = []
    print(f"id_konta  imie       nazwisko")
    for row in myresult:
        print(f"{row[0]}         {row[2]} {row[1]}")
        id.append(int(row[0]))
    try:
        numer = int(input("\nPodaj id konta nauczyciela które chcesz połączyć: "))
        if numer not in id:
            input("Nie ma takiego id konta.")
            return False
        przedmiot = input(txt.nauczyciel_przedmiot)
        if przedmiot == "m":
            przedmiot = "matematyka"
        elif przedmiot == "p":
            przedmiot = "polski"
        elif przedmiot == "a":
            przedmiot = "angielski"
        else:
            input("Użyłeś niedozwolonego znaku.")
            return False
        mycursor.execute(
            f"SELECT klasa FROM klasy group by klasa")
        myresult = mycursor.fetchall()
        klasy = []
        for num, row in enumerate(myresult):
            print(f"{num + 1} {row[0]}")
            klasy.append(row[0])
        klasa = int(input("Podaj numer klasy którą chcesz wybrać: "))
        if klasa > len(klasy) or klasa < 1:
            input("Nie ma takiego numeru klasy.")
            return False
        klasa = klasy[klasa - 1]
        mycursor.execute(f"INSERT INTO `nauczyciele` (`id_nauczyciela`, `przedmiot`, `klasa`) VALUES ('{numer}', '{przedmiot}', '{klasa}')")
        mydb.commit()
        input("Przesłano żądanie do  bazy danych.")
    except:
        input("Error, spróbuj jeszcze raz.")


def dodaj_uzytkownika():
    imie = input("Podaj imie uzytkownika: ").lower()
    nazwisko = input("Podaj nazwisko uzytkownika: ").lower()
    if zgodnosc_znakow(imie) or zgodnosc_znakow(nazwisko):
        return False
    rodzaj = input(txt.rodzaj_uzytkownika).lower()
    if rodzaj != "u" and rodzaj != "r" and rodzaj != "n" and rodzaj != "a":
        input("Podałeś niedozwolony znak. Naciśnij enter i spróbuj ponownie.")
        os.system("cls")
        return False
    if rodzaj == "u":
        mycursor.execute(
            f"SELECT klasa FROM klasy group by klasa")
        myresult = mycursor.fetchall()
        klasy = []
        print("\n")
        for num, row in enumerate(myresult):
            print(f"{num + 1} {row[0]}")
            klasy.append(row[0])
        numer = int(input("\nPodaj numer klasy do której ma należeć uczen np.1, 4, 6: "))
        if numer < 1 or numer > len(klasy):
            input("Nie ma takiego numeru klasy.")
            return False
        klasa = klasy[numer - 1]
    try:
        mycursor.execute(
            f"INSERT INTO `uzytkownicy` (`id`, `imie`, `nazwisko`, `rodzaj`) VALUES (NULL, '{imie}', '{nazwisko}', '{rodzaj}');")
        mydb.commit()
        if rodzaj == "u":
            mycursor.execute(
                f"SELECT `id` FROM `uzytkownicy` WHERE imie = '{imie}' and `nazwisko` = '{nazwisko}' and `rodzaj` = '{rodzaj}'")
            myresult = mycursor.fetchone()
            mycursor.execute(
                f"INSERT INTO `klasy` (`klasa`, `id_uzytkownika`) VALUES ('{klasa}', '{int(myresult[0])}');")
            mydb.commit()
    except:
        input("Wystąpił niespodziewany błąd z bazą danych.")
