class FootyStats():
    def __init__(self,bot):
        self.bot = bot
        self.home = []
        self.away = []
        self.labelText = ["[1/2] Navigate to the home team",
                          "[2/2] Navigate to the away team"]
        self.tableIndex = 16
        self.steps = 2
        self.hasName = False
        

    def getLabelTexts(self): return self.labelText

    def fetchData(self,step):
        self.bot.updateSoup()
        print("yeyee",step)
##        print(self.bot.soup)
        try:
            name = self.bot.getData('span','class','mr05 fa-adjust-l1 flag flag-gb-eng')
            print(name)
            try: print(name.text)
            except: pass
            #leage rank
            selected = self.bot.getData('tr','class','leagueTeam selected')    
            position = self.bot.getData('p','class','pr mild-small',selected)

            #first table
            table = self.bot.getData('div','class','pa1e bbox w100 cf pb05e')
            
            goalsF = self.bot.getData('div','class','g',table,1) #list
            goalsA = self.bot.getData('div','class','a',table,1) #list

            ppg = self.bot.getData('div','class','p',table,1) #list

            L5 = self.bot.getData('ul','class','form-run',table,1) #list

            #second table
            table2 = self.bot.getData('table','class','mt1e comparison-table-table w100')

            rows = self.bot.getData('tr','class','row',table2,1)
            
            rows = table2.findAll('td')
            home,away = [],[]
            
            for i in range(0,16,4):
                home.append(rows[i+2].text)
                away.append(rows[i+3].text)


            if step == 1:
                self.home = [
                    goalsF[3].text, #Total goals
                    goalsA[3].text, #Total conceded
                    position.text,  #Position in league
                    goalsF[1].text, #Goals
                    goalsA[1].text, #Conceded
                    ppg[0].text,    #PPG
                    home[0],        #XG for
                    home[1],        #XG against
                    home[2],        #average goals
                    home[3]]        #average goals conceded
                print(self.home)
            
            elif step == 2:
                self.away = [
                    goalsF[3].text,
                    goalsA[3].text,
                    position.text,
                    goalsF[2].text,
                    goalsA[2].text,
                    ppg[1].text,
                    away[0],
                    away[1],
                    away[2],
                    away[3]]
                print(self.away)

        except Exception as e:
            print("Error with Footy Stats data collection:\n",e)
            return 0
        return 1


    def getTableData(self): return [self.home,self.away]

class FakeClass(): pass
        
if __name__ == "__main__":
    app = FootyStats(FakeClass())
