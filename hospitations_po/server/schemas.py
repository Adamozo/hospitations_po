from numbers import Real
from tokenize import Double
from typing import List, Optional
from unicodedata import numeric
from xmlrpc.client import Boolean
from pydantic import BaseModel
from datetime import date, datetime


class OdwolanieBase(BaseModel):
    tekst: str
    data_odwolanie: date


class OdwolanieCreate(OdwolanieBase):

    class Config:
        orm_mode = True


class Odwolanie(OdwolanieBase):
    uzytkownik_fk: int
    protokol_fk: int

    class Config:
        orm_mode = True


class ProtokolBase(BaseModel):
    date: date
    czy_zatwierdzony: Boolean


class ProtokolCreate(ProtokolBase):

    class Config:
        orm_mode = True


class Protokol(ProtokolBase):
    ocena: Optional[str] = None
    uzasadnienie: Optional[str] = None
    wnioski_i_zalecenia: Optional[str] = None
    data_zapoznania: Optional[date] = None
    czy_przeslany: Boolean
    przedstawienie_ocena_fk: Optional[float] = None
    wyjasnienie_ocena_fk: Optional[float] = None
    realizacja_ocena_fk: Optional[float] = None
    inspiracja_ocena_fk: Optional[float] = None
    udzielenie_ocena_fk: Optional[float] = None
    stosowanie_ocena_fk: Optional[float] = None
    poslugiwanie_ocena_fk: Optional[float] = None
    panowanie_ocena_fk: Optional[float] = None
    tworzenie_ocena_fk: Optional[float] = None

    class Config:
        orm_mode = True


class ProtokolShort(ProtokolBase):
    id: int
    nr_kursu: str
    nazwa_kursu: str
    ocena: Optional[str] = None


class ProtokolEdit(ProtokolBase):
    id: int
    nr_kursu: str
    nazwa_kursu: str
    hospitowany_imie: str
    hospitowany_nazwisko: str
    czy_przeslany: Boolean


class ProtokolDetails(ProtokolEdit):
    stopien_i_froma_studiow: str
    forma_dydaktyczna: str
    termin: str
    liczba_uczestnikow: int
    miejsce: str
    jednostka_organizacyjna: str


class Kurs(BaseModel):
    id: int
    uzytkownik_fk: int
    nazwa: str
    kod: str
    stopien_i_froma_studiow: str
    forma_dydaktyczna: str
    termin: str
    liczba_uczestnikow: int
    miejsce: str
    jednostka_organizacyjna: str
    semestr: str
