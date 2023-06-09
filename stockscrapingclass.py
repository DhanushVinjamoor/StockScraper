import pandas as pd


class StockScraper:
    # filedefault = 'scrapeddata.csv'
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

        import pandas as pd
        df = pd.read_csv(self.filename, index_col=[0, 1])

        # if there are any empty rows, drop them, and fill in incomplete rows with 0

        df.dropna(how="all", inplace=True)
        df.fillna(value=0, inplace=True)

        # set the datetime index to pandas datetime and localise to Indian timezone .Initially, a normal pandas
        # datetime value was utilized. However, this caused issues when reading the df and adding new rows to the df.
        # As a countermeasure, all values read from and written to the csv are first passed through timezone
        # localisations

        from pytz import timezone

        indian_tz = timezone('Asia/Kolkata')
        try:
            df.index.set_levels(
                pd.to_datetime(df.index.get_level_values('Dates'), format='%Y-%m-%d %H:%M:%S.%f').tz_localize(indian_tz),
                level='Dates', inplace=True, verify_integrity=False)
        except TypeError:
            df.index.set_levels(
                pd.to_datetime(df.index.get_level_values('Dates'), format='%Y-%m-%d %H:%M:%S.%f').tz_convert(
                    indian_tz),
                level='Dates', inplace=True, verify_integrity=False)

        self.df = df

    # main method, to identify and get stock data
    def quotegetter(self, targets=None):

        import re
        from datetime import datetime

        # getting timestamp, utilised when returning final value

        import pytz
        indian_tz = pytz.timezone('Asia/Kolkata')
        timestamp = indian_tz.localize(datetime.now())

        # initialise the list that holds the values that are scraped. A nested list is needed, as a multi level index
        # dataframe is utilised, and each row to be written to the df needs to be a list, which in turn is nested in
        # list.

        valuefinal = []

        # if targets are provided as an argument, the argument is set as the target. If no arguments are provided,
        # the identify targets method will use the level 0 index values as the targets

        if targets is not None:
            self.targets = targets
        # checking for user defined targets
        else:
            self.targets = self.identifytargets()
        # in case single user defined string

        # the string cleaning is necessary as a failsafe when attempting to establish a connection, as unnecessary
        # whitespace may cause a bad url

        if type(self.targets) is str:

            splitr = re.split(":", self.targets)

            # clean whitespaces
            for s in range(0, len(splitr)):
                splitr[s] = splitr[s].strip()

            # try to connect and get the values
            # the gfinance method returns a list of values in the format - open,high,low,close

            valuefinal.append(self.getgfinancequote(splitr[0], splitr[1]))

            # error handling
            if valuefinal[0] == 'Fatal error, please verify targets assigned':
                return valuefinal[0] + 'Error in ticker ' + str(self.targets)

            self.df = self.add_values_toFrame_handler(self.targets, timestamp, valuefinal)

            return [self.targets, timestamp, valuefinal]

        else:
            # split each item in list and get values
            for i in self.targets:
                splitr = re.split(":", i)

                # clean whitespaces
                for s in range(0, len(splitr)):
                    splitr[s] = splitr[s].strip()
                    # print(splitr[s])

                # refer above for explanation

                valueinst = self.getgfinancequote(splitr[0], splitr[1])

                # error handling
                if valueinst == 'Fatal error, please verify targets assigned':
                    return valueinst + 'Error in ticker ' + str(i)

                valuefinal.append(valueinst)

            # use the method to update the df for the values scraped in this instance of the function

            self.df = self.add_values_toFrame_handler(self.targets, timestamp, valuefinal)

            return [self.targets, timestamp, valuefinal]

    def add_row_single(self, target: str, date, values: list):

        # prepare a new dataframe for the values to be added, with a multilevel index, and add it to the existing
        # dataframe using concat
        new_df_index = pd.MultiIndex.from_tuples([(target, date)], names=['Targets', 'Dates'])
        new_df = pd.DataFrame(data=values, columns=self.df.columns, index=new_df_index)
        new_df = pd.concat([self.df, new_df])

        # since concat adds the new index at the bottom, the df is sorted first based on dates then based on
        # the ticker names

        new_df = new_df.sort_index(level='Dates', sort_remaining=False)

        new_df.sort_index(inplace=True)

        return new_df

    def add_values_toFrame_handler(self, target: str | list, date, values: list):
        if self.df is None:
            return None
        else:
            if isinstance(target, str):
                return self.add_row_single(target, date, values)
            else:
                # since only one date value will be provided by the quotegetter method, the a list comprehension and
                # zip call is used to prepare a list to be used for creating a multiindex dataframe that for the new
                # rows

                date_listing_forl2_index = [date for x in range(len(target))]
                new_df_index = list(zip(target, date_listing_forl2_index))
                new_df_index = pd.MultiIndex.from_tuples(new_df_index, names=['Targets', 'Dates'])
                new_df = pd.DataFrame(values, columns=self.df.columns, index=new_df_index)
                new_df = pd.concat([self.df, new_df], ignore_index=False)

                # since concat adds the new index at the bottom, the df is sorted first based on dates then based on
                # the ticker names

                new_df = new_df.sort_index(level='Dates', sort_remaining=False)

                new_df.sort_index(inplace=True)

                return new_df

    def filewriter(self, path="scrapeddata_template.csv"):
        # write the df to the file
        self.df.to_csv(path)

    # methods called by main methods, do not modify unless you know what you are doing
    def identifytargets(self):

        # identify and extract the target stock tickers
        # Getting the list of stocks, and getting values
        import re
        collist = list(self.df.index.get_level_values('Targets').unique().tolist())
        targetlist = []
        for potent in collist:
            if re.search(":", potent):
                targetlist.append(potent)

        # self.targets = targetlist
        return targetlist

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

        # portion of code to find the closing value
        targetvalue_closing = googlesoup.find('div', attrs={'class': 'YMlKec fxKbKc'}).text

        # get the numbers and convert to number value
        targetvalue_closing = self.convert_gfinance_text_to_num(targetvalue_closing)

        # the gfinance website has a section where the opening, high, low values are placed. These values are stored
        # in divs with class names the same. So all of these are extracted with the fina all method, and the first
        # two sections are used for the required values

        targetvalue_all = googlesoup.find_all('div', attrs={'class': 'P6K39c'})

        for count, div_values in enumerate(targetvalue_all):

            # there are strip methods applied here, inspite of the fact that the cleaning methods also apply them.
            # This is because the text sometimes has extra spaces that the split in the beginning of the those
            # methods don't catch, leading to errors.

            if count == 0:
                # the first div contains the previous close, which is the current open. Only this value is present.
                targetvalue_opening = self.convert_gfinance_text_to_num(div_values.get_text().strip())
            elif count == 1:
                # The 2nd section contains the high and low values in the following format - highxx-lowxxx. So,
                # the text is split into two, and each of them are cleaned seperately
                high_low_values_raw = re.split('-', div_values.get_text())
                targetvalue_low = self.convert_gfinance_text_to_num(high_low_values_raw[0].strip())
                targetvalue_high = self.convert_gfinance_text_to_num(high_low_values_raw[1].strip())
                break

        return [targetvalue_opening, targetvalue_high, targetvalue_low, targetvalue_closing]

    def convert_gfinance_text_to_num(self, targetvalues):
        import re

        # goldspot has been kept as 3, based on prior experience
        goldspot = 3

        # since text scraped from Google finance is not directly able to be converted to int with int(),
        # this function splits the number into each character, and tries to convert it into int. if it works,
        # the loop is broken and the index of that value is passed to the following code

        splittxt = re.split('', targetvalues.strip())
        for count, suspects in enumerate(splittxt):
            try:
                int(suspects)
            except:
                continue
            else:
                # only if the piece of code in try is run successfully is this part of code run
                goldspot = count - 1
                break

        # the index value received from the loop is used to initiate a slice, the sliced value is trimmed for any
        # whitespace in the end of the value, and sent to a function that converts the value with the commas using
        # the locale module(i.e to translate Indian and International numbering systems)

        targetvalues = targetvalues[goldspot:]
        targetvalues = targetvalues.strip()
        targetvalues = self.cleanstrtonum(targetvalues)
        return targetvalues

    def cleanstrtonum(self, value):
        import locale
        locale.setlocale(locale.LC_ALL, '')
        returnval = locale.atof(value)
        return returnval

    def movementindex(self):

        # method to generate a series with differences between the last (n) and (n-1) row for each column

        dataframe_for_calculation = self.df.iloc[[-2, -1]]

        return dataframe_for_calculation[
            [columns for columns in dataframe_for_calculation.columns if columns != 'Dates']].iloc[1] - \
            dataframe_for_calculation[
                [columns for columns in dataframe_for_calculation.columns if columns != 'Dates']].iloc[0]

    def candlesticks(self, target):
        import mplfinance as mpf
        df_for_candlestick = self.df.loc[target]
        df_for_candlestick = df_for_candlestick.reset_index(drop=False)

        df_for_candlestick['Dates'] = pd.to_datetime(df_for_candlestick['Dates'])
        df_for_candlestick.set_index('Dates', inplace=True)

        # Create the candlestick chart
        mpf.plot(df_for_candlestick, type='candle', title='Stock Price', ylabel='Price')

"""
import time
start_time = time.perf_counter()
handler = StockScraper()
handler.filedata()
handler.quotegetter()
handler.filewriter()
end_time = time.perf_counter()
print(end_time - start_time, "seconds")
"""