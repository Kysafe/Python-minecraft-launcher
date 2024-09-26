import mysql.connector
from passlib.hash import bcrypt  
from tkinter import messagebox

def create_connection():
    """Tworzy połączenie z bazą danych."""
    try:
        connection = mysql.connector.connect(
            host='uzupelnij',  # proszę uzupełnić informacje o hostie
            user='uzupelnij',  # proszę uzupełnić nazwę użytkownika
            password='uzupelnij',  # proszę uzupełnić hasło do bazy danych
            database='uzupelnij'  # proszę uzupełnić nazwę bazy danych
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Błąd przy połączeniu z bazą danych: {err}")
        messagebox.showerror("Błąd", f"Nie udało się połączyć z bazą danych: {err}")
        return None

def authenticate_user(username, password):
    """Autoryzuje użytkownika na podstawie nazwy użytkownika i hasła."""
    connection = create_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            print("Pobierane hasło:", user[2])  
            if bcrypt.verify(password, user[2]):  
                return True
            else:
                print("Hasło nieprawidłowe.")
                return False
        else:
            print("Użytkownik nie znaleziony.")
            return False

    except mysql.connector.Error as err:
        print(f"Błąd w zapytaniu do bazy danych: {err}")
        messagebox.showerror("Błąd", f"Wystąpił błąd w zapytaniu do bazy danych: {err}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
