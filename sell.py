from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Konfigurasi opsi untuk menjaga browser tetap terbuka
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Inisialisasi WebDriver dengan opsi
driver = webdriver.Chrome(options=chrome_options)

# Akses halaman yang diinginkan
driver.get('https://www.tokopedia.com')
