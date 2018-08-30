# -*- coding: utf-8 -*-

import share
import time as timer
from selenium import webdriver

result_list = []

def get_date(time:str):
	for i in range(len(time)):
		if not time[i].isdigit():
			index = i
			break
	m = time[:index]
	d = time[index+1:-1]
	return m,d

def process_articles(art_list: list,keyword_list:list) -> None:
	for article in art_list:
		title = article.find_element_by_class_name('article-item-title').text
		if share.double_check(keyword_list,title):
			link = article.find_element_by_tag_name('a').get_attribute('href')
			result_list.append(share.Page_info(link,title,None))
			# print(title,link)

def get_all_body(driver):
	for webpage in result_list:
		driver.get(webpage.link)
		timer.sleep(4)
		tags = driver.find_elements_by_tag_name('p')
		for tag in tags:
			if len(tag.text) >= 40:
				webpage.body = tag.text
				break

def main(keyword_list:str):
	while True:
		print('Searching Wusuobuneng......')
		driver = webdriver.Chrome(share.FILE_PATH+'/chromedriver')
		driver.get('http://www.wusuobuneng.com/')
		timer.sleep(7)
		try:
			button_xpath = '//*[@id="root"]/div/div[3]/div/div[3]/ul/li[1]/div[2]/button'
			while True:
				button = driver.find_element_by_xpath(button_xpath)
				button.click()
				timer.sleep(5)
				l = driver.find_elements_by_class_name('article-item')
				last_time = l[-1].find_element_by_class_name('article-item-time-icon').text
				m,d = get_date(last_time)
				if not share.compare_date(None,m,d):
					break
			timer.sleep(2)
			article_list = l
			process_articles(article_list,keyword_list)
			get_all_body(driver)
			if len(result_list) != 0:
				share.write_file(result_list)
			print('Finished')
		# except selenium.common.exceptions.NoSuchElementException:
		# 	main(keyword_list)
		except:
			pass
		else:
			break

		finally:
			driver.close()

if __name__ == '__main__':
	keyword = '新能源'.split('，')
	main(keyword)
