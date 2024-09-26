import os
import zipfile
import requests
import subprocess
import uuid
import minecraft_launcher_lib
import threading  

kan_directory = "C:\\Games\\KAN"  
minecraft_directory = os.path.join(kan_directory, ".minecraft")
minecraft_zip_path = os.path.join(minecraft_directory, "minecraft.zip")
modpack_zip_path = os.path.join(minecraft_directory, "modpack.zip")

# Zmień te adresy URL na odpowiednie i bezpieczne.
minecraft_url = "http://example.com/minecraft/minecraft.zip"  
modpack_url = "http://example.com/minecraft/modpack.zip"  
base_url = "http://example.com/minecraft/"  

def download_file(url, download_path, log_callback):
    try:
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        response = requests.get(url, stream=True)  
        response.raise_for_status()  
        with open(download_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):  
                file.write(chunk)
        log_callback(f"Pobranie pliku z {url} zakończone sukcesem.")
        return True
    except requests.HTTPError as http_err:
        log_callback(f"Błąd pobierania pliku: {http_err}")
        return False
    except Exception as e:
        log_callback(f"Błąd podczas pobierania pliku: {e}")
        return False

def install_zip(zip_path, destination_directory, log_callback):
    os.makedirs(destination_directory, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(destination_directory)
        log_callback(f"Plik {zip_path} został rozpakowany do {destination_directory}.")
    except zipfile.BadZipFile:
        log_callback(f"Błąd: Plik zip jest uszkodzony lub niepoprawny: {zip_path}")
    except Exception as e:
        log_callback(f"Błąd podczas rozpakowywania pliku: {e}")

    if os.path.exists(zip_path):
        os.remove(zip_path)

def download_and_install_minecraft(log_callback):
    if download_file(minecraft_url, minecraft_zip_path, log_callback):
        install_zip(minecraft_zip_path, minecraft_directory, log_callback)
        return True
    return False

def download_and_install_modpack(log_callback):
    if download_file(modpack_url, modpack_zip_path, log_callback):
        install_modpack_zip(modpack_zip_path, minecraft_directory, log_callback)
        return True
    return False

def install_modpack_zip(modpack_path, minecraft_directory, log_callback):
    directories_to_create = ["mods", "resourcepacks", "shaderpacks", "datapacks", "config", "data", "moddata"]
    for directory in directories_to_create:
        os.makedirs(os.path.join(minecraft_directory, directory), exist_ok=True)
    try:
        with zipfile.ZipFile(modpack_path, 'r') as zip_ref:
            zip_ref.extractall(minecraft_directory)
        log_callback(f"Modpack z {modpack_path} został zainstalowany.")
    except zipfile.BadZipFile:
        log_callback(f"Błąd: Plik modpacka jest uszkodzony lub niepoprawny: {modpack_path}")
    except Exception as e:
        log_callback(f"Błąd podczas instalacji modpacka: {e}")

    if os.path.exists(modpack_path):
        os.remove(modpack_path)

def launch_minecraft_with_fabric(ram, minecraft_directory, username, log_callback):
    minecraft_version = "1.20.1"
    fabric_loader_version = "fabric-loader-0.16.5-1.20.1"

    version_directory = os.path.join(minecraft_directory, "versions", fabric_loader_version)
    os.makedirs(version_directory, exist_ok=True)

    try:
        minecraft_launcher_lib.fabric.install_fabric(minecraft_version, minecraft_directory)
        log_callback(f"Fabric zainstalowany dla wersji {minecraft_version}.")
    except Exception as e:
        log_callback(f"Błąd podczas instalacji Fabric: {e}")
        return

    offline_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))
    options = {
        "username": username,
        "uuid": offline_uuid,
        "token": "0",
        "jvmArguments": [f"-Xmx{ram}", f"-Xms{ram}", f"-Duser.home={minecraft_directory}"]  
    }

    os.chdir(minecraft_directory)

    try:
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(fabric_loader_version, minecraft_directory, options)

        subprocess.run(minecraft_command)
        log_callback("Minecraft został uruchomiony.")
    except Exception as e:
        log_callback(f"Błąd podczas uruchamiania Minecrafta: {e}")

def start_minecraft_in_thread(ram, minecraft_directory, username, log_callback):
    threading.Thread(target=launch_minecraft_with_fabric, args=(ram, minecraft_directory, username, log_callback)).start()

if __name__ == "__main__":
    ram = "2G"  
    username = "test_user"  

    def sample_log(message):
        print(message)

    if download_and_install_minecraft(sample_log):
        print("Minecraft został pobrany i zainstalowany.")

    if download_and_install_modpack(sample_log):
        print("Modpack został pobrany i zainstalowany.")

    start_minecraft_in_thread(ram, minecraft_directory, username, sample_log)
