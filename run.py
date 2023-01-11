from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Initialize driver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--headless')
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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
            
    if(len(to_download) > 0):
        for td in to_download:
            driver.get(td)
            # We will wait for the "Click aquí" button
            print('Going to Ad site')
            ad_site = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'button')))
            # Once we have the presence of the button in the DOM, let's execute the noobBypass function in the Chrome console
            if (ad_site):
                print('Noob bypassing...')
                driver.execute_script("noobBypass();")            
                #Let's wait a couple of seconds            
                button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab1"]/form/input[5]')))
                print('Adding links to JDownloader...')
                button.click()
            

#Closing chromedriver        
driver.quit()