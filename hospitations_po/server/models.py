from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.schema import CheckConstraint
from database import Base


class Rola(Base):
    __tablename__ = "rola"

    id = Column(Integer, primary_key=True, index=True)
    nazwa = Column(String, unique=True, nullable=False)


class Uzytkownik(Base):
    __tablename__ = "uzytkownik"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    haslo = Column(String, nullable=False)
    nr_telefonu = Column(String, nullable=False)
    email = Column(String, nullable=False)
    rola_fk = Column(Integer,
                     ForeignKey('rola.id'),
                     index=True,
                     nullable=False)
    imie = Column(String, nullable=False)
    nazwisko = Column(String, nullable=False)


class Komisja_hospitacyjna(Base):
    __tablename__ = "komisja_hospitacyjna"

    id = Column(Integer, primary_key=True, index=True)
    uzytkownik_fk = Column(Integer,
                           ForeignKey('uzytkownik.id'),
                           index=True,
                           nullable=False)


class Komisja_kospitacyjna_Uzytkownik(Base):
    __tablename__ = "komisja_kospitacyjna_uzytkownik"

    komisja_hospitacyjna_fk = Column(Integer,
                                     ForeignKey('komisja_hospitacyjna.id'),
                                     index=True,
                                     nullable=False,
                                     primary_key=True)
    uzytkownik_fk = Column(Integer,
                           ForeignKey('uzytkownik.id'),
                           index=True,
                           nullable=False,
                           primary_key=True)


class Ocena(Base):
    __tablename__ = "ocena"

    ocena = Column(Float, primary_key=True, unique=True)


class Protokol(Base):
    __tablename__ = "protokol"

    id = Column(Integer, primary_key=True, index=True)
    data_protokol = Column(Date, nullable=False)
    ocena = Column(String)
    uzasadnienie = Column(String)
    wnioski_i_zalecenia = Column(String)
    data_zapoznania = Column(Date)
    czy_zatwierdzona = Column(Boolean, nullable=False)
    czy_przeslany = Column(Boolean, nullable=False)
    przedstawienie_ocena_fk = Column(Float, ForeignKey('ocena.ocena'))
    wyjasnienie_ocena_fk = Column(Float, ForeignKey('ocena.ocena'))
    realizacja_ocena_fk = Column(Float, ForeignKey('ocena.ocena'))
    inspiracja_ocena_fk = Column(Float, ForeignKey('ocena.ocena'))
    udzielenie_ocena_fk = Column(Float, ForeignKey('ocena.ocena'))
    stosowanie_ocena_fk = Column(Float, ForeignKey('ocena.ocena'))
    poslugiwanie_ocena_fk = Column(Float, ForeignKey('ocena.ocena'))
    panowanie_ocena_fk = Column(Float, ForeignKey('ocena.ocena'))
    tworzenie_ocena_fk = Column(Float, ForeignKey('ocena.ocena'))


class Kurs(Base):
    __tablename__ = "kurs"

    id = Column(Integer, primary_key=True, index=True)
    uzytkownik_fk = Column(Integer,
                           ForeignKey('uzytkownik.id'),
                           index=True,
                           nullable=False)
    nazwa = Column(String, unique=True, nullable=False)
    kod = Column(String, unique=True, nullable=False)
    stopien_i_froma_studiow = Column(String, nullable=False)
    forma_dydaktyczna = Column(String, nullable=False)
    termin = Column(String, nullable=False)
    liczba_uczestnikow = Column(Integer, nullable=False)
    miejsce = Column(String, nullable=False)
    jednostka_organizacyjna = Column(String, nullable=False)
    semestr = Column(String, nullable=False)


class Uzytkownik_Kurs(Base):
    __tablename__ = "uzytkownik_kurs"

    kurs_fk = Column(Integer,
                     ForeignKey('kurs.id'),
                     index=True,
                     nullable=False,
                     primary_key=True)
    uzytkownik_fk = Column(Integer,
                           ForeignKey('uzytkownik.id'),
                           index=True,
                           nullable=False,
                           primary_key=True)


class Harmonogram(Base):
    __tablename__ = "harmonogram"

    id = Column(Integer, nullable=False, index=True, primary_key=True)
    semestr = Column(String(20), nullable=False)
    rok_akademicki = Column(String(10), nullable=False)
    data_zatwierdzenia = Column(Date)
    poczatek_semestru = Column(Date, nullable=False)
    koniec_semestru = Column(Date, nullable=False)


class Hospitacja(Base):
    __tablename__ = "hospitacja"

    id = Column(Integer, primary_key=True, index=True)
    komisja_hospitacyjna_fk = Column(Integer,
                                     ForeignKey('komisja_hospitacyjna.id'),
                                     index=True,
                                     nullable=False)
    harmonogram_fk = Column(Integer,
                            ForeignKey('harmonogram.id'),
                            index=True,
                            nullable=False)
    uzytkownik_fk = Column(Integer,
                           ForeignKey('uzytkownik.id'),
                           index=True,
                           nullable=False)
    data_hospitacji = Column(Date, nullable=False)
    kurs_fk = Column(Integer,
                     ForeignKey('kurs.id'),
                     index=True,
                     nullable=False)
    protokol_fk = Column(Integer,
                         ForeignKey('protokol.id'),
                         index=True,
                         nullable=False)


class Odwolanie(Base):
    __tablename__ = "odwolanie"

    id = Column(Integer, primary_key=True, index=True)
    uzytkownik_fk = Column(Integer,
                           ForeignKey('uzytkownik.id'),
                           index=True,
                           nullable=False)
    data_odwolanie = Column(Date, nullable=False)
    tekst = Column(String, nullable=False)
    protokol_fk = Column(Integer,
                         ForeignKey('protokol.id'),
                         index=True,
                         nullable=False)
