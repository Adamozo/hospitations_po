from cgitb import text
import json
from re import X
import tkinter as tk
from tkinter import Frame, messagebox
import tkinter.ttk as ttk
from typing import Any, Optional
import requests
from datetime import date
import os

CURRENT_DIRECTORY = os.getcwd()
SERVER_ADDRESS = 'http://127.0.0.1:8000'


def replace_frame(new_frame: ttk.Frame, container) -> None:
    container.frame.destroy()
    container.frame = new_frame    # type annotanion not suported tk.Frame
    container.frame.pack(fill="both", expand=True)


class YourHospitationsFrame(ttk.Frame):
    data: list[Any] = []

    def __init__(self, container) -> None:
        super().__init__(container)
        self.user_id: int = container.user_id
        self.get_data()
        self.frame_top: ttk.Frame = ttk.Frame(self, height=100)
        self.frame_top.pack(fill='x', side=tk.TOP)
        self.logout_button: tk.Button = tk.Button(
            self.frame_top,
            text='Wyloguj',
            bg='red',
            command=lambda: replace_frame(LoginFrame(container), container))
        self.logout_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.back_button: tk.Button = tk.Button(
            self.frame_top,
            text='Powrót',
            bg='blue',
            command=lambda: replace_frame(MenuFrame(container), container))
        self.back_button.pack(side=tk.LEFT, padx=1, pady=10)

        self.frame_name: tk.Label = tk.Label(self,
                                             text="Twoje hospitacje",
                                             font=('Arial', 25))
        self.frame_name.pack(padx=10)

        self.frame_main: tk.Frame = tk.Frame(self, width=1000, height=500)
        self.frame_main.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.hospitations_list: ttk.Treeview = ttk.Treeview(
            self.frame_main, height=5, selectmode="browse")
        self.hospitations_list['columns'] = (
            'numer protokołu', 'data hospitacji', 'kurs', 'ocena'
        )    # type annotatnion not suported

        self.hospitations_list.column('#0', width=0, stretch=tk.NO)
        self.hospitations_list.column('numer protokołu', anchor='e', width=100)
        self.hospitations_list.column('data hospitacji',
                                      anchor=tk.CENTER,
                                      width=150)
        self.hospitations_list.column('kurs', anchor='w', width=300)
        self.hospitations_list.column('ocena', anchor='e', width=100)

        self.hospitations_list.heading('#0', text='', anchor=tk.CENTER)
        self.hospitations_list.heading('numer protokołu',
                                       text='numer protokołu',
                                       anchor=tk.CENTER)
        self.hospitations_list.heading('data hospitacji',
                                       text='data hospitacji',
                                       anchor=tk.CENTER)
        self.hospitations_list.heading('kurs', text='kurs', anchor=tk.CENTER)
        self.hospitations_list.heading('ocena', text='ocena', anchor=tk.CENTER)
        self.hospitations_list.pack(side=tk.LEFT)

        self.sb: ttk.Scrollbar = ttk.Scrollbar(self.frame_main,
                                               orient=tk.VERTICAL)
        self.sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.hospitations_list.config(yscrollcommand=self.sb.set)
        self.sb.config(command=self.hospitations_list.yview)

        self.insert_into_list()

        self.frame_button: tk.Frame = tk.Frame(self, width=600)
        self.frame_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.select_button: tk.Button = tk.Button(
            self.frame_button,
            text='Wybierz',
            bg='aquamarine',
            fg='black',
            command=lambda: self.open_protocol(container),
            width=100)
        self.select_button.pack()

    def insert_into_list(self) -> None:
        size: int = len(self.data)

        for i in range(size):
            self.hospitations_list.insert(
                parent='',
                index=i,
                iid=str(i),
                values=(self.data[0]['id'], self.data[0]['date'],
                        self.data[0]['nr_kursu'] + ' ' +
                        self.data[0]['nazwa_kursu'],
                        "brak" if self.data[0]['ocena'] is None else
                        self.data[0]['ocena']))

    def get_data(self) -> None:
        # get base info
        base_info_response: json = requests.get(
            f'{SERVER_ADDRESS}/protokoly/prowadzacy/{self.user_id}?user_id={self.user_id}'
        )
        if (base_info_response.status_code == 200):
            self.data = base_info_response.json()

        elif (base_info_response.status_code == 404):
            messagebox.showinfo('Error', 'Nie masz hospitacji w bazie')

        else:
            messagebox.showinfo(
                'Error', 'Nie udało się pobrać danych z powodu błędu serwera')

    def open_protocol(self, container) -> None:
        try:
            temp: Optional[Any] = self.hospitations_list.item(
                self.hospitations_list.focus())
            protocol_id: int = int(temp['values'][0])
            protocol_frame: ProtocolPresentFrame = ProtocolPresentFrame(
                container, protocol_id)

            replace_frame(protocol_frame, container)

        except Exception as e:
            messagebox.showinfo('Error', 'Najpierw musisz wybrać opcje')


class ProtocolPresentFrame(ttk.Frame):
    protocol_data: Optional[Any] = None
    base_info: dict[str, Any] = {}

    def __init__(self, container, id: int) -> None:
        super().__init__(container)
        self.id: int = id
        self.protocol_details: dict[str, Any] = {}
        res: bool = self.get_protocol_data()
        self.frame_top: ttk.Frame = ttk.Frame(self, height=100)
        self.frame_top.pack(fill='x', side=tk.TOP)
        self.logout_button = tk.Button(
            self.frame_top,
            text='Wyloguj',
            bg='red',
            command=lambda: replace_frame(LoginFrame(container), container))
        self.logout_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.back_button: tk.Button = tk.Button(
            self.frame_top,
            text='Powrót',
            bg='blue',
            command=lambda: replace_frame(YourHospitationsFrame(container),
                                          container))
        self.back_button.pack(side=tk.LEFT, padx=1, pady=10)

        self.frame_main: ttk.Frame = ttk.Frame(self)
        self.frame_main.pack(fill=tk.BOTH, expand=1)

        self.canvas: tk.Canvas = tk.Canvas(self.frame_main)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.sb: ttk.Scrollbar = ttk.Scrollbar(self.frame_main,
                                               orient=tk.VERTICAL,
                                               command=self.canvas.yview)
        self.sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.sb.set)

        self.canvas.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.
                                                           canvas.bbox("all")))

        self.frame_protocol: ttk.Frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0),
                                  window=self.frame_protocol,
                                  anchor='n')

        if res:
            self.setup_base_info()
            self.marks_table()

        self.appeal_button: tk.Button = tk.Button(
            self.frame_top,
            text='Odwołaj się',
            command=lambda: replace_frame(AppealFrame(container, id), container
                                          ))
        self.appeal_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.accept_button: tk.Button = tk.Button(
            self.frame_top,
            text='Zatwierdź',
            command=lambda: self.accept_hospitation())
        self.accept_button.pack(side=tk.RIGHT, padx=6, pady=10)

        if self.protocol_details['czy_zatwierdzony'] or requests.get(
                f'{SERVER_ADDRESS}/odwolanie/{self.id}?protokol_id={self.id}'
        ).json():
            self.appeal_button.configure(state=tk.DISABLED)

        if self.protocol_details['czy_zatwierdzony']:
            self.accept_button.configure(state=tk.DISABLED)

        self.frame_name: tk.Label = tk.Label(self.frame_top,
                                             text=f"Protokół numer: {id}",
                                             font=('Arial', 25))
        self.frame_name.pack(padx=10)

    def accept_hospitation(self) -> None:
        succes: json = requests.put(
            f'{SERVER_ADDRESS}/protokol/set_true/{self.id}').json()
        if not succes:
            messagebox.showinfo("Error 500", "Internal server error")

        else:
            self.accept_button.configure(state=tk.DISABLED)

    def setup_base_info(self) -> None:
        self.frame_base_info: ttk.Frame = ttk.Frame(self.frame_protocol)
        tk.Label(self.frame_base_info,
                 text="Informacje wstępne",
                 font=('Arial', 20, 'underline')).grid(row=0,
                                                       column=0,
                                                       padx=100,
                                                       pady=20,
                                                       sticky='w')

        tk.Label(self.frame_base_info, text="Nazwa kursu:",
                 font=('Arial', 16)).grid(row=1,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['nazwa'],
                 font=('Arial', 16)).grid(row=1,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info, text="Kod kursu:",
                 font=('Arial', 16)).grid(row=2,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['kod'],
                 font=('Arial', 16)).grid(row=2,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info,
                 text="Forma dydaktyczna:",
                 font=('Arial', 16)).grid(row=3,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['forma_dydaktyczna'],
                 font=('Arial', 16)).grid(row=3,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info,
                 text="Stopień i forma studiów:",
                 font=('Arial', 16)).grid(row=4,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['stopien_i_froma_studiow'],
                 font=('Arial', 16)).grid(row=4,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info, text="Semestr:",
                 font=('Arial', 16)).grid(row=5,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['semestr'],
                 font=('Arial', 16)).grid(row=5,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info,
                 text="Miejsce i termin:",
                 font=('Arial', 16)).grid(row=6,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['miejsce'] + ' ' +
                 self.base_info['termin'],
                 font=('Arial', 16)).grid(row=6,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info, text=" ",
                 font=('Arial', 20)).grid(row=7, column=0, padx=20, pady=20)

        self.frame_base_info.pack(fill=tk.X)

    def marks_table(self) -> None:
        self.frame_radio_table: ttk.Frame = ttk.Frame(self.frame_protocol)

        tk.Label(self.frame_radio_table,
                 text="Prowadzący",
                 font=('Arial', 20, 'underline')).grid(row=0,
                                                       column=0,
                                                       sticky='w',
                                                       pady=30)
        tk.Label(self.frame_radio_table,
                 text="Ocena",
                 font=('Arial', 16, 'underline')).grid(row=0,
                                                       column=1,
                                                       sticky='e',
                                                       padx=100)

        tk.Label(self.frame_radio_table,
                 text="Przedstawił temat, cel i zakres zajęć",
                 font=('Arial', 16)).grid(row=1, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text=f"{self.protocol_details['przedstawienie_ocena_fk']}",
                 font=('Arial', 16, 'underline')).grid(row=1, column=1)

        tk.Label(self.frame_radio_table,
                 text="Wyjaśnił w zrozumiały sposób omawiane zagadnienia",
                 font=('Arial', 16)).grid(row=2, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text=self.protocol_details['wyjasnienie_ocena_fk'],
                 font=('Arial', 16, 'underline')).grid(row=2, column=1)

        tk.Label(self.frame_radio_table,
                 text="Realizował zajęcia z zaangażowaniem",
                 font=('Arial', 16)).grid(row=3, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text=self.protocol_details['realizacja_ocena_fk'],
                 font=('Arial', 16, 'underline')).grid(row=3, column=1)

        tk.Label(
            self.frame_radio_table,
            text=
            "Inspirował studentów do samodzielnego myślenia (stawiania pytań, dyskusji, samodzielnego rozwiązywania problemów/zadań itp.)",
            font=('Arial', 16),
            wraplength=500,
            anchor='w').grid(row=4, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text=self.protocol_details['inspiracja_ocena_fk'],
                 font=('Arial', 16, 'underline')).grid(row=4, column=1)

        tk.Label(
            self.frame_radio_table,
            text=
            "Udzielał merytorycznie poprawnych odpowiedzi na pytania studentów",
            font=('Arial', 16),
            wraplength=500).grid(row=5, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text=self.protocol_details['udzielenie_ocena_fk'],
                 font=('Arial', 16, 'underline')).grid(row=5, column=1)

        tk.Label(
            self.frame_radio_table,
            text=
            "Stosował środki dydaktyczne adekwatne do celów i treści zajęć",
            font=('Arial', 16)).grid(row=6, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text=self.protocol_details['stosowanie_ocena_fk'],
                 font=('Arial', 16, 'underline')).grid(row=6, column=1)

        tk.Label(self.frame_radio_table,
                 text="Posługiwał się poprawnym językiem",
                 font=('Arial', 16)).grid(row=7, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text=self.protocol_details['poslugiwanie_ocena_fk'],
                 font=('Arial', 16, 'underline')).grid(row=7, column=1)

        tk.Label(self.frame_radio_table,
                 text="Panował nad dynamiką grupy",
                 font=('Arial', 16)).grid(row=8, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text=self.protocol_details['panowanie_ocena_fk'],
                 font=('Arial', 16, 'underline')).grid(row=8, column=1)

        tk.Label(self.frame_radio_table,
                 text="Tworzył pozytywną atmosferę na zajęciach",
                 font=('Arial', 16)).grid(row=9, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text=self.protocol_details['tworzenie_ocena_fk'],
                 font=('Arial', 16, 'underline')).grid(row=9, column=1)

        tk.Label(self.frame_radio_table, text=" ",
                 font=('Arial', 16)).grid(row=10,
                                          column=0,
                                          sticky='w',
                                          pady=30)

        tk.Label(self.frame_radio_table,
                 text="Ocena końcowa",
                 font=('Arial', 20, 'underline')).grid(row=11,
                                                       column=0,
                                                       sticky='w',
                                                       pady=30)
        tk.Label(self.frame_radio_table,
                 text=f"Ocena:    {self.protocol_details['ocena']}",
                 font=('Arial', 16)).grid(row=12, column=0, sticky='w')

        tk.Label(self.frame_radio_table,
                 text="Uzasadnienie oceny końcowej",
                 font=('Arial', 20, 'underline')).grid(row=14,
                                                       column=0,
                                                       sticky='w',
                                                       pady=30)
        tk.Label(self.frame_radio_table,
                 text=self.protocol_details['uzasadnienie'],
                 font=('Arial', 15)).grid(row=15,
                                          column=0,
                                          sticky='w',
                                          pady=30)
        tk.Label(self.frame_radio_table, text=" ",
                 font=('Arial', 16)).grid(row=16,
                                          column=0,
                                          sticky='w',
                                          pady=30)

        tk.Label(self.frame_radio_table,
                 text="Wnioski i zalecenia",
                 font=('Arial', 20, 'underline')).grid(row=17,
                                                       column=0,
                                                       sticky='w',
                                                       pady=30)
        tk.Label(self.frame_radio_table,
                 text=self.protocol_details['wnioski_i_zalecenia'],
                 font=('Arial', 15)).grid(row=18,
                                          column=0,
                                          sticky='w',
                                          pady=30)
        tk.Label(self.frame_radio_table, text=" ",
                 font=('Arial', 16)).grid(row=19, column=0, pady=30)

        self.frame_radio_table.pack(fill=tk.X, padx=100)

    def get_protocol_data(self) -> bool:
        base_info_response: json = requests.get(
            f'{SERVER_ADDRESS}/kurs/{self.id}?protokol_id={self.id}')
        if (base_info_response.status_code == 200):
            self.base_info: dict[str, Any] = base_info_response.json()

            prot_inf: json = requests.get(
                f'{SERVER_ADDRESS}/protokol/{self.id}?protokol_id={self.id}')

            if (prot_inf.status_code == 200):
                self.protocol_details = prot_inf.json()
                return True

            elif (prot_inf.status_code == 404):
                messagebox.showinfo('Error 404',
                                    'Nie znaleziono szczegółów protokołu')

            else:
                messagebox.showinfo('Error 500',
                                    'Serwer nie może przetworzyć zapytania')

            return False

        elif (base_info_response.status_code == 404):
            messagebox.showinfo(
                'Error 404', 'Nie znaleziono szczegółów hospitowanego kursu')

        else:
            messagebox.showinfo('Error 500',
                                'Serwer nie może przetworzyć zapytania')

        return False


class AppealFrame(ttk.Frame):

    def __init__(self, container, protocol_id: int) -> None:
        super().__init__(container)
        self.protocol_id: int = protocol_id
        self.user_id: int = container.user_id
        self.date: str = date.today().strftime("%Y-%m-%d")

        self.frame_top: ttk.Frame = ttk.Frame(self, height=100)
        self.frame_top.pack(fill='x', side=tk.TOP)
        self.logout_button: tk.Button = tk.Button(
            self.frame_top,
            text='Wyloguj',
            bg='red',
            command=lambda: replace_frame(LoginFrame(container), container))
        self.logout_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.back_button: tk.Button = tk.Button(
            self.frame_top,
            text='Powrót',
            bg='blue',
            command=lambda: replace_frame(
                ProtocolPresentFrame(container, self.protocol_id), container))
        self.back_button.pack(side=tk.LEFT, padx=1, pady=10)

        self.send_button: tk.Button = tk.Button(self.frame_top,
                                                text='Prześlij',
                                                command=lambda: self.apply())
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.label_name: tk.Label = tk.Label(
            self,
            text=f"Odwołanie do protokołu numer: {self.protocol_id}",
            font=('Arial', 25))
        self.label_name.pack(padx=10)

        self.frame_main: ttk.Frame = ttk.Frame(self)
        self.frame_main.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.appeal_text: tk.Label = tk.Label(
            self.frame_main,
            text=
            f"Niniejszym odwołuje się od oceny na protokole numer: {self.protocol_id}, ponieważ:",
            font=('Arial', 17),
            anchor='w')
        self.appeal_text.grid(row=0, column=0, pady=30)

        self.appeal_reason: tk.Text = tk.Text(self.frame_main,
                                              bd=5,
                                              width=80,
                                              height=5,
                                              font=('Arial', 14))
        self.appeal_reason.grid(row=1, column=0, pady=10)

        self.label_date: tk.Label = tk.Label(self.frame_main,
                                             text=f'Data: {self.date}',
                                             font=('Arial', 17),
                                             anchor='e')
        self.label_date.grid(row=3, column=0, pady=30)

    def apply(self) -> None:
        r: json = requests.post(
            f'{SERVER_ADDRESS}/odwolanie/create/{self.protocol_id}/?user_id={self.user_id}',
            json={
                "tekst": str(self.appeal_reason.get('1.0', "end-1c")),
                "data_odwolanie": self.date
            })
        if r.status_code == 200:
            messagebox.showinfo('Success', 'Odwołanie zostało przesłane')
            self.send_button.configure(state=tk.DISABLED)

        elif r.status_code == 404:
            messagebox.showinfo('Error',
                                'Brak możliwości dodania odwołania do bazy')
            self.send_button.configure(state=tk.DISABLED)

        elif r.status_code == 409:
            messagebox.showinfo('Error',
                                'Brak możliwości dodania odwołania do bazy')
            self.send_button.configure(state=tk.DISABLED)

        else:
            messagebox.showinfo('Error', 'Błąd wewnętrzny serwera')


class EditProtocolFrame(ttk.Frame):
    protocol_data: Optional[Any] = None
    base_info: dict[str, Any] = {}

    def __init__(self, container, protocol_id: int, tutor: str) -> None:
        super().__init__(container)
        self.tutor: str = tutor
        self.protocol_id: int = protocol_id
        self.container = container
        self.final_mark: tk.StringVar = tk.StringVar()
        self.final_mark.set('negatywna')
        self.protocol_details: dict[str, Any] = {}
        res: bool = self.get_protocol_data()

        self.frame_main: ttk.Frame = ttk.Frame(self)
        self.frame_main.pack(fill=tk.BOTH, expand=1)

        self.canvas: tk.Canvas = tk.Canvas(self.frame_main)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.sb: ttk.Scrollbar = ttk.Scrollbar(self.frame_main,
                                               orient=tk.VERTICAL,
                                               command=self.canvas.yview)
        self.sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.sb.set)

        self.canvas.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.
                                                           canvas.bbox("all")))

        self.frame_protocol: ttk.Frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0),
                                  window=self.frame_protocol,
                                  anchor='n')

        if res:
            self.setup_frame_top(True)
            self.setup_base_info()
            self.setup_radio_table()
            self.setup_final_mark()
            self.setup_mark_reason()
            self.setup_conclusions()

        else:
            self.setup_frame_top(False)

    def setup_frame_top(self, is_enable) -> None:
        self.frame_top: tk.Frame = tk.Frame(self.frame_protocol, height=100)
        self.frame_top.pack(fill=tk.X, pady=10)
        self.logout_button: tk.Button = tk.Button(
            self.frame_top,
            text='Wyloguj',
            bg='red',
            command=lambda: replace_frame(LoginFrame(self.container), self.
                                          container))
        self.logout_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.back_button: tk.Button = tk.Button(
            self.frame_top,
            text='Powrót',
            bg='blue',
            command=lambda: replace_frame(
                GuidedHospitationsProtocols(self.container), self.container))
        self.back_button.pack(side=tk.LEFT, padx=1, pady=10)

        if is_enable:
            self.send_button: tk.Button = tk.Button(
                self.frame_top,
                text='Prześlij',
                command=lambda: self.send_action())
            self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)

            self.save_button: tk.Button = tk.Button(
                self.frame_top,
                text='Zapisz',
                command=lambda: self.save_action())
            self.save_button.pack(side=tk.RIGHT, pady=10)

        else:
            self.send_button: tk.Button = tk.Button(
                self.frame_top,
                text='Prześlij',
                command=lambda: self.send_action(),
                state=tk.DISABLED)
            self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)

            self.save_button: tk.Button = tk.Button(
                self.frame_top,
                text='Zapisz',
                command=lambda: self.save_action(),
                state=tk.DISABLED)
            self.save_button.pack(side=tk.RIGHT, pady=10)

        self.label_name: tk.Label = tk.Label(
            self.frame_top,
            text=f"Wypełnianie protokołu numer: {self.protocol_id}",
            font=('Arial', 25))
        self.label_name.pack(padx=190)

    def setup_base_info(self) -> None:
        self.frame_base_info: ttk.Frame = ttk.Frame(self.frame_protocol)
        tk.Label(self.frame_base_info,
                 text="Informacje wstępne",
                 font=('Arial', 20, 'underline')).grid(row=0,
                                                       column=0,
                                                       padx=100,
                                                       pady=20,
                                                       sticky='w')

        tk.Label(self.frame_base_info,
                 text="Prowadzący zajęcia:",
                 font=('Arial', 16)).grid(row=1,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info, text=self.tutor,
                 font=('Arial', 16)).grid(row=1,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info, text="Nazwa kursu:",
                 font=('Arial', 16)).grid(row=2,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['nazwa'],
                 font=('Arial', 16)).grid(row=2,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info, text="Kod kursu:",
                 font=('Arial', 16)).grid(row=3,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['kod'],
                 font=('Arial', 16)).grid(row=3,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info,
                 text="Forma dydaktyczna:",
                 font=('Arial', 16)).grid(row=4,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['forma_dydaktyczna'],
                 font=('Arial', 16)).grid(row=4,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info,
                 text="Stopień i forma studiów:",
                 font=('Arial', 16)).grid(row=5,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['stopien_i_froma_studiow'],
                 font=('Arial', 16)).grid(row=5,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info, text="Semestr:",
                 font=('Arial', 16)).grid(row=6,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['semestr'],
                 font=('Arial', 16)).grid(row=6,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info,
                 text="Miejsce i termin:",
                 font=('Arial', 16)).grid(row=7,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['miejsce'] + ' ' +
                 self.base_info['termin'],
                 font=('Arial', 16)).grid(row=7,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        # empty line of (n-1) + 20 + n pixels
        tk.Label(self.frame_base_info, text=" ",
                 font=('Arial', 20)).grid(row=8, column=0, padx=20, pady=20)

        self.frame_base_info.pack(fill=tk.X)

    def setup_radio_table(self) -> None:
        self.frame_radio_table: ttk.Frame = ttk.Frame(self.frame_protocol)

        tk.Label(self.frame_radio_table,
                 text="Prowadzący",
                 font=('Arial', 20, 'underline')).grid(row=0,
                                                       column=0,
                                                       sticky='w',
                                                       pady=30)
        tk.Label(self.frame_radio_table,
                 text="Ocena",
                 font=('Arial', 16, 'underline')).grid(row=0,
                                                       column=1,
                                                       sticky='e',
                                                       padx=100)

        tk.Label(self.frame_radio_table,
                 text="Przedstawił temat, cel i zakres zajęć",
                 font=('Arial', 16)).grid(row=1, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text="Wyjaśnił w zrozumiały sposób omawiane zagadnienia",
                 font=('Arial', 16)).grid(row=2, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text="Realizował zajęcia z zaangażowaniem",
                 font=('Arial', 16)).grid(row=3, column=0, sticky='w', pady=10)
        tk.Label(
            self.frame_radio_table,
            text=
            "Inspirował studentów do samodzielnego myślenia (stawiania pytań, dyskusji, samodzielnego rozwiązywania problemów/zadań itp.)",
            font=('Arial', 16),
            wraplength=500,
            anchor='w').grid(row=4, column=0, sticky='w', pady=10)
        tk.Label(
            self.frame_radio_table,
            text=
            "Udzielał merytorycznie poprawnych odpowiedzi na pytania studentów",
            font=('Arial', 16),
            wraplength=500).grid(row=5, column=0, sticky='w', pady=10)
        tk.Label(
            self.frame_radio_table,
            text=
            "Stosował środki dydaktyczne adekwatne do celów i treści zajęć",
            font=('Arial', 16)).grid(row=6, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text="Posługiwał się poprawnym językiem",
                 font=('Arial', 16)).grid(row=7, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text="Panował nad dynamiką grupy",
                 font=('Arial', 16)).grid(row=8, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table,
                 text="Tworzył pozytywną atmosferę na zajęciach",
                 font=('Arial', 16)).grid(row=9, column=0, sticky='w', pady=10)
        tk.Label(self.frame_radio_table, text=" ",
                 font=('Arial', 16)).grid(row=10,
                                          column=0,
                                          sticky='w',
                                          pady=30)

        self.marks: list[tk.StringVar] = [
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar()
        ]
        self.marks[0].set('0') if self.protocol_details[
            'przedstawienie_ocena_fk'] is None else self.marks[0].set(
                str(self.protocol_details['przedstawienie_ocena_fk']))
        self.marks[1].set('0') if self.protocol_details[
            'wyjasnienie_ocena_fk'] is None else self.marks[1].set(
                str(self.protocol_details['wyjasnienie_ocena_fk']))
        self.marks[2].set('0') if self.protocol_details[
            'realizacja_ocena_fk'] is None else self.marks[2].set(
                str(self.protocol_details['realizacja_ocena_fk']))
        self.marks[3].set('0') if self.protocol_details[
            'inspiracja_ocena_fk'] is None else self.marks[3].set(
                str(self.protocol_details['inspiracja_ocena_fk']))
        self.marks[4].set('0') if self.protocol_details[
            'udzielenie_ocena_fk'] is None else self.marks[4].set(
                str(self.protocol_details['udzielenie_ocena_fk']))
        self.marks[5].set('0') if self.protocol_details[
            'stosowanie_ocena_fk'] is None else self.marks[5].set(
                str(self.protocol_details['stosowanie_ocena_fk']))
        self.marks[6].set('0') if self.protocol_details[
            'poslugiwanie_ocena_fk'] is None else self.marks[6].set(
                str(self.protocol_details['poslugiwanie_ocena_fk']))
        self.marks[7].set('0') if self.protocol_details[
            'panowanie_ocena_fk'] is None else self.marks[7].set(
                str(self.protocol_details['panowanie_ocena_fk']))
        self.marks[8].set('0') if self.protocol_details[
            'tworzenie_ocena_fk'] is None else self.marks[8].set(
                str(self.protocol_details['tworzenie_ocena_fk']))

        tk.OptionMenu(self.frame_radio_table, self.marks[0], '0', '2', '3',
                      '4', '5', '5.5').grid(row=1, column=1)
        tk.OptionMenu(self.frame_radio_table, self.marks[1], '0', '2', '3',
                      '4', '5', '5.5').grid(row=2, column=1)
        tk.OptionMenu(self.frame_radio_table, self.marks[2], '0', '2', '3',
                      '4', '5', '5.5').grid(row=3, column=1)
        tk.OptionMenu(self.frame_radio_table, self.marks[3], '0', '2', '3',
                      '4', '5', '5.5').grid(row=4, column=1)
        tk.OptionMenu(self.frame_radio_table, self.marks[4], '0', '2', '3',
                      '4', '5', '5.5').grid(row=5, column=1)
        tk.OptionMenu(self.frame_radio_table, self.marks[5], '0', '2', '3',
                      '4', '5', '5.5').grid(row=6, column=1)
        tk.OptionMenu(self.frame_radio_table, self.marks[6], '0', '2', '3',
                      '4', '5', '5.5').grid(row=7, column=1)
        tk.OptionMenu(self.frame_radio_table, self.marks[7], '0', '2', '3',
                      '4', '5', '5.5').grid(row=8, column=1)
        tk.OptionMenu(self.frame_radio_table, self.marks[8], '0', '2', '3',
                      '4', '5', '5.5').grid(row=9, column=1)

        self.frame_radio_table.pack(fill=tk.X, padx=100)

    def setup_final_mark(self) -> None:
        self.frame_final_mark: ttk.Frame = ttk.Frame(self.frame_protocol)
        self.frame_final_mark.grid_columnconfigure(1, minsize=150)
        tk.Label(self.frame_final_mark,
                 text="Ocena końcowa",
                 font=('Arial', 20, 'underline')).grid(row=0,
                                                       column=0,
                                                       sticky='w',
                                                       pady=30)
        self.mark_label: tk.Label = tk.Label(self.frame_final_mark,
                                             text=f"Średnia ocen: ",
                                             font=(
                                                 'Arial',
                                                 16,
                                             ))
        self.mark_label.grid(row=1, column=0, sticky='w')
        tk.Button(self.frame_final_mark,
                  text='Policz',
                  command=lambda: self.count_mark_avg()).grid(row=1,
                                                              column=1,
                                                              sticky='e')
        tk.Label(self.frame_final_mark, text="Ocena ",
                 font=('Arial', 16)).grid(row=2, column=0, sticky='w')
        if self.protocol_details['ocena'] is not None:
            self.final_mark.set(self.protocol_details['ocena'])
        tk.OptionMenu(self.frame_final_mark, self.final_mark, 'negatywna',
                      'dostateczna', 'dobra', 'bardzo dobra',
                      'wzorowa').grid(row=2, column=1, sticky='e')
        tk.Label(self.frame_final_mark, text=" ",
                 font=('Arial', 16)).grid(row=3, column=0, pady=30)

        self.frame_final_mark.pack(fill=tk.X, padx=100)

    def setup_mark_reason(self) -> None:
        self.frame_reason_mark: ttk.Frame = ttk.Frame(self.frame_protocol)
        tk.Label(self.frame_reason_mark,
                 text="Uzasadnienie oceny końcowej",
                 font=('Arial', 20, 'underline')).grid(row=0,
                                                       column=0,
                                                       sticky='w',
                                                       pady=30)
        self.reason_mark: tk.Text = tk.Text(self.frame_reason_mark,
                                            bd=5,
                                            width=80,
                                            height=5,
                                            font=('Arial', 14))
        if self.protocol_details['uzasadnienie'] is not None:
            self.reason_mark.insert("end-1c",
                                    self.protocol_details['uzasadnienie'])
        self.reason_mark.grid(row=1, column=0, sticky='w')
        tk.Label(self.frame_reason_mark, text=" ",
                 font=('Arial', 16)).grid(row=3, column=0, pady=30)

        self.frame_reason_mark.pack(fill=tk.X, padx=100)

    def setup_conclusions(self) -> None:
        self.frame_conclusion: ttk.Frame = ttk.Frame(self.frame_protocol)
        tk.Label(self.frame_conclusion,
                 text="Wnioski i zalecenia",
                 font=('Arial', 20, 'underline')).grid(row=0,
                                                       column=0,
                                                       sticky='w',
                                                       pady=30)
        self.conclusions: tk.Text = tk.Text(self.frame_conclusion,
                                            bd=5,
                                            width=80,
                                            height=5,
                                            font=('Arial', 14))
        if self.protocol_details['wnioski_i_zalecenia'] is not None:
            self.conclusions.insert(
                "end-1c", self.protocol_details['wnioski_i_zalecenia'])
        self.conclusions.grid(row=1, column=0, sticky='w')
        tk.Label(self.frame_conclusion, text=" ",
                 font=('Arial', 16)).grid(row=3, column=0, pady=30)

        self.frame_conclusion.pack(fill=tk.X, padx=100)

    def get_protocol_data(self) -> bool:
        base_info_response: json = requests.get(
            f'{SERVER_ADDRESS}/kurs/{self.protocol_id}?protokol_id={self.protocol_id}'
        )
        if (base_info_response.status_code == 200):
            self.base_info: dict[str, Any] = base_info_response.json()

            prot_inf: json = requests.get(
                f'{SERVER_ADDRESS}/protokol/{self.protocol_id}/?protokol_id={self.protocol_id}'
            )

            if (prot_inf.status_code == 200):
                self.protocol_details = prot_inf.json()
                return True

            elif (prot_inf.status_code == 404):
                messagebox.showinfo('Error 404',
                                    'Nie znaleziono szczegółów protokołu')

            else:
                messagebox.showinfo('Error 500',
                                    'Serwer nie może przetworzyć zapytania')

            return False

        elif (base_info_response.status_code == 404):
            messagebox.showinfo(
                'Error 404', 'Nie znaleziono szczegółów hospitowanego kursu')

        else:
            messagebox.showinfo('Error 500',
                                'Serwer nie może przetworzyć zapytania')

        return False

    def count_mark_avg(self) -> None:
        sum: float = 0.0

        for mark in self.marks:
            sum += float(mark.get())

        self.mark_label.configure(
            text=f"Średnia ocen: {round(sum/len(self.marks), 2)}")
        self.mark_label.update()

    def save_action(self) -> None:
        r: json = requests.put(
            f'{SERVER_ADDRESS}/protokol/update/{self.protocol_id}',
            json={
                "date": self.protocol_details["date"],
                "czy_zatwierdzony": False,
                "ocena": self.final_mark.get(),
                "uzasadnienie": str(self.reason_mark.get('1.0', "end-1c")),
                "wnioski_i_zalecenia":
                str(self.conclusions.get('1.0', "end-1c")),
                "data_zapoznania": self.protocol_details["data_zapoznania"],
                "czy_przeslany": False,
                "przedstawienie_ocena_fk": float(self.marks[0].get()),
                "wyjasnienie_ocena_fk": float(self.marks[1].get()),
                "realizacja_ocena_fk": float(self.marks[2].get()),
                "inspiracja_ocena_fk": float(self.marks[3].get()),
                "udzielenie_ocena_fk": float(self.marks[4].get()),
                "stosowanie_ocena_fk": float(self.marks[5].get()),
                "poslugiwanie_ocena_fk": float(self.marks[6].get()),
                "panowanie_ocena_fk": float(self.marks[7].get()),
                "tworzenie_ocena_fk": float(self.marks[8].get())
            })

        if r.status_code == 200:
            messagebox.showinfo('Success', 'Zapisano zmiany w systemie')

        elif r.status_code == 404:
            messagebox.showinfo('Error', 'Nie znaleziono protokołu w bazie')

        elif r.status_code == 409:
            messagebox.showinfo('Error', 'Nie mozna zapisac zmian')

        else:
            messagebox.showinfo('Error', 'Błąd wewnętrzny serwera')

    def send_action(self) -> None:
        r: json = requests.put(
            f'{SERVER_ADDRESS}/protokol/update/{self.protocol_id}',
            json={
                "date": self.protocol_details["date"],
                "czy_zatwierdzony": False,
                "ocena": self.final_mark.get(),
                "uzasadnienie": str(self.reason_mark.get('1.0', "end-1c")),
                "wnioski_i_zalecenia":
                str(self.conclusions.get('1.0', "end-1c")),
                "data_zapoznania": self.protocol_details["data_zapoznania"],
                "czy_przeslany": True,
                "przedstawienie_ocena_fk": float(self.marks[0].get()),
                "wyjasnienie_ocena_fk": float(self.marks[1].get()),
                "realizacja_ocena_fk": float(self.marks[2].get()),
                "inspiracja_ocena_fk": float(self.marks[3].get()),
                "udzielenie_ocena_fk": float(self.marks[4].get()),
                "stosowanie_ocena_fk": float(self.marks[5].get()),
                "poslugiwanie_ocena_fk": float(self.marks[6].get()),
                "panowanie_ocena_fk": float(self.marks[7].get()),
                "tworzenie_ocena_fk": float(self.marks[8].get())
            })

        if r.status_code == 200:
            messagebox.showinfo('Success', 'Przesłano protokół')
            self.save_button.configure(state=tk.DISABLED)
            self.send_button.configure(state=tk.DISABLED)

        elif r.status_code == 404:
            messagebox.showinfo('Error', 'Nie znaleziono protokołu w bazie')

        elif r.status_code == 409:
            messagebox.showinfo('Error', 'Nie mozna zapisac zmian')

        else:
            messagebox.showinfo('Error', 'Błąd wewnętrzny serwera')


class GuidedHospitationsProtocols(ttk.Frame):

    def __init__(self, container) -> None:
        super().__init__(container)
        self.user_id: int = container.user_id
        self.protocols: list[dict[str, Any]] = []
        self.get_data()

        self.frame_top: ttk.Frame = ttk.Frame(self, height=100)
        self.frame_top.pack(fill='x', side=tk.TOP)
        self.logout_button: tk.Button = tk.Button(
            self.frame_top,
            text='Wyloguj',
            bg='red',
            command=lambda: replace_frame(LoginFrame(container), container))
        self.logout_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.back_button: tk.Button = tk.Button(
            self.frame_top,
            text='Powrót',
            bg='blue',
            command=lambda: replace_frame(MenuFrame(container), container))
        self.back_button.pack(side=tk.LEFT, padx=1, pady=10)

        self.frame_name: tk.Label = tk.Label(self,
                                             text="Protokoły z hospitacji",
                                             font=('Arial', 25))
        self.frame_name.pack(padx=10)

        self.frame_main: tk.Frame = tk.Frame(self, width=1000, height=500)
        self.frame_main.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.hospitations_list: ttk.Treeview = ttk.Treeview(
            self.frame_main, height=5, selectmode="browse")
        self.hospitations_list['columns'] = ('numer protokołu',
                                             'data hospitacji', 'kurs',
                                             'hospitowany', 'edytowalny'
                                             )    # type annotatnion error

        self.hospitations_list.column('#0', width=0, stretch=tk.NO)
        self.hospitations_list.column('numer protokołu', anchor='e', width=100)
        self.hospitations_list.column('data hospitacji',
                                      anchor=tk.CENTER,
                                      width=150)
        self.hospitations_list.column('kurs', anchor='w', width=300)
        self.hospitations_list.column('hospitowany', anchor='e', width=300)
        self.hospitations_list.column('edytowalny', anchor='e', width=80)

        self.hospitations_list.heading('#0', text='', anchor=tk.CENTER)
        self.hospitations_list.heading('numer protokołu',
                                       text='numer protokołu',
                                       anchor=tk.CENTER)
        self.hospitations_list.heading('data hospitacji',
                                       text='data hospitacji',
                                       anchor=tk.CENTER)
        self.hospitations_list.heading('kurs', text='kurs', anchor=tk.CENTER)
        self.hospitations_list.heading('hospitowany',
                                       text='hospitowany',
                                       anchor=tk.CENTER)
        self.hospitations_list.heading('edytowalny',
                                       text='edytowalny',
                                       anchor='e')
        self.hospitations_list.pack(side=tk.LEFT)

        self.sb: ttk.Scrollbar = ttk.Scrollbar(self.frame_main,
                                               orient=tk.VERTICAL)
        self.sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.hospitations_list.config(yscrollcommand=self.sb.set)
        self.sb.config(command=self.hospitations_list.yview)

        self.insert_into_list()

        self.frame_button: tk.Frame = tk.Frame(self, width=600)
        self.frame_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.select_button: tk.Button = tk.Button(
            self.frame_button,
            text='Wybierz',
            bg='aquamarine',
            fg='black',
            command=lambda: self.open_protocol(container),
            width=100)
        self.select_button.pack()

    def insert_into_list(self) -> None:
        protocols_num: int = len(self.protocols)

        for i in range(protocols_num):
            self.hospitations_list.insert(
                parent='',
                index=i,
                iid=str(i),
                values=(self.protocols[i]['id'], self.protocols[i]['date'],
                        self.protocols[i]['nr_kursu'] + ' ' +
                        self.protocols[i]['nazwa_kursu'],
                        self.protocols[i]['hospitowany_imie'] + ' ' +
                        self.protocols[i]['hospitowany_nazwisko'],
                        'Nie' if self.protocols[i]['czy_zatwierdzony']
                        or self.protocols[i]['czy_przeslany'] else 'Tak'))

    def open_protocol(self, container) -> None:
        try:
            temp: Optional[Any] = self.hospitations_list.item(
                self.hospitations_list.focus())
            if temp['values'][4] == 'Tak':
                protocol_id: int = int(temp['values'][0])
                protocol_frame: EditProtocolFrame = EditProtocolFrame(
                    container, protocol_id, temp['values'][3])
                replace_frame(protocol_frame, container)

            else:
                messagebox.showinfo('Bad value',
                                    'Protokół nie jest edytowalny')

        except Exception as e:
            messagebox.showinfo('Error', 'Najpierw musisz wybrać opcje')

    def get_data(self) -> None:
        base_info_response: json = requests.get(
            f'{SERVER_ADDRESS}/protokoly/przewodniczacy/{self.user_id}?user_id={self.user_id}'
        )
        if (base_info_response.status_code == 200):
            self.protocols = base_info_response.json()

        elif (base_info_response.status_code == 404):
            messagebox.showinfo('Error', 'Nie masz protokołów w bazie')

        else:
            messagebox.showinfo(
                'Error', 'Nie udało się pobrać danych z powodu błędu serwera')


class MenuFrame(ttk.Frame):

    def __init__(self, container: Any) -> None:
        super().__init__(container)

        self.frame_top: ttk.Frame = ttk.Frame(self, height=100)
        self.frame_top.pack(fill='x', side=tk.TOP)
        self.logout_button: tk.Button = tk.Button(
            self.frame_top,
            text='Wyloguj',
            bg='red',
            command=lambda: replace_frame(LoginFrame(container), container))
        self.logout_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.frame_main: tk.Frame = tk.Frame(self, width=600, height=500)
        self.frame_main.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.frame_main.grid_rowconfigure(0, minsize=200)
        self.frame_main.grid_rowconfigure(1, minsize=200)
        self.frame_main.grid_columnconfigure(0, minsize=250)
        self.frame_main.grid_columnconfigure(1, minsize=250)

        self.your_hospitations_img: tk.PhotoImage = tk.PhotoImage(
            file=os.path.join(CURRENT_DIRECTORY,
                              'hospitations_po/gui/icons/check_protocols.png'))
        self.account_img: tk.PhotoImage = tk.PhotoImage(file=os.path.join(
            CURRENT_DIRECTORY, 'hospitations_po/gui/icons/profile.png'))
        self.hospitations_timetable_img: tk.PhotoImage = tk.PhotoImage(
            file=os.path.join(
                CURRENT_DIRECTORY,
                'hospitations_po/gui/icons/hospitations_timetable.png')
        ).subsample(1, 1)
        self.hospitations_guided_img: tk.PhotoImage = tk.PhotoImage(
            file=os.path.join(
                CURRENT_DIRECTORY,
                'hospitations_po/gui/icons/hospitations_guided.png'))

        self.your_hospitations: tk.Button = tk.Button(
            self.frame_main,
            text='TWOJE HOSPITACJE',
            bg='aquamarine',
            fg='black',
            image=self.your_hospitations_img,
            compound=tk.TOP,
            command=lambda: replace_frame(YourHospitationsFrame(container),
                                          container))
        self.account: tk.Button = tk.Button(self.frame_main,
                                            text='PROFIL',
                                            bg='aquamarine',
                                            fg='black',
                                            image=self.account_img,
                                            compound=tk.TOP)
        self.hospitations_timetable: tk.Button = tk.Button(
            self.frame_main,
            text='TERMINARZ HOSPITACJI',
            bg='aquamarine',
            fg='black',
            image=self.hospitations_timetable_img,
            compound=tk.TOP,
            command=lambda: replace_frame(
                TimetableOfHospitationsFrame(container), container))
        self.hospitations_guided: tk.Button = tk.Button(
            self.frame_main,
            text='PROTOKOŁY Z HOSPITACJI',
            bg='aquamarine',
            fg='black',
            image=self.hospitations_guided_img,
            compound=tk.TOP,
            command=lambda: replace_frame(
                GuidedHospitationsProtocols(container), container))

        self.hospitations_timetable.grid(row=0,
                                         column=0,
                                         sticky='nsew',
                                         padx=10,
                                         pady=10)
        self.hospitations_guided.grid(row=1,
                                      column=0,
                                      sticky='nsew',
                                      padx=10,
                                      pady=10)
        self.your_hospitations.grid(row=0,
                                    column=1,
                                    sticky='nsew',
                                    padx=10,
                                    pady=10)
        self.account.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)


class LoginFrame(ttk.Frame):

    def __init__(self, container) -> None:
        super().__init__(container)

        self.label_top: ttk.Label = ttk.Label(
            self,
            text="Zaloguj się na jednego z użytkowników",
            font=('Arial', 25))
        self.label_top.pack(pady=40)

        self.buttons: tk.Frame = tk.Frame(self, width=400, height=300)
        self.buttons.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.button1: tk.Button = tk.Button(
            self.buttons,
            text='przewodniczacy komisji',
            bg='aquamarine',
            fg='black',
            command=lambda: button_action(2, container))
        self.button2: tk.Button = tk.Button(
            self.buttons,
            text='członek komisji',
            bg='aquamarine',
            fg='black',
            command=lambda: button_action(3, container))
        self.button3: tk.Button = tk.Button(
            self.buttons,
            text='nauczyciel',
            bg='aquamarine',
            fg='black',
            command=lambda: button_action(1, container))
        self.button4: tk.Button = tk.Button(
            self.buttons,
            text='nauczyciel',
            bg='aquamarine',
            fg='black',
            command=lambda: button_action(6, container))
        self.buttons.grid_rowconfigure(0, minsize=160)
        self.buttons.grid_rowconfigure(1, minsize=160)
        self.buttons.grid_columnconfigure(0, minsize=190)
        self.buttons.grid_columnconfigure(1, minsize=190)
        self.button1.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.button2.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        self.button3.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self.button4.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        def button_action(user_id: int, container) -> None:
            container.user_id = user_id    # type annoatanion error
            replace_frame(MenuFrame(container), container)


class TimetableOfHospitationsFrame(ttk.Frame):

    def __init__(self, container) -> None:
        super().__init__(container)
        self.user_id: int = container.user_id
        self.get_data()
        self.frame_top: ttk.Frame = ttk.Frame(self, height=100)
        self.frame_top.pack(fill='x', side=tk.TOP)
        self.logout_button: tk.Button = tk.Button(
            self.frame_top,
            text='Wyloguj',
            bg='red',
            command=lambda: replace_frame(LoginFrame(container), container))
        self.logout_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.back_button: tk.Button = tk.Button(
            self.frame_top,
            text='Powrót',
            bg='blue',
            command=lambda: replace_frame(MenuFrame(container), container))
        self.back_button.pack(side=tk.LEFT, padx=1, pady=10)

        self.frame_name: tk.Label = tk.Label(self,
                                             text="Terminarz hospitacji",
                                             font=('Arial', 25))
        self.frame_name.pack(padx=10)

        self.frame_main: tk.Frame = tk.Frame(self, width=1000, height=500)
        self.frame_main.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.hospitations_list: ttk.Treeview = ttk.Treeview(
            self.frame_main, height=5, selectmode="browse")
        self.hospitations_list['columns'] = ('numer hospitacji',
                                             'data hospitacji', 'kurs',
                                             'hospitowany'
                                             )    # type annotatnion error

        self.hospitations_list.column('#0', width=0, stretch=tk.NO)
        self.hospitations_list.column('numer hospitacji',
                                      anchor='e',
                                      width=100)
        self.hospitations_list.column('data hospitacji',
                                      anchor=tk.CENTER,
                                      width=150)
        self.hospitations_list.column('kurs', anchor='w', width=300)
        self.hospitations_list.column('hospitowany', anchor='e', width=150)

        self.hospitations_list.heading('#0', text='', anchor=tk.CENTER)
        self.hospitations_list.heading('numer hospitacji',
                                       text='numer hospitacji',
                                       anchor=tk.CENTER)
        self.hospitations_list.heading('data hospitacji',
                                       text='data hospitacji',
                                       anchor=tk.CENTER)
        self.hospitations_list.heading('kurs', text='kurs', anchor=tk.CENTER)
        self.hospitations_list.heading('hospitowany',
                                       text='hospitowany',
                                       anchor=tk.CENTER)
        self.hospitations_list.pack(side=tk.LEFT)

        self.sb: ttk.Scrollbar = ttk.Scrollbar(self.frame_main,
                                               orient=tk.VERTICAL)
        self.sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.hospitations_list.config(yscrollcommand=self.sb.set)
        self.sb.config(command=self.hospitations_list.yview)

        self.insert_into_list()

        self.frame_button: tk.Frame = tk.Frame(self, width=600)
        self.frame_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.select_button: tk.Button = tk.Button(
            self.frame_button,
            text='Wybierz',
            bg='aquamarine',
            fg='black',
            command=lambda: self.open_protocol(container),
            width=100)
        self.select_button.pack()

    def get_data(self) -> None:
        temp: json = requests.get(
            f'{SERVER_ADDRESS}/hospitacje/{self.user_id}?user_id={self.user_id}'
        )
        if (temp.status_code == 200):
            self.hospitations = temp.json()

    def insert_into_list(self) -> None:
        quantity_of_hospitations: int = len(self.hospitations)

        for i in range(quantity_of_hospitations):
            self.hospitations_list.insert(
                parent='',
                index=i,
                iid=str(i),
                values=(self.hospitations[i]['id'],
                        self.hospitations[i]['date'],
                        self.hospitations[i]['nr_kursu'] + ' ' +
                        self.hospitations[i]['nazwa_kursu'],
                        self.hospitations[i]['hospitowany_imie'] + ' ' +
                        self.hospitations[i]['hospitowany_nazwisko']))

    def open_protocol(self, container) -> None:
        try:
            temp: Optional[Any] = self.hospitations_list.item(
                self.hospitations_list.focus())
            protocol_id: int = int(temp['values'][0])
            protocol_frame: HospitationPresentFrame = HospitationPresentFrame(
                container, protocol_id)
            replace_frame(protocol_frame, container)

        except Exception as e:
            messagebox.showinfo('Error', 'Musisz najpierw wybrać opcje')


class HospitationPresentFrame(ttk.Frame):
    base_info: dict[str, Any] = {}

    def __init__(self, container, id: int) -> None:
        super().__init__(container)
        self.id: int = id
        res: bool = self.get_data()
        self.frame_top: ttk.Frame = ttk.Frame(self, height=100)
        self.frame_top.pack(fill='x', side=tk.TOP)
        self.logout_button: tk.Button = tk.Button(
            self.frame_top,
            text='Wyloguj',
            bg='red',
            command=lambda: replace_frame(LoginFrame(container), container))
        self.logout_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.back_button: tk.Button = tk.Button(
            self.frame_top,
            text='Powrót',
            bg='blue',
            command=lambda: replace_frame(
                TimetableOfHospitationsFrame(container), container))
        self.back_button.pack(side=tk.LEFT, padx=1, pady=10)

        self.frame_main: ttk.Frame = ttk.Frame(self)
        self.frame_main.pack(fill=tk.BOTH, expand=1)

        self.canvas: tk.Canvas = tk.Canvas(self.frame_main)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.sb: ttk.Scrollbar = ttk.Scrollbar(self.frame_main,
                                               orient=tk.VERTICAL,
                                               command=self.canvas.yview)
        self.sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.sb.set)

        self.canvas.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.
                                                           canvas.bbox("all")))

        self.frame_protocol: ttk.Frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0),
                                  window=self.frame_protocol,
                                  anchor='n')

        if res:
            self.layout_info()

    def layout_info(self) -> None:
        self.frame_base_info: ttk.Frame = ttk.Frame(self.frame_protocol)
        tk.Label(self.frame_base_info,
                 text="Informacje wstępne",
                 font=('Arial', 20, 'underline')).grid(row=0,
                                                       column=0,
                                                       padx=100,
                                                       pady=20,
                                                       sticky='w')

        tk.Label(self.frame_base_info, text="Nazwa kursu:",
                 font=('Arial', 16)).grid(row=1,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['nazwa_kursu'],
                 font=('Arial', 16)).grid(row=1,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info, text="Kod kursu:",
                 font=('Arial', 16)).grid(row=2,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['nr_kursu'],
                 font=('Arial', 16)).grid(row=2,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info,
                 text="Prowadzący kurs:",
                 font=('Arial', 16)).grid(row=3,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['hospitowany_imie'] + ' ' +
                 self.base_info['hospitowany_nazwisko'],
                 font=('Arial', 16)).grid(row=3,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info,
                 text="Forma dydaktyczna:",
                 font=('Arial', 16)).grid(row=4,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['forma_dydaktyczna'],
                 font=('Arial', 16)).grid(row=4,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info,
                 text="Stopień i forma studiów:",
                 font=('Arial', 16)).grid(row=5,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['stopien_i_froma_studiow'],
                 font=('Arial', 16)).grid(row=5,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info,
                 text="Jednostka organizacyjna:",
                 font=('Arial', 16)).grid(row=6,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['jednostka_organizacyjna'],
                 font=('Arial', 16)).grid(row=6,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info,
                 text="Miejsce i termin:",
                 font=('Arial', 16)).grid(row=7,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['miejsce'] + ' ' +
                 self.base_info['termin'],
                 font=('Arial', 16)).grid(row=7,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info,
                 text="Data hospitacji:",
                 font=('Arial', 16)).grid(row=8,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['date'],
                 font=('Arial', 16)).grid(row=8,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        tk.Label(self.frame_base_info,
                 text="Liczba uczestników:",
                 font=('Arial', 16)).grid(row=8,
                                          column=0,
                                          padx=100,
                                          pady=10,
                                          sticky='w')
        tk.Label(self.frame_base_info,
                 text=self.base_info['liczba_uczestnikow'],
                 font=('Arial', 16)).grid(row=8,
                                          column=1,
                                          padx=100,
                                          pady=10,
                                          sticky='e')

        self.frame_base_info.pack(fill=tk.X)

    def get_data(self) -> bool:
        base_info_response = requests.get(
            f'{SERVER_ADDRESS}/hospitacja/detal/{self.id}')
        if (base_info_response.status_code == 200):
            self.base_info = base_info_response.json()
            return True

        elif (base_info_response.status_code == 404):
            messagebox.showinfo('Error 404',
                                'Nie znaleziono szczegółów protokołu')

        else:
            messagebox.showinfo('Error 500',
                                'Serwer nie może przetworzyć zapytania')

        return False
