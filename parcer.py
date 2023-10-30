import os
import requests
import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import filedialog
import pyperclip

# Путь к папке по умолчанию (media в каталоге приложения)
default_media_folder = os.path.join(os.getcwd(), 'media')

# Переменные для счетчика
total_downloaded = 0
total_failed = 0

# Функция для скачивания медиа-файлов
def download_media(url, folder_path):
    global total_downloaded, total_failed

    try:
        response = requests.get(url)
        if response.status_code == 200:
            content_type = response.headers.get('content-type')
            if 'image' in content_type:
                file_extension = 'jpg'
            elif 'video' in content_type:
                file_extension = 'mp4'
            elif 'audio' in content_type:
                file_extension = 'mp3'
            else:
                return

            file_name = os.path.join(folder_path, f'{os.path.basename(url)}.{file_extension}')
            with open(file_name, 'wb') as file:
                file.write(response.content)

            total_downloaded += 1
        else:
            total_failed += 1
    except Exception as e:
        print(f"Ошибка при скачивании: {e}")
        total_failed += 1

    update_counter_label()

# Функция для обновления текста счетчика
def update_counter_label():
    counter_label.config(text=f"Скачано: {total_downloaded} Не удалось: {total_failed}")

# Функция для обработки URL и скачивания медиа-файлов
def process_url():
    global total_downloaded, total_failed
    total_downloaded = 0
    total_failed = 0

    url = url_entry.get()
    media_folder = media_folder_entry.get()

    if not media_folder:
        media_folder = default_media_folder

    if not os.path.exists(media_folder):
        os.makedirs(media_folder)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            media_elements = soup.find_all(['img', 'video', 'audio'])

            for element in media_elements:
                if 'src' in element.attrs:
                    media_url = element['src']
                    download_media(media_url, media_folder)

            result_label.config(text="Файлы успешно скачаны")
        else:
            result_label.config(text="Ошибка при обработке URL")
    except Exception as e:
        result_label.config(text=f"Ошибка при обработке URL: {e}")

# Функция для вставки URL из буфера обмена
def paste_url():
    clipboard_contents = pyperclip.paste()
    url_entry.delete(0, 'end')
    url_entry.insert(0, clipboard_contents)

# Функция для выбора другой папки для скачивания
def select_download_folder():
    folder_path = filedialog.askdirectory()
    media_folder_entry.delete(0, 'end')
    media_folder_entry.insert(0, folder_path)

# Создание горячей клавиши для вставки URL (не нужна, используется pyperclip)

# Создание графического интерфейса
app = tk.Tk()
app.title("Web Media Downloader")

url_label = tk.Label(app, text="URL веб-сайта:")
url_label.pack()

url_entry = tk.Entry(app)
url_entry.pack()

media_folder_label = tk.Label(app, text="Папка для медиа-файлов (media в каталоге приложения по умолчанию):")
media_folder_label.pack()

media_folder_entry = tk.Entry(app)
media_folder_entry.insert(0, default_media_folder)
media_folder_entry.pack()

select_folder_button = tk.Button(app, text="Выбрать папку", command=select_download_folder)
select_folder_button.pack()

download_button = tk.Button(app, text="Скачать медиа", command=process_url)
download_button.pack()

counter_label = tk.Label(app, text="Скачано: 0 Не удалось: 0")
counter_label.pack()

result_label = tk.Label(app, text="")
result_label.pack()

app.mainloop()
