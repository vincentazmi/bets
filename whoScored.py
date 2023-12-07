class WhoScored():
    def __init__(self,bot):
        self.bot = bot
        self.home = []
        self.away = []
        self.labelText = ["[1/7] Navigate to the home team",
                          "[2/7] Now navigate to squad stats home table",
                          "[3/7] Now navigate to fixtures -> select league",
                          "[4/7] Now navigate to the h2h page",
                          "[5/7] Navigate to the away team",
                          "[6/7] Now navigate to sqaud stats away table",
                          "[7/7] Now navigate to fixtures -> select league"]
        
        self.tableIndex = 0
        self.steps = 7
        self.hasName = True
        

    def getLabelTexts(self): return self.labelText

    def fetchData(self,step):
        self.bot.updateSoup()
        if step == 1 or step == 5: #summary page
            table = self.bot.getData('tbody','id','player-table-statistics-body')
            
            above7,below65 = 0,0
            for row in table:
                rating = self.bot.getData('td','class','rating sorted',row).text
                if float(rating) > 7: above7 += 1
                elif float(rating) < 6.5: below65 += 1

            if step == 1:
                self.HOMEabove7 = above7
                self.HOMEbelow65 = below65
            elif step == 5:
                self.AWAYabove7 = above7
                self.AWAYbelow65 = below65
                
        elif step == 2 or step == 6: #player stats
            try:
                table = self.bot.getData('tbody','id','player-table-statistics-body')
                strengths = self.bot.getData('div','class','col12-lg-6 col12-m-6 col12-s-12 col12-xs-12 strengths')
                weaknesses = self.bot.getData('div','class','col12-lg-6 col12-m-6 col12-s-12 col12-xs-12 weaknesses')
                
                HAabove7,HAbelow65 = 0,0
                for row in table:
                    rating = self.bot.getData('td','class','rating sorted',row).text
                    if float(rating) > 7: HAabove7 += 1
                    elif float(rating) < 6.5: HAbelow65 += 1

                sCount,wCount = 0,0
                s = strengths.findAll('div',{'class':'character'})
                for x in s:
                    real = x.text.split()
                    for i in range(len(real)):
                        if real[i] == "Very": sCount += 1
                        elif real[i] == "Strong": sCount += 1

                w = weaknesses.findAll('div',{'class':'character'})
                for x in w:
                    real = x.text.split()
                    for i in range(len(real)):
                        if real[i] == "Very": wCount += 1
                        elif real[i] == "Weak": wCount += 1
##                print("sw",sCount,wCount)
                if step == 2:
                    self.HOMEHAabove7 = HAabove7
                    self.HOMEHAbelow65 = HAbelow65
                    self.HOMEsCount = sCount
                    self.HOMEwCount = wCount
                elif step == 6:
                    self.AWAYHAabove7 = HAabove7
                    self.AWAYHAbelow65 = HAbelow65
                    self.AWAYsCount = sCount
                    self.AWAYwCount = wCount
                    
            except Exception as e: print("uiashfuisa",e)
                
        
        elif step == 3 or step == 7: # league
            table = self.bot.getData('div','class','divtable-body')

            WDL,scores = [],[]
            for row in table:
                try:
                    WDL.append(self.bot.getData('div','class',
'col12-lg-1 col12-m-1 col12-s-1 col12-xs-1 divtable-data form-fixtures',row).text)
                    scores.append(self.bot.getData('a','class','horiz-match-link result-1',row).text)
                except: pass

            scores.reverse()
            WDL.reverse()

            WDL10 = WDL[:10]
            WDL5 = WDL[:5]


            
            L5points,L10points = 0,0
            count = 0
            for x in WDL10:
                if x == "w":
                    if count < 5: L5points += 3
                    L10points += 3
                elif x == "d":
                    if count < 5: L5points += 1
                    L10points += 1
                count += 1


            goals5,goals10 = 0,0
            conc5,conc10 = 0,0
            clean5,clean10 = 0,0
            
            for i in range(10):
                if WDL10[i] == "w":
                    if i <= 4:
                        goals5 += max(int(scores[i][0]),int(scores[i][4]))
                        conc5 += min(int(scores[i][0]),int(scores[i][4]))
                    goals10 += max(int(scores[i][0]),int(scores[i][4]))
                    conc10 += min(int(scores[i][0]),int(scores[i][4]))

                    if min(int(scores[i][0]),int(scores[i][4])) == 0:
                        if i <= 4: clean5 += 1
                        clean10 += 1

                elif WDL10[i] == "d":
                    if i <= 4:
                        goals5 += int(scores[i][0])
                        conc5 += int(scores[i][0])
                    goals10 += int(scores[i][0])
                    conc10 += int(scores[i][0])
                    
                elif WDL10[i] == "l":
                    if i <= 4:
                        goals5 += min(int(scores[i][0]),int(scores[i][4]))
                        conc5 += max(int(scores[i][0]),int(scores[i][4]))
                    goals10 += min(int(scores[i][0]),int(scores[i][4]))
                    conc10 += max(int(scores[i][0]),int(scores[i][4]))

            if step == 3:
                self.HOMEL5points = L5points
                self.HOMEgoals5 = goals5
                self.HOMEconc5 = conc5
                self.HOMEclean5 = clean5
                self.HOMEL10points = L10points
                self.HOMEgoals10 = goals10
                self.HOMEconc10 = conc10
                self.HOMEclean10 = clean10
                
            elif step == 7:
                self.AWAYL5points = L5points
                self.AWAYgoals5 = goals5
                self.AWAYconc5 = conc5
                self.AWAYclean5 = clean5
                self.AWAYL10points = L10points
                self.AWAYgoals10 = goals10
                self.AWAYconc10 = conc10
                self.AWAYclean10 = clean10

        elif step == 4: # h2h
            
            header = self.bot.getData('div','id','match-header')
            homeName = self.bot.getData('span','class',
'col12-lg-4 col12-m-4 col12-s-0 col12-xs-0 home team',header).text
            
            awayName = self.bot.getData('span','class',
'col12-lg-4 col12-m-4 col12-s-0 col12-xs-0 away team',header).text
            print(homeName, awayName)
            date = self.bot.getData('div','class','info-block cleared',header,All=True)
##            print(len(date))
##            for i,x in enumerate(date):
##                print(i,type(x),type(x.text),x.text,"\n")

            for i,x in enumerate(date):
                if x.text != "":
                    z = x.text.split(":")
                    self.DATE = ' '.join([z[0],z[1]+":"+z[2][:2],z[3]])
                    print(self.DATE)
##                    print(z[0],z[1]+":"+z[2][:2],z[3])


            
            
            table = self.bot.getData('div','class','divtable-body')

            homeGoals,awayGoals = 0,0
            homePoints,awayPoints = 0,0
            for x in table:
                scoreA = self.bot.getNum(x.find('div',{'class':'home-score'}).text)
                scoreB = self.bot.getNum(x.find('div',{'class':'away-score'}).text)
                leftTeam = x.find('a',{'class':'team-link'}).text

                if scoreA == scoreB:
                    homePoints += 1
                    awayPoints += 1
                    
                elif scoreA > scoreB:
                    if leftTeam == homeName: homePoints += 3
                    elif leftTeam == awayName: awayPoints += 3
                    else: print("math error bruh")
                    
                elif scoreB > scoreA:
                    if leftTeam == homeName: awayPoints += 3
                    elif leftTeam == awayName: homePoints += 3
                    else: print("math error bruh2")
                    
                if leftTeam == homeName:
                    homeGoals += scoreA
                    awayGoals += scoreB
                    
                elif leftTeam == awayName:
                    awayGoals += scoreA
                    homeGoals += scoreB

            #date
            

            self.HOMEname = homeName
            self.HOMEpoints = homePoints
            self.HOMEgoals = homeGoals
            self.AWAYname = awayName
            self.AWAYpoints = awayPoints
            self.AWAYgoals = awayGoals

        if step == 7:
            self.home = [self.HOMEpoints,
                         self.HOMEgoals,
                         self.HOMEL5points,
                         self.HOMEgoals5,
                         self.HOMEconc5,
                         self.HOMEclean5,
                         self.HOMEL10points,
                         self.HOMEgoals10,
                         self.HOMEconc10,
                         self.HOMEclean10,
                         self.HOMEabove7,
                         self.HOMEbelow65,
                         self.HOMEHAabove7,
                         self.HOMEHAbelow65,
                         self.HOMEsCount,
                         self.HOMEwCount]
            
            self.away = [self.AWAYpoints,
                         self.AWAYgoals,
                         self.AWAYL5points,
                         self.AWAYgoals5,
                         self.AWAYconc5,
                         self.AWAYclean5,
                         self.AWAYL10points,
                         self.AWAYgoals10,
                         self.AWAYconc10,
                         self.AWAYclean10,
                         self.AWAYabove7,
                         self.AWAYbelow65,
                         self.AWAYHAabove7,
                         self.AWAYHAbelow65,
                         self.AWAYsCount,
                         self.AWAYwCount]



    def getTableData(self): return [self.home,self.away]

    def getHeaders(self): return [self.DATE,self.HOMEname,self.AWAYname]

class FakeClass(): pass
        
if __name__ == "__main__":
    app = WhoScored(FakeClass())



