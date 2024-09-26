import os
import tkinter as tk
import webbrowser
from tkinter import messagebox
from database import authenticate_user
from minecraft import (
    download_and_install_minecraft,
    download_and_install_modpack,
    launch_minecraft_with_fabric,
)
from updater import update_modpack, get_remote_version, get_local_version

LOGIN_DIR = "C:\\Games\\KAN"  # proszę uzupełnić ścieżkę do katalogu, w którym będą zapisywane pliki z loginem
LOGIN_FILE = os.path.join(LOGIN_DIR, "login.txt")  
RAM_FILE = os.path.join(LOGIN_DIR, "ram.txt")  

def save_login(username):
    """Zapisuje login do pliku."""
    with open(LOGIN_FILE, 'w') as file:
        file.write(username)

def load_login():
    """Ładuje zapisany login z pliku, jeśli istnieje."""
    if os.path.exists(LOGIN_FILE):
        with open(LOGIN_FILE, 'r') as file:
            return file.read().strip()
    return ""

def save_ram(ram_value):
    """Zapisuje wybraną ilość RAM do pliku."""
    with open(RAM_FILE, 'w') as file:
        file.write(str(ram_value))

def load_ram():
    """Ładuje zapisaną ilość RAM z pliku, jeśli istnieje."""
    if os.path.exists(RAM_FILE):
        with open(RAM_FILE, 'r') as file:
            return int(file.read().strip())
    return 6  # domyślna ilość RAM, jeśli brak pliku

def get_version_from_file(filepath="C:\\Games\\KAN\\.minecraft\\update.txt"):
    """Pobiera wersję gry z pliku, jeśli istnieje."""
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Plik {filepath} nie istnieje.")  # proszę uzupełnić ścieżkę do pliku z wersją

        with open(filepath, 'r') as file:
            version = file.read().strip()
            if not version:
                raise ValueError(f"Plik {filepath} jest pusty.")
            return version
    except FileNotFoundError as fnf_error:
        print(f"Błąd: {fnf_error}")  
        return "Gra niezainstalowana"
    except ValueError as ve:
        print(f"Błąd: {ve}")  
        return "Brak wersji (plik pusty)"
    except Exception as e:
        print(f"Inny błąd: {e}")  
        return f"Błąd: {e}"

def create_gui():
    root = tk.Tk()
    root.title("Sigma launcher Pro")
    root.iconbitmap("app_icon.ico")  # proszę uzupełnić ścieżkę do pliku z ikoną

    version = get_version_from_file()

    version_label = tk.Label(root, text=f"Wersja: {version}", fg="green", font=("Helvetica", 16))
    version_label.pack(pady=10)  

    console_frame = tk.Frame(root)
    console_frame.pack(pady=10)

    console_text = tk.Text(console_frame, height=10, width=50, state=tk.DISABLED)
    console_text.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(console_frame, command=console_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    console_text.config(yscrollcommand=scrollbar.set)

    def log_to_console(message):
        """Dodaje wiadomość do konsoli w GUI."""
        console_text.config(state=tk.NORMAL)  
        console_text.insert(tk.END, message + '\n')  
        console_text.config(state=tk.DISABLED)  
        console_text.see(tk.END)  

    def login_and_launch():
        """Logowanie i uruchamianie Minecrafta."""
        username = username_entry.get()
        password = password_entry.get()
        if authenticate_user(username, password):  # funkcja autoryzacji użytkownika
            save_login(username)  
            selected_ram = ram_var.get()
            if selected_ram:
                ram_value = f"{selected_ram}G"
                log_to_console(f"Uruchamianie Minecrafta z {ram_value} RAM...")
                save_ram(selected_ram)  
                launch_minecraft_with_fabric(ram_value, "C:\\Games\\KAN\\.minecraft", username, log_to_console)  # proszę uzupełnić ścieżkę do katalogu Minecrafta
            else:
                messagebox.showerror("Błąd", "Proszę wybrać ilość RAM przed uruchomieniem Minecrafta.")
        else:
            messagebox.showerror("Błąd", "Błędna nazwa użytkownika lub hasło.")

    def check_and_update_modpack():
        """Sprawdza i aktualizuje modpack."""
        minecraft_directory = "C:\\Games\\KAN\\.minecraft"  # proszę uzupełnić ścieżkę do katalogu Minecrafta
        log_to_console("Sprawdzanie aktualizacji modpacka...")
        if update_modpack(minecraft_directory):
            messagebox.showinfo("Aktualizacja", "Modpack został zaktualizowany!")
            auto_check_updates()  
        else:
            messagebox.showinfo("Aktualizacja", "Brak dostępnych aktualizacji lub wystąpił błąd.")

    ram_label = tk.Label(root, text="WYBIERZ ILOŚĆ RAM:")
    ram_label.pack(pady=10)  

    warning_label = tk.Label(root, text="")
    warning_label.pack(pady=5)  

    ram_var = tk.IntVar(value=load_ram())  

    ram_slider = tk.Scale(
        root,
        variable=ram_var,
        from_=3,       
        to=12,         
        orient=tk.HORIZONTAL,  
        resolution=1,  
        length=300,    
    )
    ram_slider.pack(pady=10)

    def update_warning(val):
        """Wyświetla ostrzeżenie dla wartości RAM powyżej 10."""
        if val > 10:
            warning_label.config(text="(OSTROŻNIE)", fg="red")
        else:
            warning_label.config(text="")

    ram_var.trace("w", lambda *args: update_warning(ram_var.get()))

    tk.Label(root, text="Wprowadź nazwę użytkownika:").pack(pady=10)
    username_entry = tk.Entry(root)
    username_entry.pack()

    saved_login = load_login()
    if saved_login:
        username_entry.insert(0, saved_login)  

    tk.Label(root, text="Wprowadź hasło:").pack(pady=10)
    password_entry = tk.Entry(root, show='*')
    password_entry.pack()

    launch_button = tk.Button(root, text="Zaloguj i uruchom Minecrafta", command=login_and_launch)
    launch_button.pack(pady=20)

    def on_enter(event):
        """Obsługuje logowanie po wciśnięciu Enter."""
        login_and_launch()

    password_entry.bind("<Return>", on_enter)
    username_entry.bind("<Return>", on_enter)

    def auto_check_updates():
        """Automatycznie sprawdza dostępność Minecrafta i modpacka."""
        update_file_path = "C:\\Games\\KAN\\.minecraft\\update.txt"  # proszę uzupełnić ścieżkę do pliku z aktualizacją
        if os.path.exists(update_file_path):
            install_minecraft_button.pack_forget()
            install_modpack_button.pack_forget()
            check_server_version()  
        else:
            log_to_console("Pobierz Minecraft i Modpack.")
            install_minecraft_button.pack(pady=10)
            install_modpack_button.pack(pady=10)

    def check_server_version():
        """Sprawdza wersję zainstalowaną na serwerze i lokalnie."""
        installed_version = get_local_version("C:\\Games\\KAN\\.minecraft")  # proszę uzupełnić ścieżkę do katalogu Minecrafta
        server_version = get_remote_version()  # funkcja pobierająca zdalną wersję

        if server_version is not None and installed_version is not None and server_version > installed_version:
            log_to_console(f"Dostępna nowa wersja: {server_version} (zainstalowana: {installed_version})")
            update_modpack_button.pack(pady=10)  
        else:
            log_to_console("Modpack jest aktualny.")

    install_minecraft_button = tk.Button(root, text="Zainstaluj Minecrafta", command=lambda: download_and_install_minecraft(log_to_console))

    install_modpack_button = tk.Button(root, text="Pobierz i zainstaluj modpack", command=lambda: download_and_install_modpack(log_to_console))

    update_modpack_button = tk.Button(root, text="Sprawdź i zaktualizuj modpack", command=check_and_update_modpack)
    update_modpack_button.pack_forget()  

    auto_check_updates()

    copyright_label = tk.Label(root, text="Copyright © Kysafe | Zarejestruj się!", fg="blue", cursor="hand2")
    copyright_label.pack(pady=10)

    def open_link(event):
        """Otwiera link do rejestracji w przeglądarce."""
        webbrowser.open("http://uzupelnij/register.php")  # proszę uzupełnić adres URL do strony rejestracji

    copyright_label.bind("<Button-1>", open_link)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
