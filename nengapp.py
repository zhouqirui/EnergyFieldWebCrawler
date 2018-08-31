
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

def generate_url(index: int) -> str:
	return 'https://www.nengapp.com/news/22/'+str(index)

def compare_date(text: str) -> bool:
	'''Return True if date is within 14 days, else False'''
	text_list = text.split()
	date = text_list[-1]
	if '昨天' in date or '前天' in date or '分钟' in date or '刚刚' in date or '小时' in date or '今天' in date:
		return True
	else:
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
				if share.double_check(keyword_list, title) and not check_exist(title):
					link = article.find_element_by_tag_name('a').get_attribute('href')
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