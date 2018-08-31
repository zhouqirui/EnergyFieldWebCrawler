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
    return False

def write_file(content) -> None:
    from datetime import date
    filename = 'Search Result on '+str(date.today())+'.txt'
    file = open(FILE_PATH + '/result/'+filename,"a")
    if type(content) == str:
        file.write(content)
    elif type(content) == list:
        for item in content:
            file.write(str(item)+'\n')
    return
