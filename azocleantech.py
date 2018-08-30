"""azocleantech"""
from selenium import webdriver
import share,selenium

result_list = []

def create_xpath(i:int) -> str:
	return '//*[@id="ctl00_cphBody_latestNewsItems_posts"]/div['+str(2*i+1)+']'

def get_link(i:int,driver) -> (str,str):
	xpath = create_xpath(i)
	article_element = driver.find_element_by_xpath(xpath)
	link = article_element.find_element_by_tag_name('h3').find_element_by_tag_name('a').get_attribute('href')
	body = article_element.find_element_by_tag_name('p').text
	return link,body

def main(keyword_list:list):
	print("Searching Azocleantech......")
	driver = webdriver.Chrome(share.FILE_PATH+'/chromedriver')
	driver.get('https://www.azocleantech.com/news-index.aspx')
	try:
		main_part = driver.find_element_by_xpath('//*[@id="ctl00_cphBody_latestNewsItems_posts"]')
		full_list = main_part.find_elements_by_class_name('row')
		striped = [a.text.strip() for a in full_list]
		length = int(len(striped)/2)
		for i in range(length):
			title_and_despt = striped[2*i].split('\n')
			title = title_and_despt[0].strip()
			date = striped[2*i+1].split('\n')[-1].strip().split()
			y,m,d = date[2],date[1],date[0]
			if share.compare_date(y,m,d) and share.double_check(keyword_list,title):
				link,body = get_link(i,driver)
				result_list.append(share.Page_info(link,title,body))
		if len(result_list) != 0:
			share.write_file(result_list)
		print("Finished")
	finally:
		driver.close()


if __name__ == '__main__':
	keyword = str(input("Enter keyword: "))
	main(keyword.split(','))