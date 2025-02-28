import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import pandas as pd

class Scraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(executable_path=r'F:\Kuliah\Magang\codingan jadi1\Hasil fixs\codingan 2 scraping tokopedia\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service, options=options)
    
    def get_data(self):
        # Buka halaman utama Tokopedia
        self.driver.get('https://www.tokopedia.com')
        
        # Tunggu hingga halaman selesai dimuat
        WebDriverWait(self.driver, 20).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        
        # Cari input pencarian dengan beberapa alternatif selector
        selectors = ['input[name="q"]', 'input[type="search"]', 'input[placeholder*="Cari"]']
        search_input = None
        for selector in selectors:
            try:
                search_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if search_input:
                    print(f"Ditemukan input dengan selector: {selector}")
                    break
            except TimeoutException:
                continue
        
        if not search_input:
            print("Elemen input pencarian tidak ditemukan.")
            self.driver.quit()
            return []
        
        # Masukkan keyword pencarian "jadwal sholat"
        search_input.clear()
        search_input.send_keys("mesin antrian")
        search_input.send_keys(Keys.ENTER)
        
        # Tunggu hasil pencarian termuat
        time.sleep(5)
        
        csv_filename = 'data_mesin_antrian.csv'
        header_exists = os.path.exists(csv_filename)
        
        # Loop untuk 10 halaman hasil pencarian
        for page in range(1, 11):
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#zeus-root'))
                )
            except TimeoutException:
                print("Kontainer hasil pencarian tidak ditemukan.")
                break
            
            time.sleep(3)
            
            # Lakukan scroll agar lazy-loaded content termuat
            for i in range(15):
                self.driver.execute_script('window.scrollBy(0,500)')
                time.sleep(1)
            
            # Parsing HTML halaman dengan BeautifulSoup
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Gunakan selector container produk terbaru: 'div.css-5wh65g'
            products = soup.find_all('div', class_='css-5wh65g')
            if not products:
                print(f"Halaman {page}: Produk tidak ditemukan dengan selector 'div.css-5wh65g'.")
            else:
                print(f"Halaman {page}: Ditemukan {len(products)} produk.")
            
            page_data = []
            for item in products:
                # Ambil nama produk
                try:
                    name_elem = item.find('div', class_='_6+OpBPVGAgqnmycna+bWIw==')
                    product_name = name_elem.get_text(strip=True) if name_elem else ''
                except Exception:
                    product_name = ''
                
                # Ambil harga produk
                try:
                    price_elem = item.find('div', class_='XvaCkHiisn2EZFq0THwVug==')
                    price = price_elem.get_text(strip=True) if price_elem else ''
                except Exception:
                    price = ''
                
                # Ambil rating produk dari kelas "Lrp+JcoWPuzTgMQ41Mkg3w=="
                try:
                    sold_elem = item.find('div', class_='Lrp+JcoWPuzTgMQ41Mkg3w==')
                    sold = sold_elem.get_text(strip=True) if sold_elem else ''
                except Exception:
                    sold = ''
                
                # Ambil nama toko dari kelas "bi73OIBbtCeigSPpdXXfdw=="
                try:
                    store_elem = item.find('div', class_='bi73OIBbtCeigSPpdXXfdw==')
                    store_name = store_elem.get_text(strip=True) if store_elem else ''
                except Exception:
                    store_name = ''
                
                # Debug: tampilkan data yang diambil
                print(f"Produk: {product_name} | Harga: {price} | Sold: {sold} | Toko: {store_name}")
                
                page_data.append({
                    'Produk': product_name,
                    'Harga': price,
                    'Sold': sold,
                    'Nama Toko': store_name
                })
            
            # Simpan data halaman ke CSV jika ada data
            if page_data:
                df = pd.DataFrame(page_data)
                df.to_csv(csv_filename, mode='a', header=not header_exists, index=False)
                header_exists = True
                print(f"Data dari halaman {page} disimpan ke {csv_filename}")
            else:
                print(f"Halaman {page}: Tidak ada data yang diambil.")
            
            # Klik tombol "Laman berikutnya" untuk pagination jika ada
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label^="Laman berikutnya"]')
                next_button.click()
            except NoSuchElementException:
                print("Tombol 'Laman berikutnya' tidak ditemukan. Mungkin sudah di halaman terakhir.")
                break
            
            time.sleep(3)
        
        self.driver.quit()
        return []

if __name__ == '__main__':
    scraper = Scraper()
    scraper.get_data()
