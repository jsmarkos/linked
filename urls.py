from selenium import webdriver
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
import time

query_keyword = "geomatic"
query_keyword_Education='"yıldız teknik üniversitesi"'
no_of_pages = 2
username = ""
password = ""

driver_path='/home/markos/İndirilenler/geckodriver-v0.28.0-linux64/geckodriver'
driver=webdriver.Firefox(executable_path=driver_path)
driver.get('https://www.linkedin.com/')

email_box = driver.find_element_by_id('session_key')
email_box.send_keys('e.birinnci@gmail.com')
pass_box = driver.find_element_by_id('session_password')
pass_box.send_keys('')
submit_button = driver.find_element_by_class_name('sign-in-form__submit-button')
submit_button.click()

time.sleep(1)

urls = []
for i in tqdm(range(no_of_pages)):
	try:
		driver.get(
			'https://www.linkedin.com/search/results/people/?'+
			'origin=FACETED_SEARCH&page=' + str(i) +
            '&schoolFreetext=' + query_keyword_Education+
			'&title=' + query_keyword
       
		)
		soup = BeautifulSoup(driver.page_source, "lxml")
		soup = soup.find_all(class_="app-aware-link ember-view")
		for s in soup:
            
            #url = 'https://www.linkedin.com' + s['href']
			url = s['href']
			urls.append(url)
		print(i)
	except KeyboardInterrupt:
		break

urls = list(set(urls))

with open("Url_linked.txt", "w") as f:
	for url in urls:
		f.write(url + "\n")
