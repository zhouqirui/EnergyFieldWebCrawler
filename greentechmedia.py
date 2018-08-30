"""greentechmedia"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import share,selenium
import time

result_list = []
link_list = ['https://www.greentechmedia.com/','https://www.greentechmedia.com/P25','https://www.greentechmedia.com/P50']

def check_exist(title) -> bool:
	"""
	Return True if exists
	"""
	for result in result_list:
		if result.title == title:
			return True
	return False

def get_body(link) -> str:
	from urllib.request import urlopen,Request
	from bs4 import BeautifulSoup
	request = Request(link,headers={'User-Agent':'Mozilla/5.0'})
	webpage = urlopen(request)
	soup = BeautifulSoup(webpage,'html.parser')
	print(soup.find('p').get_text())

def find_body(link,driver) -> str:
	driver.get(link)
	time.sleep(2)
	text = None
	whole_text = None
	try:
		whole_text = driver.find_element_by_class_name('col-md-9 article-content')
	except Exception as e:
		whole_text = driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/article/div/div[1]')
	try:
		if whole_text != None:
			text = whole_text.find_element_by_tag_name('p').text.strip()
	except Exception as e:
		print(e)
	finally:
		driver.back()
		time.sleep(2)
		# driver.refresh()
		# time.sleep(5)
		if text != None:
			return text
		else:
			return "FAILED"

def featured_head(sublist,keyword_list,driver):
	title = sublist[3]
	if share.double_check(keyword_list,title):
		link_element = driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[2]/div[1]/article/div/div/h1/a')
		link = link_element.get_attribute("href")
		driver.get(link)
		body_element = driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/article/div/div[1]/p[1]')
		body = body_element.text.strip()
		driver.back()
		result_list.append(share.Page_info(link,title,body))

def feature_box(sublist,keyword_list,driver,count):
	title = sublist[2]
	if share.double_check(keyword_list,title):
		if count == 1:
			xpath = '//*[@id="content"]/div/div[1]/div[2]/div[2]/div/article[1]/div[3]/h2/a'
		elif count == 2:
			xpath = '//*[@id="content"]/div/div[1]/div[2]/div[2]/div/article[2]/div[3]/h2/a'
		link_element = driver.find_element_by_xpath(xpath)
		link = link_element.get_attribute("href")
		# body = find_body(link,driver)
		result_list.append(share.Page_info(link,title,None))

def process_featured(featured,keywords,driver):
	text = featured.text
	text_list = text.split("\n")
	copy_list = [t.rstrip().lstrip() for t in text_list if t != '' and t.rstrip().lstrip() != '']
	print(copy_list)
	sub1,sub2,sub3 = copy_list[0:4],copy_list[5:9],copy_list[10:14]
	featured_head(sub1,keywords,driver)
	feature_box(sub2,keywords,driver,1)
	feature_box(sub3,keywords,driver,2)

def add_to_result(block,title,year,month,day,driver,keyword_list):
	if share.double_check(keyword_list,title) and share.compare_date(year,month,day) and not check_exist(title):
		b = block.find_element_by_class_name('article-wrapper')
		link = b.find_element_by_tag_name('a').get_attribute('href')
		# body = find_body(link,driver)
		result_list.append(share.Page_info(link,title,None))
	return

def test_add(block,title,year,month,day,driver):
	b = block.find_element_by_class_name('article-wrapper')
	link = b.find_element_by_tag_name('a').get_attribute('href')
	body = find_body(link,driver)
	print(share.Page_info(link,title,body))

def clear_fix(block,keyword_list,driver):
	text_list = [text.strip() for text in block.text.split('\n') if text.strip() != '']
	title = text_list[3]
	date = text_list[0].split('.')
	add_to_result(block,title,date[2],date[0],date[1],driver,keyword_list)
	return

def clearfix_with_label(block,keyword_list,driver):
	text_list = [text.strip() for text in block.text.split('\n') if text.strip() != '']
	title = text_list[4]
	date = text_list[0].split('.')
	add_to_result(block,title,date[2],date[0],date[1],driver,keyword_list)

def squared_label(block,keyword_list,driver):
	text_list = [text.strip() for text in block.text.split('\n') if text.strip() != '']
	title = text_list[1]
	date = text_list[-1].split('|')[-1].strip().split()
	y,m,d = date[2],date[0],date[1][:-1]
	if share.double_check(keyword_list,title) and share.compare_date(y,m,d) and not check_exist(title):
		b = block.find_element_by_class_name('article-wrapper')
		link = b.find_element_by_tag_name('a').get_attribute('href')
		xpath = '//*[@id="wrapper"]/div[1]/div/div/section/div[2]/div/p'
		driver.get(link)
		para = driver.find_element_by_xpath(xpath)
		body = para.text
		result_list.append(share.Page_info(link,title,body))
		driver.back()

def same_h(block,keyword_list,driver):
	title = block.find_element_by_tag_name('h2').text
	date = block.find_element_by_tag_name('time').text
	if len(date.split('.')) == 1:
		date = date.split()
		y,m,d = date[2],date[0],date[1][:-1]
	else:
		date = date.split('.')
		y,m,d = date[2],date[0],date[1]
	if share.double_check(keyword_list,title) and share.compare_date(y,m,d) and not check_exist(title):
		b = block.find_element_by_tag_name('h2')
		link = b.find_element_by_tag_name('a').get_attribute('href')
		# body = find_body(link,driver)
		result_list.append(share.Page_info(link,title,None))

def feature_box(block,keyword_list,driver):
	title = block.find_element_by_tag_name('h1').text
	date = block.find_element_by_tag_name('time').text.split('.')
	y,m,d = date[2],date[0],date[1]
	if share.double_check(keyword_list,title) and share.compare_date(y,m,d) and not check_exist(title):
		b = block.find_element_by_tag_name('h1')
		link = b.find_element_by_tag_name('a').get_attribute('href')
		# body = find_body(link,driver)
		result_list.append(share.Page_info(link,title,None))

def list_article(block,keyword_list,driver):
	title = block.find_element_by_tag_name('h2').text
	date = block.find_element_by_tag_name('time').text.split('.')
	y,m,d = date[2],date[0],date[1]
	# print(title,date)
	if share.double_check(keyword_list,title) and share.compare_date(y,m,d) and not check_exist(title):
		link = block.find_element_by_tag_name('a').get_attribute('href')
		# body = find_body(link,driver)
		result_list.append(share.Page_info(link,title,None))
	# print(text_list)


def process_blocks(keyword_list,driver):
	blocks = driver.find_elements_by_tag_name('article')
	blocks_num = len(blocks)
	for n in range(blocks_num):
		try:
			# print(n)
			time.sleep(1)
			blocks = driver.find_elements_by_tag_name('article')
			# print(blocks)
			b = blocks[n]
			class_name = b.get_attribute('class')
			if class_name == 'article-item clearfix  ':
				clear_fix(b,keyword_list,driver)
			elif class_name == 'article-box same-h':
				# print("TEXT",b.text)
				same_h(b,keyword_list,driver)
			elif class_name == 'article-item clearfix squared with-label':
				squared_label(b,keyword_list,driver)
			elif class_name == 'article-item clearfix  with-label':
				clearfix_with_label(b,keyword_list,driver)
			elif class_name == 'article-box same-h same-height-left':
				# print("TEXT",b.text)
				same_h(b,keyword_list,driver)
			elif class_name == 'article-box same-h same-height-right':
				# print("TEXT",b.text)
				same_h(b,keyword_list,driver)
			elif class_name == 'featured-box':
				feature_box(b,keyword_list,driver)
			elif class_name == 'list-article col-sm-6 col-md-6':
				list_article(b,keyword_list,driver)
			# print(result_list[-1].link)
		except selenium.common.exceptions.StaleElementReferenceException:
			print(b.text)
			print('error selenium.common.exceptions.StaleElementReferenceException')
			continue
		except IndexError:
			continue	

def main(keyword_list:str):
	print("Searching GreenTechMedia......")
	# keywords = keyword.split()
	driver = webdriver.Chrome(share.FILE_PATH+'/chromedriver')
	try:
		for l in link_list:
			driver.get(l)
			process_blocks(keyword_list,driver)
		for page in result_list:
			driver.get(page.link)
			# print(page.link)
			time.sleep(2)
			try:
				content = driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/article/div/div[1]')
				page.body = content.find_element_by_tag_name('p').text.strip()
				# print(page.body)
			except selenium.common.exceptions.NoSuchElementException:
				page.body = driver.find_element_by_xpath('//*[@id="wrapper"]/div[1]/div/div/section/div[2]/div/p').text.strip()


		if len(result_list) != 0:
			share.write_file(result_list)
		print("Finished")
	finally:
		driver.close()

if __name__ == '__main__':
	main('battery, solar,wind'.split(','))
