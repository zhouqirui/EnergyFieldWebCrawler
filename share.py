"""
Share file
Common functions
"""

FILE_PATH="/Users/zhouqirui/Documents/Projects/Crawler-V2"

class Page_info:
    def __init__(self,link,title,body):
        self.link = link
        self.title = title
        self.body = body
    def __repr__(self):
        return "Title: "+self.title+"\nBody: "+self.body+"\nLink: "+self.link+"\n"

def open_url(link:str) -> 'urlopen object':
    from urllib.request import Request,urlopen
    request = Request(link,headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(request)
    return webpage

def get_all_links(link:str) -> list:
    from lxml import html,etree
    result = []
    webpage = open_url(link)
    content = html.fromstring(webpage.read())
    for link in content.xpath('//a/@href'):
        result.append(link)
    return result

def get_url_hostname(link:str) -> str:
    from urllib.parse import urlparse
    parsed = urlparse(link)
    return parsed.hostname

def get_url_path(link:str) -> str:
    from urllib.parse import urlparse
    parsed = urlparse(link)
    return parsed.path

def get_url_title(link:str) -> str:
    import re
    url = open_url(link)
    content = str(url.read())
    match = re.search('<title>(.*?)</title>',content)
    if match == None:
        return "No title"
    title = match.group(1)
    return title

def compare_date(y,m,d) -> bool:
    """
    Return True if within 14 days
    False otherwise
    """
    import datetime
    current = datetime.datetime.now()
    if y == None:
        y = str(current.year)
    if len(y) == 2:
        y = '20'+y
    try:
        webpage_time = datetime.datetime.strptime(y+' '+m+' '+d,"%Y %m %d")
    except ValueError:
        try:
            webpage_time = datetime.datetime.strptime(y+' '+m+' '+d,"%Y %B %d")
        except ValueError:
            webpage_time = datetime.datetime.strptime(y+' '+m+' '+d,"%Y %b %d")
    return webpage_time + datetime.timedelta(days=14) >= current

def double_check(keyword_list,title) -> bool:
    is_in = True
    for keyword in keyword_list:
        keyword = keyword.strip()
        for word in keyword.split():
            if word.lower() not in title.lower():
                is_in = False
        if is_in == True:
            return is_in
        is_in = True
                # break
    return False

def write_file(content) -> None:
    from datetime import date
    filename = 'Search Result on '+str(date.today())+'.txt'
    file = open(FILE_PATH + '/result/'+filename,"a")
    # file.write("Search Result for \""+keyword+'\"\n')
    if type(content) == str:
        file.write(content)
    elif type(content) == list:
        for item in content:
            file.write(str(item)+'\n')
    return
