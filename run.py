from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Initialize driver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--headless')
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

DELAY = 11
shouldWait = False
isRecaptcha = False

def save_to_file(link):
    with open("failed.txt", "a") as f:
        f.write(f"{link}\n")
        
def isReCAPTCHAenabled(driver):
    recaptcha = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".g-recaptcha")))
    if (recaptcha):        
        get_url = driver.current_url
        print('Using reCAPTCHA ' + get_url)
        save_to_file(get_url)        
        return True
    return False


print('WELCOME TO SHONNY DEEP!')
print('Reading links...')
awesome_links = open('./links.txt', 'r')
links = awesome_links.readlines()

for link in links:
    to_download = []
    #navigate to the url
    driver.get(link)    
    anchors = driver.find_elements(By.TAG_NAME, 'a')
    for anchor in anchors:
        a = anchor.get_attribute('title')        
        ## Getting download links
        if (a == 'Enlaces'):
            to_download.append(anchor.get_attribute('href'))
            
                
            
    if(len(to_download) == 0):
        # Trying the ones that are inside a paragraph
        print('Second way...')
        anchors = driver.find_elements(By.CSS_SELECTOR, 'p.info > a')
        for anchor in anchors:
            a = anchor.get_attribute('href')            
            to_download.append(a)
        
        if(len(to_download) == 0):
            print('Failed:' + link)
            continue        
    
        for td in to_download:
            print('Going to Ad site')
            driver.get(td)
            try:
                ad_site = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'vell')))
                if (ad_site):
                    ad_site.click()
                    if (isReCAPTCHAenabled(driver)):
                        continue
            except:
                for td in to_download:                    
                    driver.get(td)
                    # We will wait for the "Click aquí" button
                    try:        
                        ad_site = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'button')))
                        # Once we have the presence of the button in the DOM, let's execute the noobBypass function in the Chrome console
                        if (ad_site):
                            print('Noob bypassing...')
                            driver.execute_script("noobBypass();")            
                            if (isReCAPTCHAenabled(driver)):
                                continue
                            
                            #Let's wait a couple of seconds
                            button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab1"]/form/input[5]')))
                            print('Adding links to JDownloader...')
                            button.click()
                    except TimeoutException:
                        print('Failed Bypassing: '+ td)
                        continue
                    except NoSuchElementException:
                        print('Failed Bypassing: '+ td)
                        continue

#Closing chromedriver
driver.quit()