
import share
from selenium import webdriver
import time

result_list = []

def check_exist(title) -> bool:
	"""
	Return True if exists
	"""
	for result in result_list:
		if result.title == title:
			return True
	return False

def get_day(t:str) -> int:
	str_d = ''
	for char in t:
		if char.isdigit():
			str_d += char
	return int(str_d)

def main(keyword_list:str):
	print("Searching NengApp......")
	driver = webdriver.Chrome(share.FILE_PATH+'/chromedriver')
	try:
		driver.get('https://www.nengapp.com/')
		time.sleep(2)
		button = driver.find_element_by_xpath('//*[@id="loading_more"]')
		times = 0
		last_len = 0
		while True:
			button.click()
			# print(n)
			time.sleep(1)
			l = driver.find_elements_by_class_name('news')
			if len(l) == last_len:
				times += 1
			t = l[-1].find_element_by_class_name('time')
			last_len = len(l)
			if times >= 5:
				break
			if '天' in t.text:
				days = get_day(t.text)
				if days >= 14:
					break
		article_list = driver.find_elements_by_class_name('news')
		for article in article_list:
			link = article.find_element_by_tag_name('a').get_attribute('href')
			title = article.find_element_by_tag_name('a').get_attribute('title')
			if not check_exist(title):
				if share.double_check(keyword_list,title):
					result_list.append(share.Page_info(link,title,None))
		for webpage in result_list:
			driver.get(webpage.link)
			time.sleep(1)
			paragraphs = driver.find_elements_by_tag_name('p')
			webpage.body = paragraphs[0].text if len(paragraphs[0].text) >= 10 else paragraphs[1].text
		if len(result_list) != 0:
			share.write_file(result_list)
		print('Finished')
	finally:
		driver.close()

if __name__ == '__main__':
	keyword = '新能源'
	main(keyword.split(','))