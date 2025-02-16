import requests
from bs4 import BeautifulSoup
import re
import os

# Saytın URL-i
url = 'https://yoda.az/'

# Çıxış qovluğu
output_folder = 'm3u8_links'
os.makedirs(output_folder, exist_ok=True)  # Qovluq yaradılır (əgər yoxdursa)

# Saytın məzmununu əldə et
try:
    response = requests.get(url)
    response.raise_for_status()  # HTTP xətası yoxlanılır
except requests.exceptions.RequestException as e:
    print(f"Sayta giriş zamanı xəta baş verdi: {e}")
    exit(1)

soup = BeautifulSoup(response.text, 'html.parser')

# Axtarılacaq m3u8 linki
target_link = 'https://str.yodacdn.net/aztv/index.m3u8'

# Bütün linkləri yoxla
found_links = []
for tag in soup.find_all('a', href=True):
    href = tag['href']
    if target_link in href:
        found_links.append(href)

# Əgər link tapılıbsa, fayla yaz
if found_links:
    output_file = os.path.join(output_folder, 'found_m3u8_links.txt')
    try:
        with open(output_file, 'w') as f:
            for link in found_links:
                f.write(link + '\n')
        print(f"Link tapıldı və {output_file} faylına yazıldı.")
    except IOError as e:
        print(f"Fayla yazmaq zamanı xəta baş verdi: {e}")
else:
    print("Heç bir m3u8 linki tapılmadı.")
