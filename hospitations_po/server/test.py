from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_get_protocol_details():
    response = client.get("/protokol/7")
    assert response.status_code == 200
    assert response.json() == {
        "date": "2022-02-06",
        "czy_zatwierdzony": False,
        "ocena": "negatywna",
        "uzasadnienie": "",
        "wnioski_i_zalecenia": "",
        "data_zapoznania": None,
        "czy_przeslany": False,
        "przedstawienie_ocena_fk": 0,
        "wyjasnienie_ocena_fk": 0,
        "realizacja_ocena_fk": 0,
        "inspiracja_ocena_fk": 0,
        "udzielenie_ocena_fk": 0,
        "stosowanie_ocena_fk": 0,
        "poslugiwanie_ocena_fk": 0,
        "panowanie_ocena_fk": 0,
        "tworzenie_ocena_fk": 0
    }

    response = client.get("/protokol/20")
    assert response.status_code == 404
    assert response.json() == {"detail": "Protocol not found"}


def test_get_prowadzacy_protocols():
    response = client.get("/protokoly/prowadzacy/1?user_id=1")
    assert response.status_code == 200
    assert response.json() == [{
        "date": "2022-01-10",
        "czy_zatwierdzony": True,
        "id": 1,
        "nr_kursu": "INZ-254542P",
        "nazwa_kursu": "Bazy danych",
        "ocena": "dostateczna"
    }]

    response = client.get("/protokoly/prowadzacy/20?user_id=20")
    assert response.status_code == 404
    assert response.json() == {"detail": "Protocols not found"}


def test_get_przewodniczacy_protocols():
    response = client.get("/protokoly/przewodniczacy/2?user_id=2")
    assert response.status_code == 200
    assert response.json() == [{
        "date": "2022-01-10",
        "czy_zatwierdzony": True,
        "id": 1,
        "nr_kursu": "INZ-254542P",
        "nazwa_kursu": "Bazy danych",
        "hospitowany_imie": "Tadeusz",
        "hospitowany_nazwisko": "Pudełko",
        "czy_przeslany": True
    }, {
        "date": "2022-02-02",
        "czy_zatwierdzony": False,
        "id": 3,
        "nr_kursu": "INZ00112233W",
        "nazwa_kursu": "Analiza 1",
        "hospitowany_imie": "Adam",
        "hospitowany_nazwisko": "Malysz",
        "czy_przeslany": True
    }, {
        "date": "2022-02-03",
        "czy_zatwierdzony": False,
        "id": 4,
        "nr_kursu": "INZ00112235C",
        "nazwa_kursu": "Algerbra 1",
        "hospitowany_imie": "Mariusz",
        "hospitowany_nazwisko": "Pudznianowski",
        "czy_przeslany": True
    }, {
        "date": "2022-02-04",
        "czy_zatwierdzony": True,
        "id": 5,
        "nr_kursu": "INZ00112236W",
        "nazwa_kursu": "Algerbra 2",
        "hospitowany_imie": "Stanisław",
        "hospitowany_nazwisko": "Tumulec",
        "czy_przeslany": True
    }, {
        "date": "2022-02-05",
        "czy_zatwierdzony": False,
        "id": 6,
        "nr_kursu": "INZ00112237W",
        "nazwa_kursu": "Logika",
        "hospitowany_imie": "Maria",
        "hospitowany_nazwisko": "Awaria",
        "czy_przeslany": False
    }]

    response = client.get("/protokoly/przewodniczacy/20?user_id=20")
    assert response.status_code == 404
    assert response.json() == {"detail": "Protocols not found"}


def test_get_course_from_protocols():
    response = client.get("/kurs/1?protokol_id=1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "uzytkownik_fk": 1,
        "nazwa": "Bazy danych",
        "kod": "INZ-254542P",
        "stopien_i_froma_studiow": "pierwszego stopia, stacjonarne",
        "forma_dydaktyczna": "Projekt",
        "termin": "poniedzialek 09:15-11:00 TP",
        "liczba_uczestnikow": 1,
        "miejsce": "A1 s129c",
        "jednostka_organizacyjna": "K1 cos",
        "semestr": "zimowy"
    }

    response = client.get("/kurs/20?protokol_id=20")
    assert response.status_code == 404
    assert response.json() == {"detail": "Kurs not found"}


def test_does_odwolanie_exist():
    response = client.get("/odwolanie/4?protokol_id=4")
    assert response.status_code == 200
    assert response.json() == True

    response = client.get("/odwolanie/20?protokol_id=314")
    assert response.status_code == 200
    assert response.json() == False


def test_create_odwolanie():
    response = client.post("/odwolanie/create/9/?user_id=2",
                           json={
                               "tekst": "string",
                               "data_odwolanie": "2022-02-01"
                           })
    assert response.status_code == 200
    assert response.json() == {
        "tekst": "string",
        "data_odwolanie": "2022-02-01",
        "uzytkownik_fk": 2,
        "protokol_fk": 9
    }

    r = client.post("/odwolanie/create/120/?user_id=120",
                    json={
                        "tekst": "string",
                        "data_odwolanie": "2022-02-01"
                    })
    assert r.status_code == 404
    assert r.json() == {"detail": "Protocol not found"}

    r = client.post("/odwolanie/create/1/?user_id=2",
                    json={
                        "tekst": "string",
                        "data_odwolanie": "2022-02-01"
                    })
    assert r.status_code == 409
    assert r.json() == {'detail': 'Protocol already approved'}


def test_get_hospitations_details():
    response = client.get("/hospitacja/detal/1")
    assert response.status_code == 200
    assert response.json() == {
        "date": "2022-01-10",
        "czy_zatwierdzony": True,
        "id": 1,
        "nr_kursu": "INZ-254542P",
        "nazwa_kursu": "Bazy danych",
        "hospitowany_imie": "Tadeusz",
        "hospitowany_nazwisko": "Pudełko",
        "czy_przeslany": True,
        "stopien_i_froma_studiow": "pierwszego stopia, stacjonarne",
        "forma_dydaktyczna": "Projekt",
        "termin": "poniedzialek 09:15-11:00 TP",
        "liczba_uczestnikow": 1,
        "miejsce": "A1 s129c",
        "jednostka_organizacyjna": "K1 cos"
    }

    response = client.get("/hospitacja/detal/20")
    assert response.status_code == 404
    assert response.json() == {"detail": "Hospitacja not found"}


def test_delete_odwolanie():
    response = client.delete("/odwolanie/delete/9?user_id=2")
    assert response.status_code == 200
    assert response.json() == True

    response = client.delete("/odwolanie/delete/900?user_id=200")
    assert response.status_code == 200
    assert response.json() == False


def test_protokol_set_true():
    response = client.put("/protokol/set_true/5")
    assert response.status_code == 200
    assert response.json() == True

    response = client.put("/protokol/set_true/1410")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Protocols not found'}


def test_get_hospitacje():
    response = client.get("/hospitacje/2?user_id=2")
    assert response.status_code == 200
    assert response.json() == [{
        "date": "2022-01-10",
        "czy_zatwierdzony": True,
        "id": 1,
        "nr_kursu": "INZ-254542P",
        "nazwa_kursu": "Bazy danych",
        "hospitowany_imie": "Tadeusz",
        "hospitowany_nazwisko": "Pudełko",
        "czy_przeslany": True
    }, {
        "date": "2022-02-02",
        "czy_zatwierdzony": True,
        "id": 2,
        "nr_kursu": "INZ00112233W",
        "nazwa_kursu": "Analiza 1",
        "hospitowany_imie": "Adam",
        "hospitowany_nazwisko": "Malysz",
        "czy_przeslany": True
    }, {
        "date": "2022-02-03",
        "czy_zatwierdzony": True,
        "id": 3,
        "nr_kursu": "INZ00112235C",
        "nazwa_kursu": "Algerbra 1",
        "hospitowany_imie": "Mariusz",
        "hospitowany_nazwisko": "Pudznianowski",
        "czy_przeslany": True
    }, {
        "date": "2022-02-04",
        "czy_zatwierdzony": True,
        "id": 4,
        "nr_kursu": "INZ00112236W",
        "nazwa_kursu": "Algerbra 2",
        "hospitowany_imie": "Stanisław",
        "hospitowany_nazwisko": "Tumulec",
        "czy_przeslany": True
    }, {
        "date": "2022-02-05",
        "czy_zatwierdzony": True,
        "id": 5,
        "nr_kursu": "INZ00112237W",
        "nazwa_kursu": "Logika",
        "hospitowany_imie": "Maria",
        "hospitowany_nazwisko": "Awaria",
        "czy_przeslany": True
    }]

    response = client.get("/hospitacje/1?user_id=1")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Protocols not found'}


def test_protokol_update():
    response = client.put("/protokol/update/290")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Protocols not found'}

    response = client.put("/protokol/update/9",
                          json={
                              "date": "2022-02-01",
                              "czy_zatwierdzony": True,
                              "ocena": "blad",
                              "uzasadnienie": "string",
                              "wnioski_i_zalecenia": "string",
                              "data_zapoznania": "2022-02-01",
                              "czy_przeslany": True,
                              "przedstawienie_ocena_fk": 0,
                              "wyjasnienie_ocena_fk": 0,
                              "realizacja_ocena_fk": 0,
                              "inspiracja_ocena_fk": 0,
                              "udzielenie_ocena_fk": 0,
                              "stosowanie_ocena_fk": 0,
                              "poslugiwanie_ocena_fk": 0,
                              "panowanie_ocena_fk": 0,
                              "tworzenie_ocena_fk": 0
                          })
    assert response.status_code == 500
    assert response.json() == {"detail": "Inner server error"}

    response = client.put("/protokol/update/9",
                          json={
                              "date": "2022-02-01",
                              "czy_zatwierdzony": True,
                              "ocena": "wzorowa",
                              "uzasadnienie": "string",
                              "wnioski_i_zalecenia": "string",
                              "data_zapoznania": "2022-02-01",
                              "czy_przeslany": False,
                              "przedstawienie_ocena_fk": 0,
                              "wyjasnienie_ocena_fk": 0,
                              "realizacja_ocena_fk": 0,
                              "inspiracja_ocena_fk": 0,
                              "udzielenie_ocena_fk": 0,
                              "stosowanie_ocena_fk": 0,
                              "poslugiwanie_ocena_fk": 0,
                              "panowanie_ocena_fk": 0,
                              "tworzenie_ocena_fk": 0
                          })
    assert response.status_code == 200
    assert response.json() == {
        "date": "2022-02-08",
        "czy_zatwierdzony": True,
        "ocena": "wzorowa",
        "uzasadnienie": "string",
        "wnioski_i_zalecenia": "string",
        "data_zapoznania": "2022-02-02",
        "czy_przeslany": False,
        "przedstawienie_ocena_fk": 0,
        "wyjasnienie_ocena_fk": 0,
        "realizacja_ocena_fk": 0,
        "inspiracja_ocena_fk": 0,
        "udzielenie_ocena_fk": 0,
        "stosowanie_ocena_fk": 0,
        "poslugiwanie_ocena_fk": 0,
        "panowanie_ocena_fk": 0,
        "tworzenie_ocena_fk": 0
    }

    response = client.put("/protokol/update/9",
                          json={
                              "date": "2022-02-01",
                              "czy_zatwierdzony": True,
                              "ocena": "string",
                              "uzasadnienie": "string",
                              "wnioski_i_zalecenia": "string",
                              "data_zapoznania": "2022-02-01",
                              "czy_przeslany": False,
                              "przedstawienie_ocena_fk": 0,
                              "wyjasnienie_ocena_fk": 0,
                              "realizacja_ocena_fk": 0,
                              "inspiracja_ocena_fk": 0,
                              "udzielenie_ocena_fk": 0,
                              "stosowanie_ocena_fk": 0,
                              "poslugiwanie_ocena_fk": 0,
                              "panowanie_ocena_fk": 0,
                              "tworzenie_ocena_fk": 0
                          })
    assert response.status_code == 409
    assert response.json() == {"detail": "Unable to update"}


def test_protokol_update():
    response = client.put("/protokol/set_false/9")
    assert response.status_code == 200
    assert response.json() == True

    response = client.put("/protokol/set_false/1410")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Protocols not found'}
