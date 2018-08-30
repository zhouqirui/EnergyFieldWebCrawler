from multiprocessing import Process
from pathlib import Path
import share,os
from datetime import date

try:
    import pip,os,subprocess,time
    import cleantechnica,cleantech,greentechmedia,azocleantech,nengapp,wusuobuneng
except ModuleNotFoundError:
    subprocess.check_call('pip','install','selenium')
    subprocess.check_call('pip','install','requests')
    os.system('python "main program.py"')
    
if __name__ == "__main__":
    filepath = Path(share.FILE_PATH+'/result/'+'Search Result on '+str(date.today())+'.txt')
    if filepath.is_file():
        os.remove(filepath)
        
    start_time = time.time()
    try:
        keyword_list = str(input("Enter keyword in English(seperated by comma): ")).split(',')
        chinese_keyword_list = str(input('输入中文关键词（用逗号分隔）: ')).split('，')

        p1 = Process(target = cleantechnica.main, args = (keyword_list,))
        p2 = Process(target = cleantech.main, args = (keyword_list,))
        p3 = Process(target = greentechmedia.main, args = (keyword_list,))
        p4 = Process(target = azocleantech.main, args = (keyword_list,))
        p5 = Process(target = nengapp.main, args = (chinese_keyword_list,))
        p6 = Process(target = wusuobuneng.main, args = (chinese_keyword_list,))
        p_list = [p1,p2,p3,p4,p5,p6]
        for p in p_list:
            p.start()

        for p in p_list:
            p.join()

        print("File has been written under the folder named 'result'")
        end_time = time.time()
        print('Total use time is '+str(end_time-start_time)+' seconds.')
    except Exception as e:
        print('Error occured, please restart the cralwer')
        print(e)
