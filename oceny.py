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


def wpisz_oceny(id_konta):
    os.system("cls")
    mycursor.execute(f"SELECT przedmiot, klasa from nauczyciele WHERE id_nauczyciela ='{id_konta}'")
    myresult = mycursor.fetchall()
    przedmioty = []
    klasy = []
    for row in myresult:
        przedmioty.append(row[0])
        klasy.append(row[1])
    klasa = klasy[0]
    if len(klasy) > 1:
        for klasa_for in klasy:
            klasa += f"' or klasa ='{klasa_for}"

    mycursor.execute(f"SELECT imie, nazwisko, id, klasa from klasy join uzytkownicy on klasy.id_uzytkownika = uzytkownicy.id WHERE rodzaj ='u' and klasa ='{klasa}'")
    myresult = mycursor.fetchall()
    for num, row in enumerate(myresult):
        print(f"{num+1} {row[3]}| {row[0]} {row[1]}")

    numer = input("Podaj numer ucznia któremu wystawiasz ocenę: ")
    try:
        numer = int(numer)
    except:
        input("Zły format danych, podaj cyfrę.")
        return False

    if numer < 1 or numer > num + 2:
        input("Podano zły numer ucznia.")
        return False

    ocena = input("Podaj ocenę: ")
    try:
        ocena = int(ocena)
    except:
        input("Zły format danych, podaj cyfrę.")
        return False

    for num, p in enumerate(przedmioty):
        print(f"{num + 1} - {p}")
    user_ch = int(input("Podaj numer przedmiotu z  którego chcesz wystawić ocenę: "))
    if user_ch > len(przedmioty) or user_ch < 1:
        print("Nie ma takiego numeru przedmiotu.")
        return False
    przedmiot = przedmioty[user_ch - 1]

    mycursor.execute(f"INSERT INTO `oceny` (`id`, `ocena`, `przedmiot`, `id_ucznia`) VALUES (NULL, '{ocena}', '{przedmiot}', '{myresult[numer-1][2]}');")
    mydb.commit()


def wyswietl_oceny(dane):
    os.system("cls")
    if dane[4] == "r":
        try:
            mycursor.execute(
                f"SELECT uzytkownicy.id from rodzice join konta on rodzice.id_ucznia = konta.id join uzytkownicy on konta.id_uzytkownika = uzytkownicy.id WHERE rodzice.id_rodzica = '{dane[0]}'")
            myresult = mycursor.fetchone()
            dane[1] = int(myresult[0])
        except:
            input("Z tym kontem nie jest powiazany żaden uczen.")
            return False
    mycursor.execute(f"SELECT ocena, przedmiot from oceny join uzytkownicy on oceny.id_ucznia = uzytkownicy.id WHERE uzytkownicy.id = '{dane[1]}' ORDER BY przedmiot")
    myresult = mycursor.fetchall()
    przedmiot = ""
    oceny = ""
    srednia = []
    og_srednia = []
    try:
        for row in myresult:
            if przedmiot == "":
                przedmiot = row[1]
                oceny = str(f"{row[0]} ")
                srednia.append(int(row[0]))
            elif row[1] == przedmiot:
                oceny += f"{row[0]} "
                srednia.append(int(row[0]))
            elif row[1] != przedmiot:
                srednia = sum(srednia)/len(srednia)
                print(f"{przedmiot}\n{oceny}\nSrednia z ocen: {round(srednia, 2)}\n")
                og_srednia.append(srednia)
                srednia = []
                przedmiot = row[1]
                oceny = str(f"{row[0]} ")
                srednia.append(int(row[0]))
        srednia = sum(srednia) / len(srednia)
        og_srednia.append(srednia)
        og_srednia = sum(og_srednia)/len(og_srednia)
        input(f"{przedmiot}\n{oceny}\nSrednia z ocen: {round(srednia, 2)}\n\nOgolna srednia: {round(og_srednia, 2)}\n")
    except:
        input("Nie masz jeszcze żadnych ocen. :c")


def wyswietl_wszystkie_oceny(id_konta):
    os.system("cls")
    mycursor.execute(f"SELECT przedmiot, klasa from nauczyciele WHERE id_nauczyciela ='{id_konta}'")
    myresult = mycursor.fetchall()
    klasy = []
    przedmioty = []
    for row in myresult:
        przedmioty.append(row[0])
        klasy.append(row[1])
    klas = klasy[0]
    przedm = przedmioty[0]
    if len(klasy) > 1:
        for klasa_for in klasy:
            if klasa_for != klasy[0]:
                klas += f"' or klasa ='{klasa_for}"

    if len(przedmioty) > 1:
        for przedm_for in przedmioty:
            if przedm_for != przedmioty[0]:
                przedm += f"' or przedmiot ='{przedm_for}"

    mycursor.execute(f"SELECT ocena, przedmiot, imie, nazwisko from oceny join uzytkownicy on oceny.id_ucznia = uzytkownicy.id join klasy on uzytkownicy.id = klasy.id_uzytkownika WHERE (klasa = '{klas}') and (przedmiot = '{przedm}') ORDER BY uzytkownicy.id, przedmiot")
    myresult1 = mycursor.fetchall()
    przedmiot = ""
    oceny = ""
    uczniowie = []
    uczen = ""
    for row in myresult1:
        if przedmiot == "":
            print(f"{row[3]} {row[2]}")
            uczen = f"{row[3]} {row[2]}"
            uczniowie.append(uczen.lower())
            przedmiot = row[1]
            oceny = str(f"{row[0]} ")
        elif row[1] == przedmiot and uczen == f"{row[3]} {row[2]}":
            oceny += f"{row[0]} "
        elif row[1] != przedmiot and uczen == f"{row[3]} {row[2]}":
            print(f"{przedmiot}\n{oceny}")
            przedmiot = row[1]
            oceny = str(f"{row[0]} ")
        elif uczen != f"{row[3]} {row[2]}":
            uczen = f"{row[3]} {row[2]}"
            uczniowie.append(uczen.lower())
            print(f"{przedmiot}\n{oceny}")
            przedmiot = row[1]
            oceny = str(f"{row[0]} ")
            print(f"\n{row[3]} {row[2]}")
    print(f"{row[1]}\n{row[0]}\n")
    if input("Naciśnij enter aby powrocic do menu glownego lub wpisz 'u' aby usunąć ocenę.").lower() == "u":
        usun_ocene(uczniowie, przedmioty)


def usun_ocene(uczniowie, przedmioty):
    imie = input("Podaj imie ucznia: ").lower()
    nazwisko = input("Podaj nazwisko ucznia: ").lower()
    if f"{nazwisko} {imie}" not in uczniowie:
        input("Źle podane imie i nazwisko lub uczen nie posiada jeszcze ocen lub nie masz uprawnień do edycji ocen tego ucznia.")
        return False

    for num, p in enumerate(przedmioty):
        print(f"{num + 1} - {p}")
    try:
        user_ch = int(input("Podaj numer przedmiotu z  którego chcesz wystawić ocenę: "))
    except:
        input("Podano błędny znak.")
        return False
    if user_ch > len(przedmioty) or user_ch < 1:
        print("Nie ma takiego numeru przedmiotu.")
        return False
    przedmiot = przedmioty[user_ch - 1]

    ocena = input("Podaj ocene do skasowania: ")
    try:
        ocena = int(ocena)
    except:
        input("Zły format danych, podaj cyfre.")
        return False

    mycursor.execute(f"DELETE FROM oceny WHERE id IN (select * from(SELECT oceny.id FROM oceny join uzytkownicy on oceny.id_ucznia = uzytkownicy.id WHERE imie = '{imie}' and nazwisko = '{nazwisko}' and ocena = {ocena} and przedmiot = '{przedmiot}' order by id desc LIMIT 1) temp_tab) order by RAND() LIMIT 1")
    mydb.commit()
    input("Wysłano żądanie do bazy danych.")


def menu(id_konta):
    os.system("cls")
    u_choice = input(txt.oceny_menu).lower()
    if u_choice == "d":
        wpisz_oceny(id_konta)
    elif u_choice == "p":
        wyswietl_wszystkie_oceny(id_konta)
    else:
        return False
