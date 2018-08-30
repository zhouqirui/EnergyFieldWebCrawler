
from selenium import webdriver
import share,time,selenium

link_list = ['https://cleantechnica.com/',
'https://cleantechnica.com/page/2/','https://cleantechnica.com/page/3/',
'https://cleantechnica.com/page/4/','https://cleantechnica.com/page/5/',
'https://cleantechnica.com/page/6/','https://cleantechnica.com/page/7/',
'https://cleantechnica.com/page/8/','https://cleantechnica.com/page/9/']

def main(keyword_list:list):
    print('Searching Cleantechnica......')
    result_list = []
    try:
        for l in link_list:
            driver = webdriver.Chrome(share.FILE_PATH+'/chromedriver')
            # print(l)
            driver.get(l)
            time.sleep(.1)
            driver.refresh()
            main_part = driver.find_elements_by_class_name('omc-blog-one')
            for article in main_part:
                date = article.find_element_by_class_name('omc-date-time-one').text.split('|')[0][13:-1].split()
                y,m,d = date[-1],date[0],date[1][:-3]
                title = article.find_element_by_tag_name('h2').text
                link = article.find_elements_by_tag_name('a')[1].get_attribute('href')
                if share.double_check(keyword_list,title) and share.compare_date(y,m,d):
                    result_list.append(share.Page_info(link,title,None))
            driver.close()
        driver = webdriver.Chrome(share.FILE_PATH+'/chromedriver')
        for page in result_list:
            driver.get(page.link)
            time.sleep(1)
            page.body = driver.find_element_by_xpath('//*[@id="omc-full-article"]/p[2]').text
            if len(page.body) <= 40:
                page.body = driver.find_element_by_xpath('//*[@id="omc-full-article"]/p[3]').text
                if len(page.body) <= 40:
                    page.body = driver.find_element_by_xpath('//*[@id="omc-full-article"]/p[4]').text
        if len(result_list) != 0:
            share.write_file(result_list)
        print('Finished')
    finally:
        try:
            driver.close()
        except selenium.common.exceptions.WebDriverException:
            pass


if __name__ == '__main__':
    keyword_list = ['energy iot','solar','wind']
    main(keyword_list)
