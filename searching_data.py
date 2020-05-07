from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
import requests 
from bs4 import BeautifulSoup 
import os 
import sys 
import time
import warnings
from colorama import Fore, Back, Style 

warnings.filterwarnings('ignore')

PHANTOM_JS_PATH = './phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
CHROME_DRIVER_PATH = 'chromedriver_linux64'
MAX_RESULTS = 10000

class MetaSingleton(type):
	__instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls.__instances:
			cls.__instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
		return cls.__instances[cls]

class StatusBuilder:
	@staticmethod
	def prepate_console_output(counter_number, title, price, currency, search_keyword):
		output_title = ""
		title = title.upper()
		currency = currency.upper()
		search_keyword = search_keyword.upper()
		if search_keyword in title:
			start_pos = title.index(search_keyword)
			end_pos = start_pos + len(search_keyword)
			output_title = (
            	f"{Fore.CYAN}{counter_number}"
            	f"{Fore.WHITE}: "
            	f"{Fore.WHITE}{title[:start_pos]}"
            	f"{Fore.CYAN}{title[start_pos:end_pos]}"
            	f"{Fore.WHITE}{title[end_pos:]} "
            	f"{Fore.YELLOW}{price}"
            	f"{Fore.WHITE}{currency}"
       			)
		else:
			output_title = (
				f"{Fore.CYAN}{counter_number}"
            	f"{Fore.WHITE}: "
            	f"{Fore.WHITE}{title} "
            	f"{Fore.YELLOW}{price}"
            	f"{Fore.WHITE}{currency}"
            	)
		return output_title

class DataGraber(metaclass = MetaSingleton):
	def __init__(self, search_item, browser = 'phantom_js', show_process = False, max_results = MAX_RESULTS):
		if browser == 'phantom_js':
			self.webdriver = webdriver.PhantomJS(PHANTOM_JS_PATH)
		elif browser == "firefox":
			self.webdriver = webdriver.Firefox()
		elif browser == "chrome":
			options = webdriver.ChromeOptions()
			options.headless = True
			options.add_argument('--window-size=1200x600')
			self.webdriver = webdriver.Chrome(executable_path = CHROME_DRIVER_PATH , options = 'options')
		else:
			print('Error: there is no such webdriver')
			exit()

		self.search_item = search_item
		self.data = None
		self.show_process = show_process 
		self.max_results = max_results
		
		if self.show_process:
			print('Getting the data...')
		self.webdriver.get("https://tap.az/")

	def get_data_from_tapaz(self):
		product_list = []
		input_item = self.webdriver.find_element_by_xpath('//input[@id="keywords"]')
		button_item = self.webdriver.find_element_by_xpath("//button[@type='submit']")
		input_item.clear()
		input_item.send_keys(self.search_item)
		button_item.click()
		
		try:
			table = WebDriverWait(self.webdriver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='content']")))
			html = table.get_attribute('innerHTML')
			soup = BeautifulSoup(html, "lxml")
	
			all_products = [product for product in soup.find_all('div', attrs = {"class" : "products-i"})]
			item_counter = 0
			for product in all_products:
				if item_counter >= self.max_results:
					break
				item_counter += 1
				product_title = product.find('div', attrs = {'class':'products-name'}).text 
				product_date = product.find('div', attrs = {'class':'products-created'}).text 
				product_curr = product.find('span', attrs = {'class': 'price-cur'}).text
				product_price = product.find('span', attrs = {'class': 'price-val'}).text
				product_price = float("".join(product_price.strip().split()))

				product_list.append((product_title, product_price,product_curr, product_date))
				
				if self.show_process:
					output_builder = StatusBuilder.prepate_console_output(
						item_counter,
						product_title,
						product_price,
						product_curr,
						self.search_item
					)
					print(output_builder)

		finally:
			self.webdriver.quit()

		def get_contact_data_from_tap_az(self, link):
			res = {}
			response = requests(link)
			soup = BeautifulSoup(response, 'lxml')
			
			author = soup.find('div', attrs = {'class':'author'})
			shop_contact = soup.find('div', attrs = {'class':'shop-contact'})

			if author:
				phone_number = author.find('a', attrs = {'class':'phone'})
				author_name = author.find('div', attrs = {'class':'name'})
				
				res['type'] = 'private'
				res['phone_number'] = phone_number.text
				res['author_name'] = author_name.text  
			
			if shop_contact:
				phone_number =  shop_contact.find('a', attrs = {'class', 'shop-phones--number'})
				shop_title   =  shop_contact.find(attrs = {'class':'shop-contact--shop-name'})
				
				res['type'] = 'shop'	
				res['phone_number'] = phone_number.text 
				res['shop_title'] = shop_title.text 

			return res 

			
def main():
	if len(sys.argv) < 2:
		print('ERROR: you didn\'t entered the searched keyword')
		exit()
	search_request = sys.argv[1]
	if len(sys.argv) == 2:
		rs = DataGraber(search_request, show_process = True, max_results = 10) # edit chrome driver
		rs.get_data_from_tapaz()
	elif len(sys.argv) == 3:
		mx_out = int(sys.argv[2])
		rs = DataGraber(search_request, show_process = True, max_results = mx_out) # edit chrome driver
		rs.get_data_from_tapaz()

if __name__ == "__main__":
	main()