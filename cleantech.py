"""cleantech"""
from selenium import webdriver
import share

result_list = []

def process(date:str) -> bool:
	real_date = date[:date.find('20')+4].split()
	y,m,d = real_date[-1],real_date[0],real_date[1][:-1]
	return share.compare_date(y,m,d)

def generate_xpath(post_id):
	return '//*[@id="'+post_id+'"]/header/h1/a'

def main(keyword_list:str):
        print("Searching CleanTech......")
        driver = webdriver.Chrome(share.FILE_PATH+'/chromedriver')
        try:
                driver.get("https://www.cleantech.com/category/cleantech-news/")
                main_xpath = '//*[@id="main"]/section[2]/div'
                blocks = driver.find_elements_by_tag_name("article")
                for article in blocks:
                        whole_text = article.text.rstrip().lstrip()
                        sentence_list = whole_text.split('\n')
                        copy_list = list(sentence_list)
                        for item in sentence_list:
                                strip = item.rstrip().lstrip()
                                if strip == '':
                                        copy_list.remove(item)
                        final_list = [sentence.rstrip().lstrip() for sentence in copy_list]

                        title = final_list[0].encode('utf8').decode('utf-8','strict')
                        date = final_list[1][10:]
                        if process(date):
                                if share.double_check(keyword_list,title):
                                        description = final_list[2]
                                        post_id = article.get_attribute('id')
                                        xpath = generate_xpath(post_id)
                                        link_element = driver.find_element_by_xpath(xpath)
                                        link = link_element.get_attribute('href')
                                        result_list.append(share.Page_info(link,title,description))
                                else:
                                        continue
                        else:
                                continue
                if len(result_list) != 0:
                        share.write_file(result_list)
                print("Finished")
        finally:
                driver.close()

if __name__ == '__main__':
        keyword = str(input("Enter keyword: "))
        main(keyword.split(','))