import json
import os
from selenium import webdriver

#refs:
#https://blog.csdn.net/Demonslzh/article/details/125062240
#https://www.cnblogs.com/superhin/p/12600358.html

hostname=os.getlogin()
CHROME_PATH = f"C:/Users/{hostname}/AppData/Local/Google/Chrome/User Data/Default"
EDGE_PATH = f"C:/Users/{hostname}/AppData/Local/Microsoft/Edge/User Data/Default"
EDGE_KILL = "taskkill /f /t /im msedge.exe"
CHROME_KILL = "taskkill /f /t /im chrome.exe"
print(EDGE_PATH)

class BookMark:

    def __init__(self, Path=EDGE_PATH):
        # chromepath
        self.Path = Path
        # refresh bookmarks
        self.bookmarks = self.get_bookmarks()
        self.driver = webdriver.Edge()

    def get_folder_data(self):
        self.creatfolder(r"./本地收藏夹") #可以改成绝对路径
        for mark_name, item in self.bookmarks["roots"].items():
            self.dfs(item,r"./本地收藏夹")

    def get_bookmarks(self):
        'update chrome data from chrome path'
        # parse bookmarks
        assert os.path.exists(
            os.path.join(self.Path,
                         'Bookmarks')), "can't found ‘Bookmarks’ file,or path isn't a chrome browser cache path!"
        with open(os.path.join(self.Path, 'Bookmarks'), encoding='utf-8') as f:
            return json.loads(f.read())

    def creatfolder(self,path):
        try:
            os.makedirs(path)
        except Exception:
            print(Exception)
    
    def creatmhtml(self,path,url):
        res={"data":"null"}
        try:
            self.driver.get(url)
        # 1. 执行 Chome 开发工具命令，得到mhtml内容
        
            res = self.driver.execute_cdp_cmd('Page.captureSnapshot', {})
        except Exception:
            print(Exception)
        # 2. 写入文件
        with open((r"{}".format(path+".mhtml")), 'w', newline='') as f:#吾爱破解 - LCG - LSG|安卓破解|病毒分析|www.52pojie.cn.mhtml 会报错，
                                                                       #研究许久发现文件名不能有|以及其他一些符号，具体自己找个文件重命名试一下即可，会有提示的
            f.write(res['data'])

    def dfs(self,root,path):
        e="bug"
        if root["type"]=="url":
            self.creatmhtml(r"{}".format(path+'/'+root["name"].translate(str.maketrans({'/':e,'\\':e,'|':e,':':e,'*':e,'?':e,'"':e,'<':e,'>':e}))),root["url"])
        elif root["type"]=="folder":
            self.creatfolder(path+'/'+root["name"].translate(str.maketrans({'/':e,'\\':e,'|':e,':':e,'*':e,'?':e,'"':e,'<':e,'>':e})))
            for i in root["children"]:
                    self.dfs(i,r"{}".format(path+'/'+root["name"].translate(str.maketrans({'/':e,'\\':e,'|':e,':':e,'*':e,'?':e,'"':e,'<':e,'>':e}))))

    
test=BookMark()
test.get_folder_data()