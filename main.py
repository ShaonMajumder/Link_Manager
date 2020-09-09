from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import random
import configparser
import shaonutil


def loading_data(remove=''):
	with open('data/links.txt', 'r') as file:
	    data = file.read()
	rex = re.compile(r'<link.*?>(.*?)</link>',re.S|re.M)
	match = rex.match(data)
	if match:
	    text = match.groups()[0].strip()

	if remove != '':
		text2 = text.replace(remove+'\n','')
		data = data.replace(text,text2)
		
		links = text2.split('\n')

		
		m = re.compile(r'<done>(.*?)</done>',re.S|re.M).search(data)
		text_done = m.group(1)

		
		
		text_done2 = '\n' + remove  + text_done
		data = data.replace(text_done,text_done2)


		#write data
		with open('data/links.txt', 'w+') as fh:
		    fh.write(data)
	else:
		links = text.split('\n')

	while('' in links): links.remove('')
	if not len(links) > 0: return False
	now_link = random.choice(links)
	return now_link
	
config = shaonutil.file.read_configuration_ini("data/credential.ini")
email = config['FB_CREDENTIAL']['email']
password = config['FB_CREDENTIAL']['password']

driver = webdriver.Chrome('resources/chromedriver.exe')

driver.get("https://www.facebook.com")
driver.find_element_by_id("email").send_keys(email)
driver.find_element_by_id("pass").send_keys(password)
driver.find_element_by_name("login").click()
input("login done ?")

now_link = ''
while True:
	now_link = loading_data(remove = now_link)
	if not now_link: break
	print("Visiting",now_link)
	driver.get(now_link)
	input_ = input("Page done ?")
	if input_ == 'q': break

driver.close()
driver.quit()