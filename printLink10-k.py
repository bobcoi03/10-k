# prints out link of latest 10-k file

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import sys
import re
import time
import clipboard

PATH = 'C:\Program Files (x86)\chromedriver.exe'
tickerSymbol = str(sys.argv[1:])
fileType = '10-k'
#runs without opening browser
#options = Options()
#options.add_argument('--headless')

# loads website & chrome
driver = webdriver.Chrome(PATH)
driver.get("https://www.sec.gov/edgar/searchedgar/companysearch.html")

# find searchbar and types in Company name and enter
search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'company')))
search.send_keys(str(tickerSymbol))
time.sleep(3)
search.send_keys(Keys.RETURN)
# find filing type and search
time.sleep(5)
try:
	filingtype = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'type')))
except:
	driver.quit()
filingtype.send_keys(str(fileType))
filingtype.send_keys(Keys.RETURN)

# clicks first file documents page
time.sleep(5)
try:
	# clicks first documents button
	documentsPage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'documentsbutton'))).send_keys(Keys.RETURN)
except:
	driver.quit()
time.sleep(15)

date = driver.find_element_by_xpath("(//div[@class='info'])[position()=4]").text
date = date.split('-')

dateString = date[0] + date[1] + date[2]
print(str(dateString))

time.sleep(10)
link = driver.find_element_by_partial_link_text(dateString)
htmlHref = str(link.get_attribute('outerHTML'))

# gets html element
print("HTML ELEMENT: " + htmlHref)

link_report = re.findall('".+?"', htmlHref)

print("10-K LINK-URL: " + str(link_report[0].strip('"')))

url = link_report[0]
clipboard.copy("sec.gov/" + url.strip('"'))
urlpaste = clipboard.paste()

time.sleep(100)
driver.quit()