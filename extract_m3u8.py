import os
import requests
import time
import hashlib
import random
import string

# Qaynaq linkləri
source_urls = [
    "https://raalbatros.serv00.net:443/ctv.php?url=https://tv.canlitv.vip/saban-tv",
    # Buraya digər m3u8 linklərini əlavə edin
]

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Dinamik token və parametrlər yaratmaq üçün funksiya
def generate_dynamic_url(base_url):
    # Token və digər parametrləri yaradırıq
    accesscode = "fbly"  # Sabit qalır
    tkn = ''.join(random.choices(string.ascii_letters + string.digits, k=22))  # 22 simvol uzunluğunda təsadüfi token
    tms = str(int(time.time()))  # Cari Unix zamanı (timestamp)
    hst = "tv.canlitv.vip"  # Host adı
    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))  # Təsadüfi IP ünvanı
    
    # Parametrləri URL-ə əlavə edirik
    dynamic_url = f"{base_url}?accesscode={accesscode}&tkn={tkn}&tms={tms}&hst={hst}&ip={ip}"
    return dynamic_url

# .ts linkini əvəz edən funksiya
def replace_ts_with_m3u8(line, base_url):
    if line.strip().endswith('.ts'):  # Tam URL və ya nisbi yol olan .ts linklərini tapır
        return generate_dynamic_url(base_url)
    return line

# m3u8 faylını çıxar və qovluğa yadda saxla
def extract_m3u8(url, index):
    try:
        # m3u8 faylını yüklə
        response = requests.get(url)
        response.raise_for_status()  # Xəta yoxlanışı
        
        # Fayl adını index ilə fərqləndir
        filename = f"stream_{index}.m3u8"
        file_path = os.path.join(output_folder, filename)
        
        # Faylı oxu və içindəki nisbi linkləri tam URL-yə çevir
        m3u8_content = response.text.splitlines()
        
        # Debug: Qaynaq faylının məzmununu çap et
        print("Qaynaq faylının məzmunu:")
        print(m3u8_content)
        
        # Multi-variant m3u8 faylı üçün əsas strukturu yaradırıq
        modified_content = "#EXTM3U\n#EXT-X-VERSION:3\n"
        
        # İçindəki linkləri işləyib, onların önündəki əlavə edilən hissəni çıxarırıq
        for line in m3u8_content:
            if line.strip() and not line.startswith("#"):  # Tərkibdə "#" olmayan sətirləri seç
                # Linki əvəz etmək üçün funksiya çağırılır
                base_url = "https://cdn900.canlitv.vip/sabantv.m3u8"
                modified_line = replace_ts_with_m3u8(line, base_url)
                modified_content += f"#EXT-X-STREAM-INF:BANDWIDTH=2085600,RESOLUTION=1280x720\n{modified_line}\n"
            else:
                # Əgər sətir meta məlumatdırsa, olduğu kimi saxla
                modified_content += f"{line}\n"
        
        # Faylı qovluğa yaz (üzərinə yaz)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(modified_content)
        print(f"m3u8 faylı uğurla yeniləndi: {file_path}")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skriptin əsas hissəsi
if __name__ == "__main__":
    for index, url in enumerate(source_urls):
        if url:  # Əgər URL boş deyilsə
            extract_m3u8(url, index)
