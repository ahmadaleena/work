from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

#PSX Scraper Class: get HTML content from webpage using requests and Selenium, parse using BeautifulSoup
class PSXScraper:
    def __init__(self):
        # self.driver = webdriver.Chrome()
        self.chart_data = [] #chart data for Task 1
        self.table_data = []
        self.domain = "https://dps.psx.com.pk/"
        self.path_chart = "timeseries/eod/KSE100"
        self.path_table = "market-watch"
        self.table_html = ""
    
    def getHTMLContent(self):
        s = requests.Session()
        table_url = self.domain + self.path_table
        response = s.get(table_url)
        self.table_html = response.text 
        
        chart_url = self.domain +  self.path_chart
        response = s.get(chart_url)
        response = response.json()
        self.chart_data = response['data']
    
    def parseContent(self):
        soup = BeautifulSoup(self.table_html, 'html5lib')
        table = soup.find('table')
        if table:
            self.processTable(table)
        else:
            print("No table found")
    
    def processTable(self, HTMLtable):
        #accessing table header to get column names
        header_list = [] #list for the content of each cell in header
        table_header = HTMLtable.find_all('th')
        for cell in table_header:
            header_list.append(cell.text)
        header_list.insert(1,'DEFAULTED') 
        self.table_data.append(header_list)

        #accessing table body to get row content
        table_rows = HTMLtable.find_all('tr')
        for row in table_rows: 
            trow_list = []  
            trow_cells = row.find_all('td')
            for index, cell in enumerate(trow_cells):
                trow_list.append(cell.text)
                if index==0:
                    self.checkDefaulted(cell, trow_list)
            self.table_data.append(trow_list)
    
    def checkDefaulted(self,cell, row_list):
        if(cell.find('div') is not None):
            row_list.append('YES')
        else:
            row_list.append('NO')
    
    def getChart(self):
        required_url = self.domain + self.path1
        response = requests.get(required_url)
        response = response.json() 
        self.chart_data = response['data']


class PSXAnalyzer:
    def __init__(self, Table_Data, Chart_Data):
        self.table_data = Table_Data
        self.chart_data = Chart_Data
        self.table_dataframe = None
        self.chart_dataframe = None
        self.change_percent = "CHANGE (%)"
        self.symbol = "SYMBOL"
        self.time = "TIMESTAMP"
        self.idx_val = "INDEX VALUE"
    
    def preprocessingTable(self):
        column_names = self.table_data[0]
        data = self.table_data[2:] 
        self.table_dataframe = pd.DataFrame(data, columns=column_names) #creating Pandas DataFrame object

        # Remove '%' sign from change column
        self.table_dataframe[self.change_percent] = self.table_dataframe[self.change_percent].str.rstrip('%').astype('float')
        return self.table_dataframe
    
    def topTenChange(self):
        top_ten_indices = self.table_dataframe[self.change_percent].nlargest(10).index
        if top_ten_indices.empty:
            raise NotImplementedError
        else:
            top_ten_change = self.table_dataframe.loc[top_ten_indices, [self.symbol, self.change_percent]]


        print("Top 10 symbols with most change today:\n", top_ten_change)
    
    def preprocessingChart(self):
        self.chart_data = [column[:2] for column in self.chart_data] #using timestamp and index value columns for df
        columns = [self.time, self.idx_val]
        self.chart_dataframe = pd.DataFrame(self.chart_data, columns=columns)
        #converting from Unix timestamp to datetime objects
        self.chart_dataframe[self.time] = self.chart_dataframe[self.time].apply(lambda x:datetime.utcfromtimestamp(x))
        self.chart_dataframe = self.chart_dataframe.loc[self.chart_dataframe[self.time]>='2023-12-15 00:00:00']
        return self.chart_dataframe
    
    def maxValue(self):
        max_value_index = self.chart_dataframe[self.idx_val].idxmax()
        if max_value_index is None:
            raise NotImplementedError
        else:
            print("Highest index for last month:\n", self.chart_dataframe.loc[max_value_index, [self.time,self.idx_val]])


psx_scraper = PSXScraper()
psx_scraper.getHTMLContent()
psx_scraper.parseContent()
# psx_scraper.getChart()  

psx_analyzer = PSXAnalyzer(psx_scraper.table_data, psx_scraper.chart_data)

table_DF = psx_analyzer.preprocessingTable()
chart_DF = psx_analyzer.preprocessingChart()

psx_analyzer.topTenChange()
psx_analyzer.maxValue()


   
    
    
    
    

    