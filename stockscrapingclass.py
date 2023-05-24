class StockScraper:
    filedefault = 'scrapeddata.csv'
    # calling the quote getter function is the fastest way to get data
    """ Documentation:
            initialise the function.
            call getcsvdata function to set data from a specific file
            call quotegetter function to identify data from the specific file
            
    """

    def __init__(self):

        self.df = None
        self.filename = None
        self.targets = None

    def filedata(self, path=None):
        filedefault = 'scrapeddata_template.csv'
        # identify file
        if path is None:
            self.filename = filedefault
        else:
            self.filename = path

        # getting the data from file
        # todo move to a different method
        import pandas as pd
        df = pd.read_csv(self.filename)
        self.df = df

    # main method, to identify and get stock data
    def quotegetter(self, targets=None):

        import re
        import time
        # getting timestamp and assigning it to first value
        clocker = time.localtime()
        timestamp = str(clocker[2]) + "-" + str(clocker[1]) + "-" + str(clocker[0])
        valuefinal = [timestamp]
        if targets is not None:
            self.targets = targets
        # checking for user defined targets
        else:
            self.identifytargets()
        # in case single user defined string
        if type(self.targets) is str:

            splitr = re.split(":", self.targets)

            # clean whitespaces
            for s in range(0, len(splitr)):
                splitr[s] = splitr[s].strip()

            # try to connect and get the values

            valuefinal.append(self.getgfinancequote(splitr[0], splitr[1]))

            return valuefinal

        else:
            # split each item in list and get values
            for i in self.targets:
                splitr = re.split(":", i)

                # clean whitespaces
                for s in range(0, len(splitr)):
                    splitr[s] = splitr[s].strip()
                    # print(splitr[s])
                valueinst = self.getgfinancequote(splitr[0], splitr[1])
                if valueinst=='Fatal error, please verify targets assigned':
                    return valueinst+'Error in ticker '+str(splitr[1])
                valuefinal.append(valueinst)
            #if input("Do you want to plot the points? Reply yes or no(ensure lowercase): ") == "yes":
                #self.filewriter(valuefinal)
            self.df = self.df.append(valuefinal)
            return valuefinal

    def filewriter(self, vallist):
        # Appending to file
        from csv import writer
        valwriter = open(self.filename, 'a')
        writerobj = writer(valwriter)
        writerobj.writerow(vallist)
        valwriter.close()

    # methods called by main methods, do not modify unless you know what you are doing
    def identifytargets(self):

        # identify and extract the target stock tickers
        # Getting the list of stocks, and getting values
        import re
        collist = list(self.df.columns)
        targetlist = []
        for potent in collist:
            if re.search(":", potent):
                targetlist.append(potent)

        self.targets = targetlist

    def getgfinancequote(self, exchangename, stockname):
        import requests
        from bs4 import BeautifulSoup
        import re
        # get values for specific target tickers from Google Finance
        baseurl = 'https://www.google.com/finance/quote/' + str(stockname) + ':' + str(exchangename)
        try:
            googlescrape = requests.get(baseurl)
        except:
            return 'Fatal error, please verify targets assigned'


        googlesoup = BeautifulSoup(googlescrape.content, 'html5lib')
        targetvalues = googlesoup.find('div', attrs={'class': 'YMlKec fxKbKc'}).text
        # get the numbers and convert to number value

        splittxt = re.split('', targetvalues.strip())
        for count, suspects in enumerate(splittxt):
            try:
                int(suspects)
            except:
                continue
            else:
                goldspot = count - 1
                break
        targetvalues = targetvalues[goldspot:]
        targetvalues = targetvalues.strip()
        targetvalues = self.cleanstrtonum(targetvalues)
        return targetvalues

    def cleanstrtonum(self, value):
        import locale
        locale.setlocale(locale.LC_ALL, '')
        returnval = locale.atof(value)
        return returnval

    def growthindex(self):
        # returns an array of growth values for each target
        finalgrowthlist = [self.df['Dates'].tolist()]
        for labelnames in self.df.columns:
            if labelnames != 'Dates':
                interimgrowthlist = []
                for count, rows in enumerate(self.df.index.astype('int')):
                    if rows != 0:
                        interimgrowthlist.append(
                            int(self.df[labelnames][rows]) - int(self.df[labelnames][int(rows) - 1]))

                    else:
                        if int(self.df[labelnames][rows]) != 0:
                            interimgrowthlist.append(int(self.df[labelnames][rows]))

                    if (int(len(self.df.index)) - 1) == int(count):
                        interimgrowthlist.append(int(self.df[labelnames][rows]))

                finalgrowthlist.append(interimgrowthlist)
        return finalgrowthlist

    def movementindex(self):

        dataframe_for_calculation=self.df.iloc[[-2,-1]]

        print(dataframe_for_calculation)
        print(type(dataframe_for_calculation))

        print(dataframe_for_calculation[[columns for columns in dataframe_for_calculation.columns if columns != 'Dates']].iloc[1]-dataframe_for_calculation[[columns for columns in dataframe_for_calculation.columns if columns != 'Dates']].iloc[0])

    """def basiccandlestick(self, movementvalues, targetticker=1):
        import matplotlib.pyplot as plt
        # import numpy as np
        import pandas as pd
        # import datetime
        import matplotlib.dates as mpl_dates

        xaxis = pd.DataFrame({'Dates': movementvalues[0]})
        xaxis['Dates'] = pd.to_datetime(xaxis['Dates'])
        xaxis['Dates'] = xaxis['Dates'].apply(mpl_dates.date2num)
        xaxis.drop(index=len(xaxis) - 1, inplace=True)
        xaxis = xaxis['Dates'].tolist()

        # targetticker = 1  # placeholdervalue
        interimvalues = [100]
        basevalueidentified = False
        for count, candidates in enumerate(movementvalues[targetticker]):
            if not basevalueidentified:
                if candidates > 0:
                    basevalue = candidates
                    basevalueidentified = True
                    continue
            else:
                if int(len(movementvalues[targetticker]) - 1) == int(count):
                    closeval = candidates
                else:
                    interimvalues.append(100 + ((candidates / basevalue) * 100))

        finalvalues = pd.DataFrame({'Movements': interimvalues}, index=xaxis)
        finalupvalues = finalvalues[finalvalues.Movements >= 0]
        finaldownvalues = finalupvalues[finalvalues.Movements < 0]

        plt.figure()
        plt.ylim(min(finalupvalues['Movements']), max(finalvalues['Movements']))
        plt.bar(finalupvalues.index, finalupvalues.Movements, .7, color='green')
        plt.bar(finaldownvalues.index, finaldownvalues.Movements, .3, finaldownvalues.Movements - 2, color='red')
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()
        plt.show()"""

mainclass=StockScraper()
mainclass.filedata()
mainclass.movementindex()
