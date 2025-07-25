import random
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from PIL import Image
from io import BytesIO

# Install required packages
!pip install selenium pillow
!apt-get update
!apt install -y chromium-chromedriver

# ========== KONFIGURASI ==========
TARGET_URLS = [
    'https://www.profitableratecpm.com/yp5s785fv9?key=23fcee97edae2ea57212c118f18420bd',
    'https://www.profitableratecpm.com/w4n4gkie?key=cece3ce2daf51b4d6e580cfc73d9600e',
    'https://www.profitableratecpm.com/ua1y3ps2i?key=1e4201d6eccd48757ac0a4089150be90'
]

PROXY = "localhost:3128"
DELAY_AFTER_LOAD = 8  # Delay setelah buka URL
DELAY_AFTER_CLICK = 2  # Delay setelah klik

# ========== SISTEM IDENTITAS ==========
class IdentityManager:
    def __init__(self):
        self.devices = [
            # Mobile devices
            {'name': 'Samsung S22', 'ua': 'Mozilla/5.0 (Linux; Android 12; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.61 Mobile Safari/537.36', 'res': (360, 800), 'type': 'mobile'},
            {'name': 'iPhone 13', 'ua': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1', 'res': (390, 844), 'type': 'mobile'},
            
            # Desktop devices
            {'name': 'Win10 Chrome', 'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36', 'res': (1920, 1080), 'type': 'desktop'},
            {'name': 'MacOS Safari', 'ua': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15', 'res': (2560, 1600), 'type': 'desktop'}
        ]
    
    def get_random_identity(self):
        """Mengembalikan identitas acak"""
        device = random.choice(self.devices)
        return {
            'name': device['name'],
            'user_agent': device['ua'],
            'resolution': device['res'],
            'type': device['type'],
            'timezone': 'Asia/Jakarta',
            'language': 'en-US'
        }

# ========== UTILITAS ==========
def create_screenshot_dir():
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')

def take_screenshot(driver, request_num, url_index, prefix=''):
    screenshot = driver.get_screenshot_as_png()
    image = Image.open(BytesIO(screenshot))
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"screenshots/req_{request_num}_url{url_index+1}_{prefix}{timestamp}.png"
    image.save(filename)
    return filename

def setup_driver(identity):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f'--proxy-server={PROXY}')
    chrome_options.add_argument(f'user-agent={identity["user_agent"]}')
    chrome_options.add_argument(f'--window-size={identity["resolution"][0]},{identity["resolution"][1]}')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    return webdriver.Chrome(options=chrome_options)

def perform_single_click(driver):
    """Melakukan satu kali percobaan klik saja"""
    try:
        # Coba cari elemen yang bisa diklik
        clickable_elements = driver.find_elements(By.CSS_SELECTOR, "a, button, input[type='submit'], [onclick]")
        
        if clickable_elements:
            element = random.choice(clickable_elements)
            ActionChains(driver).move_to_element(element).click().perform()
            print(f"🖱️ Klik pada: {element.tag_name}")
            return True
        
        # Jika tidak ada elemen, klik posisi acak
        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        x = random.randint(0, width - 50)
        y = random.randint(0, height - 50)
        
        ActionChains(driver).move_by_offset(x, y).click().perform()
        print(f"🖱️ Klik posisi acak ({x}, {y})")
        return True
        
    except Exception:
        print("🖱️ Tidak berhasil klik (dilewati saja)")
        return False

# ========== PROGRAM UTAMA ==========
def main():
    create_screenshot_dir()
    identity_manager = IdentityManager()
    
    print("\n" + "="*50)
    print("🌐 PROGRAM AKSES URL DENGAN SATU KLIK")
    print("="*50)
    print(f"🔌 Proxy: {PROXY}")
    print(f"⏳ Delay load: {DELAY_AFTER_LOAD}s | Delay klik: {DELAY_AFTER_CLICK}s")
    
    request_count = 0
    url_index = 0
    
    try:
        while True:
            request_count += 1
            driver = None
            
            try:
                identity = identity_manager.get_random_identity()
                print(f"\n🔄 REQUEST #{request_count}")
                print(f"📱 {identity['name']} ({identity['type']})")
                print(f"🌐 URL {url_index+1}: {TARGET_URLS[url_index][:50]}...")
                
                driver = setup_driver(identity)
                driver.get(TARGET_URLS[url_index])
                
                # Screenshot setelah load
                take_screenshot(driver, request_count, url_index, 'loaded_')
                
                # Delay 8 detik
                print(f"⏳ Menunggu {DELAY_AFTER_LOAD} detik...")
                time.sleep(DELAY_AFTER_LOAD)
                
                # Lakukan satu kali klik saja
                print("🖱️ Mencoba klik satu kali...")
                perform_single_click(driver)
                
                # Screenshot setelah klik
                take_screenshot(driver, request_count, url_index, 'clicked_')
                
                # Delay 2 detik
                print(f"⏳ Menunggu {DELAY_AFTER_CLICK} detik...")
                time.sleep(DELAY_AFTER_CLICK)
                
                # Pindah ke URL berikutnya
                url_index = (url_index + 1) % len(TARGET_URLS)
                driver.quit()
                
            except WebDriverException as e:
                print(f"\n⚠️ Error: {str(e)[:200]}")
                if driver: driver.quit()
                print(f"⏳ Menunggu {DELAY_AFTER_LOAD} detik...")
                time.sleep(DELAY_AFTER_LOAD)
                
    except KeyboardInterrupt:
        print("\n🛑 Program dihentikan")
        
        import zipfile
        with zipfile.ZipFile('screenshots_report.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk('screenshots'):
                for file in files:
                    zipf.write(os.path.join(root, file))
        
        print("\n📦 Screenshot disimpan di screenshots_report.zip")
        print(f"🔢 Total requests: {request_count}")

if __name__ == "__main__":
    main()
