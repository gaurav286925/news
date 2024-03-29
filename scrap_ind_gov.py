import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from contextlib import closing

def scrap_page(url):
	print("Scrapping ",url)
	options = Options()
	options.add_argument("--headless")
	url_list=[]
	with closing(Firefox(firefox_options=options)) as driver:
		driver.get(url)
		WebDriverWait(driver, timeout=10).until(
								lambda x: x.find_elements_by_tag_name('div'))
		pages_remaining = True
		while pages_remaining:
			page_source = driver.page_source
			soup = BeautifulSoup(page_source,'html.parser')
			links = soup.findAll("a")
			for link in links:
				try:
					if link['title'].startswith("http"):
						print(link['title'].split(' -')[0])
						url_list.append(link['title'].split(' -')[0])
				except:
					pass
			try:
				next_link = driver.find_element_by_xpath(
								"//div[@class='pagination']//a[@title='Next']")
				next_link.click()
				time.sleep(3)
			except NoSuchElementException:
				pages_remaining=False
	return url_list

def create_url_list():
	print("Creating Url List ...")
	#UNION, LEGISLATION AND JUDICIARY (excluding ministries from UNION)
	urls=[
		'http://goidirectory.nic.in/union_apex.php',\
		'http://goidirectory.nic.in/union_organisation.php?ct=E013',\
		'http://goidirectory.nic.in/union_organisation.php?ct=E007',\
		'http://goidirectory.nic.in/independent_departments.php?ct=54',\
		'http://goidirectory.nic.in/independent_departments.php?ct=55',\
		'http://goidirectory.nic.in/union_organisation.php?ct=E009',\
		'http://goidirectory.nic.in/legislature_subcategory.php?ct=L001',\
		'http://goidirectory.nic.in/legislature_subcategory.php?ct=L004',\
		'http://goidirectory.nic.in/judiciary_subcategory.php?ct=J001',\
		'http://goidirectory.nic.in/judiciary_subcategory.php?ct=J002',\
		'http://goidirectory.nic.in/judiciary_subcategory.php?ct=J003',\
		'http://goidirectory.nic.in/judiciary_subcategory.php?ct=J011',\
	]
	#STATE
	state_codes = ['AN','AP','AR','AS','BR','CH','CG','DN','DD','DL','GA',\
		'GJ','HR','HP','JK','JH','KA','KL','LD','MP','MN','MH','ML','MZ',\
		'NL','OR','PY','PB','RJ','SK','TN','TG','TR','UK','UP','WB']
	categories = [
		'http://goidirectory.nic.in/state_category.php?ou=####&ct=E001',\
		'http://goidirectory.nic.in/state_depts.php?ou=####&ct=E003',\
		'http://goidirectory.nic.in/state_orgn_categories.php?ou=####&ct=E005',\
		'http://goidirectory.nic.in/state_orgn_categories.php?ou=####&ct=E011',\
		'http://goidirectory.nic.in/state_districts.php?ou=####&ct=E042',\
		'http://goidirectory.nic.in/state_orgn_categories.php?ou=####&ct=E051',\
		'http://goidirectory.nic.in/state_orgn_categories.php?ou=####&ct=E063',\
	]
	for state_code in state_codes:
		for category in categories:
			urls.append( c.split("####")[0] + state_code + \
							category.split("####")[-1])

	#MINISTRY part in the UNION
	ministry_num=range(52)+[723,56,1147,248,4331]
	ministry_group=[1,2,3,7,17,21]
	for i in ministry_num:
		for j in ministry_group:
			urls.append(
				'http://goidirectory.nic.in/ministries_categories.php?ct='+\
				str(i)+'#group'+str(j))
	print("Created mailing List.")
	return urls

def main():
	print("Starting main...")
	urls=create_url_list()
	url_working=set()
	for url in urls:
		try:
			temp_urls=scrap_page(url)
			for temp_url in temp_urls:
				url_working.add(temp_url)
		except:
			pass
	url_working=list(url_working)
	url_working.sort()
	filename="tempIND.txt"
	print("Writing urls to",filename)
	f=open(filename,"a+")
	for url in url_working:
		f.write(url+'\n')
	f.close()
	print("Finish.")

if __name__=="__main__":
	main()
