
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

# def get_day(t:str) -> int:
# 	str_d = ''
# 	for char in t:
# 		if char.isdigit():
# 			str_d += char
# 	return int(str_d)

# def main(keyword_list:str):
# 	print("Searching NengApp......")
# 	driver = webdriver.Chrome(share.FILE_PATH+'/chromedriver')
# 	try:
# 		driver.get('https://www.nengapp.com/')
# 		time.sleep(2)
# 		button = driver.find_element_by_xpath('//*[@id="loading_more"]')
# 		times = 0
# 		last_len = 0
# 		while True:
# 			button.click()
# 			# print(n)
# 			time.sleep(1)
# 			l = driver.find_elements_by_class_name('news')
# 			if len(l) == last_len:
# 				times += 1
# 			t = l[-1].find_element_by_class_name('time')
# 			last_len = len(l)
# 			if times >= 5:
# 				break
# 			if '天' in t.text:
# 				days = get_day(t.text)
# 				if days >= 14:
# 					break
# 		article_list = driver.find_elements_by_class_name('news')
# 		for article in article_list:
# 			link = article.find_element_by_tag_name('a').get_attribute('href')
# 			title = article.find_element_by_tag_name('a').get_attribute('title')
# 			if not check_exist(title):
# 				if share.double_check(keyword_list,title):
# 					result_list.append(share.Page_info(link,title,None))
# 		for webpage in result_list:
# 			driver.get(webpage.link)
# 			time.sleep(1)
# 			paragraphs = driver.find_elements_by_tag_name('p')
# 			webpage.body = paragraphs[0].text if len(paragraphs[0].text) >= 10 else paragraphs[1].text
# 		if len(result_list) != 0:
# 			share.write_file(result_list)
# 		print('Finished')
# 	finally:
# 		driver.close()

def generate_url(index: int) -> str:
	return 'https://www.nengapp.com/news/22/'+str(index)

def compare_date(text: str) -> bool:
	'''Return True if date is within 14 days, else False'''
	text_list = text.split()
	date = text_list[-1]
	if '昨天' in date or '前天' in date or '分钟' in date or '刚刚' in date or '小时' in date or '今天' in date:
		return True
	else:
		# print('date',date)
		date_list = date.split('-')
		y, m, d = date_list[0], date_list[1], date_list[2]
		return share.compare_date(y, m, d)



def main(keyword_list):
	print("Searching NengApp......")
	driver = webdriver.Chrome(share.FILE_PATH+'/chromedriver')
	index = 0
	finish = False
	try:
		while True:
			url = generate_url(index)
			driver.get(url)
			article_list = driver.find_elements_by_class_name('news-item')
			for article in article_list:
				info = article.find_element_by_class_name('news-info')
				if compare_date(info.text) == False:
					finish = True
					break
				content = article.find_element_by_class_name('news-content')
				title = content.find_element_by_tag_name('a').text
				# print(title)
				if share.double_check(keyword_list, title) and not check_exist(title):
					link = article.find_element_by_tag_name('a').get_attribute('href')
					# print(link)
					result_list.append(share.Page_info(link, title, None))
			if finish:
				break
			index += 1
		for page in result_list:
			driver.get(page.link)
			paragraphs = driver.find_elements_by_tag_name('p')
			for p in paragraphs:
				if len(p.text) >= 15:
					page.body = p.text
					break
		share.write_file(result_list)
		print('Finished')
	finally:
		driver.close()


if __name__ == '__main__':
	keyword = '新能源'
	main(keyword.split(','))