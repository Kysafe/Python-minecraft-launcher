import os
import requests

def get_local_version(minecraft_directory):
    """Pobierz lokalną wersję z pliku update.txt w folderze gry."""
    local_version_path = os.path.join(minecraft_directory, "update.txt")
    try:
        with open(local_version_path, 'r') as file:
            local_version = file.read().strip()
            return local_version
    except Exception as e:
        print(f"Błąd podczas odczytu lokalnej wersji: {e}")
        return None

def get_remote_version():
    """Pobierz wersję z pliku update.txt na serwerze."""
    remote_url = "http://example.com/minecraft/update.txt"  # Zmień ten link na rzeczywisty adres serwera
    print(f"Requesting remote URL: {remote_url}")  
    try:
        response = requests.get(remote_url)
        if response.status_code == 200:
            remote_version = response.text.strip()
            return remote_version
        else:
            print(f"Błąd podczas pobierania zdalnej wersji: {response.status_code}")
            if response.status_code == 404:
                print("404 Not Found: Sprawdź, czy plik istnieje pod podanym adresem.")
            return None
    except Exception as e:
        print(f"Błąd podczas połączenia z serwerem: {e}")
        return None

def check_for_updates(minecraft_directory):
    """Sprawdź, czy jest dostępna nowa wersja modpacka."""
    local_version = get_local_version(minecraft_directory)
    remote_version = get_remote_version()

    if local_version is None or remote_version is None:
        print("Nie można sprawdzić aktualizacji.")
        return False

    print(f"Lokalna wersja: {local_version}, Zdalna wersja: {remote_version}")

    if local_version < remote_version:
        print("Dostępna jest nowa wersja modpacka!")
        return True
    else:
        print("Modpack jest aktualny.")
        return False

def download_modpack(minecraft_directory):
    """Pobierz nową wersję modpacka."""
    modpack_url = "http://example.com/minecraft/modpack.zip"  # Zmień ten link na rzeczywisty adres serwera
    destination_path = os.path.join(minecraft_directory, "modpack.zip")

    try:
        response = requests.get(modpack_url)
        if response.status_code == 200:
            with open(destination_path, 'wb') as f:
                f.write(response.content)
            print("Modpack został pobrany.")
            return True
        else:
            print(f"Błąd podczas pobierania modpacka: {response.status_code}")
            return False
    except Exception as e:
        print(f"Błąd podczas pobierania modpacka: {e}")
        return False

def update_modpack(minecraft_directory):
    """Aktualizuj modpack, jeśli dostępna jest nowa wersja."""
    if check_for_updates(minecraft_directory):
        if download_modpack(minecraft_directory):  
            print("Modpack zaktualizowany pomyślnie.")
            return True
    return False
