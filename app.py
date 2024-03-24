import os
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

flask_host = os.environ.get('FLASK_HOST')
flask_port = os.environ.get('FLASK_PORT')


questions = [
    {
        "id": "1",
        "question": "Jakiej jesteś płci?",
        "answers": ["a) Kobieta", "b) Mężczyzna"],
        "type": "radio"
    },
    {
        "id": "2",
        "question": "Ile masz lat?",
        "answers": ["a) 13 lub mniej", "b) 14-16", "c) 17-19", "d) 20-22", "e) 23-25", "f) 26 lub więcej"],
        "type": "radio"
    },
    {
        "id": "3",
        "question": "Na jakim etapie edukacji jesteś?",
        "answers": ["a) Podstawowym", "b) Średnim", "c) Wyższym"],
        "type": "radio"
    },
    {
        "id": "4",
        "question": "Do jakiej szkoły/uczelni uczęszczasz?",
        "answers": ["a) Politechnika Gdańska", "b) Inna"],
        "type": "radio"
    },
    {
        "id": "5",
        "question": "Jaki był Twój stopień aktywności przed pandemią?(1-bardzo zły; 5-bardzo dobry)",
        "answers": ["a) 1", "b) 2", "c) 3", "d) 4", "e) 5"],
        "type": "radio"
    },
    {
        "id": "6",
        "question": "W jakim stopniu Twoja aktywność fizyczna spadła kiedy zaczęła się pandemia? (1-ani trochę, 5-drastycznie) ",
        "answers": ["a) 1", "b) 2", "c) 3", "d) 4", "e) 5"],
        "type": "radio"
    },
    {
        "id": "7",
        "question": "Ile godzin tygodniowo poświęcałeś na sport przed pandemią? ",
        "answers": ["a) 1-2h", "b) 3-5h", "c) 6-7h", "d) więcej"],
        "type": "radio"
    },
    {
        "id": "8",
        "question": "Ile godzin tygodniowo poświęcałeś na sport w trakcie trwania pandemii? ",
        "answers": ["a) 1-2h", "b) 3-5h", "c) 6-7h", "d) więcej"],
        "type": "radio"
    },
    {
        "id": "9",
        "question": "Ile kroków robiłeś dziennie przed pandemią?",
        "answers": ["a) Do 5000", "b) 5000-10000", "c)Ponad 10000", "d)Nie wiem"],
        "type": "radio"
    },
    {
        "id": "10",
        "question": "Ile kroków dziennie robiłeś w czasie pandemii?",
        "answers": ["a) Do 5000", "b) 5000-10000", "c)Ponad 10000", "d)Nie wiem"],
        "type": "radio"
    },
    {
        "id": "11",
        "question": "Czy jesteś zadowolony/a ze zdalnego nauczania?",
        "answers": ["a) Tak", "b) Nie", "c) ciężko stwierdzić"],
        "type": "radio"
    },
    {
        "id": "12",
        "question": "Czy podczas nauki zdalnej brakuje Ci kontaktu z rówieśnikami? ",
        "answers": ["a) Tak", "b) Nie", "c) Czasami"],
        "type": "radio"
    },
    {
        "id": "13",
        "question": "Gdzie Ci się lepiej uczy?",
        "answers": ["a) W domu", "b) W szkole", "c) Hybrydowo (trochę zdalnie, trochę stacjonarnie)"],
        "type": "radio"
    },
    {
        "id": "14",
        "question": "W jakim stopniu czujesz się obciążony ilością nauki? (1-mało, 5-bardzo)",
        "answers": ["a) 1", "b) 2", "c) 3", "d) 4", "e) 5"],
        "type": "radio"
    },
    {
        "id": "15",
        "question": "Czy Twoje zdrowie psychiczne ucierpiało z powodu pandemii?",
        "answers": ["a) Tak", "b) Nie", "c) Nie wiem"],
        "type": "radio"
    },
    {
        "id": "16",
        "question": "Jakie negatywne skutki pandemii obserwujesz u siebie?",
        "answers": ["a) Obniżenie nastroju", "b) Brak energii", "c) Ciągłe zmęczenie", "d) Trudności ze snem", "e) Lęk", "f) Uczucie niepokoju", "g) Trudności w kontaktach z ludźmi", "h) Nie odczuwam negatywnych skutków pandemii"],
        "type": "checkbox"
    },
    {
        "id": "17",
        "question": "Co było dla Ciebie najtrudniejsze w okresie pandemii?",
        "answers": ["a) Izolacja społeczna", "b) Nerwowa atmosfera w domu", "c) Zdalne nauczanie", "d) Zbyt wiele godzin spędzonych przy komputerze", "e) Brak kontaktu z innymi osobami", "f) Obawa o zachorowanie swoje lub bliskich", "g) Wszystko było idealnie zorganizowane"],
        "type": "checkbox"
    },
    {
        "id": "18",
        "question": "Czy doświadczyłeś/aś w okresie pandemii cyberprzemocy ze strony rówieśników (obrażanie, wyśmiewanie itp. w internecie)",
        "answers": ["a) tak", "b) nie"],
        "type": "radio"
    },
    {
        "id": "19",
        "question": "Co pomagało Ci w okresie pandemii?",
        "answers": ["a) Wsparcie innych osób", "b) Aktywność fizyczna", "c) Hobby", "d) Praktyki religijne", "e) Inne"],
        "type": "checkbox"
    },
    {
        "id": "20",
        "question": "Czy miałeś/aś wystarczające wsparcie innych osób?",
        "answers": ["a) tak", "b) nie"],
        "type": "radio"
    },
    {
        "id": "21",
        "question": "Kto Cię wspierał?",
        "answers": ["a) Rodzice", "b) Inni członkowie rodziny", "c) Przyjaciele", "d) Nauczyciele", "e) Pedagog lub psycholog", "f) Inne osoby", "g) nikt"],
        "type": "checkbox"
    },
    {
        "id": "22",
        "question": "Czy w okresie nauki zdalnej miałeś/miałaś możliwość prowadzenia rozmów za pomocą urządzeń elektronicznych z koleżankami, kolegami z klasy?",
        "answers": ["a) Tak, wiele razy", "b) Tak, kilka razy", "c) Nie"],
        "type": "radio"
    },
    {
        "id": "23",
        "question": "Jak oceniasz swoje relacje z rówieśnikami po okresie nauki zdalnej?",
        "answers": ["a) Mam lepsze relacje", "b) Relacje pozostają bez zmian", "c) Moje relacje się pogorszyły"],
        "type": "radio"
    },
    {
        "id": "24",
        "question": "Myśląc o Twojej szkole/uczelni które stwierdzenie najlepiej oddaje doświadczenie nauczycieli w zakresie nauczania online?",
        "answers": ["a) Posiadają bogate doświadczenie w nauczaniu online", "b) Jest to ich pierwsza styczność z nauczaniem zdalnym i sobie z tym radzą", "c) Jest to ich pierwsza styczność z nauczaniem zdalnym i sobie z tym nie radzą"],
        "type": "radio"
    },
    {
        "id": "25",
        "question": "Jakie są Twoim zdaniem największe wyzwania dla nauczycieli związane z przejściem do nauki online/zdalnej? ",
        "answers": ["a) Technologie (brak odpowiedniego sprzętu u nauczycieli albo uczniów)", "b) Komunikacja", "c) Brak przeszkoleń w nauce online", "d) Brak wytycznych/wsparcia ze strony uczelni/szkoły", "e) Stres", "f) Zarządzanie czasem i organizacją", "g) Inne", "h) Brak"],
        "type": "checkbox"
    },
    {
        "id": "26",
        "question": "Czy podczas pandemii zdarzyło Ci się mieć problemy z dołączeniem na zajęcia online?",
        "answers": ["a) Tak, wiele razy", "b) Tak, kilka razy", "c) Nie"],
        "type": "radio"
    },
    {
        "id": "27",
        "question": "W jakim stopniu zmienił się stan Twojej wiedzy w wyniku nauki zdalnej?",
        "answers": ["a) Znacznie się poprawił", "b) Poprawił się, lecz niewiele", "c) Pozostał bez zmian"],
        "type": "radio"
    },
    {
        "id": "28",
        "question": "Jak bardzo jesteś zadowolony/-a ze zdalnych lekcji? (1-bardzo niezadowolony, 5-bardzo zadowolony)",
        "answers": ["a) 1", "b) 2", "c) 3", "d) 4", "e) 5"],
        "type": "radio"
    },
    {
        "id": "29",
        "question": "Czy w Twojej szkole została utrzymana organizacja zajęć dodatkowych (kół zainteresowań naukowych) w formie zdalnej?",
        "answers": ["a) Tak", "b) Nie", "c) Nie wiem"],
        "type": "radio"
    }

]

@app.route("/", methods=['POST', 'GET'])
def survey():
    if request.method == 'GET':
        return render_template("index.html", data=questions)
    else:
        connection = sqlite3.connect("/home/hoddogaw/mysite/database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id_dane FROM dane_osobowe ORDER BY id_dane DESC LIMIT 1")
        temp = cursor.fetchone()
        id_number = temp[0]+1

        sql = '''INSERT INTO dane_osobowe(plec,wiek,etap_edukacji,szkola) VALUES (?,?,?,?)'''

        data = (request.form[questions[0].get('id')], request.form[questions[1].get('id')], request.form[questions[2].get('id')], request.form[questions[3].get('id')])

        cursor.execute(sql, data)

        sql = '''INSERT INTO aktywnosc_fizyczna(aktywnosc_przed,aktywnosc_spadek,sport_przed,sport_w_trakcie,kroki_przed,kroki_w_trakcie,id_dane) VALUES (?,?,?,?,?,?,?)'''

        data = (request.form[questions[4].get('id')], request.form[questions[5].get('id')], request.form[questions[6].get('id')],
        request.form[questions[7].get('id')], request.form[questions[8].get('id')], request.form[questions[9].get('id')], id_number)
        cursor.execute(sql, data)

        sql = '''INSERT INTO stan_psychiczny(zadowolenie_ze_zdalnego,brak_kontaktu,preferowane_miejsce_nauki,obciazenie_nauka,zdrowie_ucierpialo,
        negatywne_skutki,najtrudniejsze_rzeczy,cyberprzemoc,co_pomagalo,wsparcie_innych,kto_wspieral,rozmowy_wideo,relacje,id_dane) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

        data = (request.form[questions[10].get('id')], request.form[questions[11].get('id')], request.form[questions[12].get('id')],
        request.form[questions[13].get('id')], request.form[questions[14].get('id')])

        data_temp = ''
        data_checkbox = request.form.getlist(questions[15].get('id'))
        for d in data_checkbox:
            data_temp += d + ','
        data += (data_temp,)

        data_temp = ''
        data_checkbox = request.form.getlist(questions[16].get('id'))
        for d in data_checkbox:
            data_temp += d + ','
        data += (data_temp,)

        data += (request.form[questions[17].get('id')],)

        data_temp = ''
        data_checkbox = request.form.getlist(questions[18].get('id'))
        for d in data_checkbox:
            data_temp += d + ','
        data += (data_temp,)

        data += (request.form[questions[19].get('id')],)

        data_temp = ''
        data_checkbox = request.form.getlist(questions[20].get('id'))
        for d in data_checkbox:
            data_temp += d + ','
        data += (data_temp,)

        data += (request.form[questions[21].get('id')], request.form[questions[22].get('id')],id_number)
        cursor.execute(sql, data)


        sql = '''INSERT INTO ocena_nauczania(doswiadczenie_nauczycieli,wyzwania_nauczycieli,problem_z_dolaczeniem,stan_wiedzy,zadowolenie,utrzymanie_zajec,id_dane) VALUES (?,?,?,?,?,?,?)'''

        data = (request.form[questions[23].get('id')],)

        data_temp = ''
        data_checkbox = request.form.getlist(questions[24].get('id'))
        for d in data_checkbox:
            data_temp += d + ','
        data += (data_temp,)

        data += (request.form[questions[25].get('id')], request.form[questions[26].get('id')], request.form[questions[27].get('id')], request.form[questions[28].get('id')], id_number)

        cursor.execute(sql, data)

        connection.commit()
        return render_template('end.html')


if __name__ == "__main__":
    app.run(host=flask_host, port=flask_port)