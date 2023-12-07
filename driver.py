from bs4 import BeautifulSoup
from selenium import webdriver

class Driver():
    def __init__(self):
        self.soup = "asd"
        self.driverStarted = False
        

    def startDriver(self,url="https://google.co.uk",xPos=539,scale=1.0):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors-spki-list')
            options.add_argument('--ignore-ssl-errors')
            self.driver = webdriver.Chrome('C:\Webdriver\chromedriver.exe',options=options)
            self.driver.set_window_position(xPos, 0, windowHandle='current')
            self.driver.set_window_size(1544-xPos,1080)
            self.driverStarted = True
            self.driver.implicitly_wait(30)
            self.driver.get(url)
        except Exception as e: print("bot.startDriver",e)

    def closeDriver(self):
        self.driver.quit()
        self.driverStarted = False

    def updateSoup(self):
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
    def getData(self, tag, ID, value, within=False, All=False):
        if self.soup == "":
            print("error: soup not made yet")
            return
        else:
##            print(self.soup)
            item = None
            try:
                if(within and All): item = within.findAll(tag,{ID:value})
                elif(within): item = within.find(tag,{ID:value})
                elif(All): item = self.soup.findAll(tag,{ID:value})
                else: item = self.soup.find(tag,{ID:value})
            except Exception as e: print("data collection error:\n",e)

            return item

    def getNum(self,s):
        new = ""
        for i in range(len(s)):
            try: new += str(int(s[i]))
            except: pass
        return int(new)
        


if __name__ == '__main__':
    app = Driver()
    print(app.getNum("*10"))
##    print("u cannot do this DUMBASS")


