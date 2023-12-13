import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import csv
import requests
from io import BytesIO
import webbrowser

class CarViewerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Przeglądarka Samochodów")
        self.master.geometry("900x350")

        self.car_data = []
        self.current_index = 0

        self.load_data()
        self.create_widgets()

    def load_data(self):
        with open('dane.csv', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                self.car_data.append({
                    "Nazwa": row[0],
                    "Cena": row[1],
                    "Przebieg": row[2],
                    "Opis": row[3],
                    "Link": row[4],
                    "ObrazLink": row[5]
                })

    def create_widgets(self):
        columns = ("Atrybut", "Wartość")
        self.tree = ttk.Treeview(self.master, columns=columns, show="headings")

        # Ustawienie nagłówków kolumn
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=300 if col in ("Link", "ObrazLink") else 100, anchor=tk.CENTER)

        # Umieszczenie widżetu Treeview
        self.tree.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")  # Add sticky="nsew"

        # Dodawanie danych do Treeview dla pierwszego samochodu
        self.show_car_data()

        prev_button = ttk.Button(self.master, text="Poprzedni", command=self.show_prev_car)
        prev_button.grid(row=1, column=0, pady=10, sticky="w", padx=10)  # Ustawienie sticky="w" i padx=10

        open_link_button = ttk.Button(self.master, text="Otwórz link", command=self.open_link)
        open_link_button.grid(row=1, column=1, pady=10, sticky="nsew")  # Ustawienie sticky="nsew"

        open_link_button = ttk.Button(self.master, text="Pokaż podobne", command=self.wyszukaj_wiecej)
        open_link_button.grid(row=1, column=2, pady=10, sticky="nsew")  # Ustawienie sticky="nsew"

        next_button = ttk.Button(self.master, text="Następny", command=self.show_next_car)
        next_button.grid(row=1, column=3, pady=10, sticky="e", padx=10)  # Ustawienie sticky="e" i padx=10

        # Konfiguracja umożliwiająca rozszerzanie okna
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

    def wyszukaj_wiecej(self):
        current_car = self.car_data[self.current_index]
        search_url = f"https://www.google.com/search?q={current_car['Nazwa']}&tbm=isch"
        webbrowser.open(search_url)

    def show_car_data(self):
        # Czyszczenie istniejących danych w Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Dodawanie danych do Treeview dla aktualnego samochodu
        current_car = self.car_data[self.current_index]
        for key, value in current_car.items():
            self.tree.insert("", tk.END, values=(key, value))

        # Dodawanie obrazu do okna
        img = self.load_image(current_car["ObrazLink"])
        img_label = ttk.Label(self.master, image=img)
        img_label.image = img
        img_label.grid(row=0, column=2, padx=10, pady=10)

    def load_image(self, image_url):
        # Pobieranie obrazu z URL przy użyciu Pillow
        response = requests.get(image_url)
        img_data = Image.open(BytesIO(response.content))
        img_data.thumbnail((320, 240))  # Dostosuj rozmiar obrazu

        # Konwersja obrazu do formatu obsługiwanego przez Tkinter
        tk_img = ImageTk.PhotoImage(img_data)

        return tk_img

    def show_next_car(self):
        # Przejście do następnego samochodu
        self.current_index = (self.current_index + 1) % len(self.car_data)
        self.show_car_data()

    def show_prev_car(self):
        # Przejście do poprzedniego samochodu
        self.current_index = (self.current_index - 1) % len(self.car_data)
        self.show_car_data()

    def open_link(self):
        # Otwieranie linku w przeglądarce
        current_car = self.car_data[self.current_index]
        webbrowser.open(current_car["Link"])

