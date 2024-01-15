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
        self.driver = webdriver.Chrome()
        self.chart_data = [] #chart data for Task 1
        self.table_data = []
        self.domain = "https://dps.psx.com.pk/"
        self.path = "timeseries/eod/KSE100"
    
    def getHTMLContent(self):
        #Using selenium driver to load page and access dynamic content
        self.driver.get(self.domain) 
        dropdown_xpath = "/html[1]/body[1]/div[6]/div[9]/div[2]/div[3]/div[1]/div[1]/div[1]/div[1]/label[1]/select[1]"
        dropdown = self.driver.find_element(by=By.XPATH, value=dropdown_xpath)
        select = Select(dropdown)
        #apply filter to get all 361 table entries
        select.select_by_visible_text("All") 
        return self.driver.page_source 
    
    def parseContent(self, html_content):
        soup = BeautifulSoup(html_content, 'html5lib')
        # Locate the table within the page
        required_class = "tbl__wrapper tbl__wrapper--scrollable"
        tableParentDiv = soup.find('div', class_=required_class)
        table = tableParentDiv.find('table')
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
        required_url = self.domain + self.path
        response = requests.get(required_url)
        response = response.json() 
        self.chart_data = response['data']


class PSXAnalyzer:
    def __init__(self, Table_Data, Chart_Data):
        self.table_data = Table_Data
        self.chart_data = Chart_Data
        self.table_dataframe = None
        self.chart_dataframe = None
    
    def preprocessingTable(self):
        column_names = self.table_data[0]
        data = self.table_data[2:] 
        self.table_dataframe = pd.DataFrame(data, columns=column_names) #creating Pandas DataFrame object

        # Remove '%' sign from change column
        self.table_dataframe["CHANGE (%)"] = self.table_dataframe["CHANGE (%)"].str.rstrip('%').astype('float')
        return self.table_dataframe
    
    def topTenChange(self):
        top_ten_indices = self.table_dataframe['CHANGE (%)'].nlargest(10).index
        top_ten_change = self.table_dataframe.loc[top_ten_indices, ['SYMBOL', 'CHANGE (%)']]

        print("Top 10 symbols with most change today:\n", top_ten_change)
    
    def preprocessingChart(self):
        self.chart_data = [column[:2] for column in self.chart_data] #using timestamp and index value columns for df
        columns = ['TIMESTAMP', 'INDEX VALUE']
        self.chart_dataframe = pd.DataFrame(self.chart_data, columns=columns)
        #converting from Unix timestamp to datetime objects
        self.chart_dataframe['TIMESTAMP'] = self.chart_dataframe['TIMESTAMP'].apply(lambda x:datetime.utcfromtimestamp(x))
        self.chart_dataframe = self.chart_dataframe.loc[self.chart_dataframe['TIMESTAMP']>='2023-12-15 00:00:00']
        return self.chart_dataframe
    
    def maxValue(self):
        max_value_index = self.chart_dataframe['INDEX VALUE'].idxmax()
        print("Highest index for last month:\n", self.chart_dataframe.loc[max_value_index, ['TIMESTAMP','INDEX VALUE']])


psx_scraper = PSXScraper()
html_content = psx_scraper.getHTMLContent()
psx_scraper.parseContent(html_content)
psx_scraper.getChart()  

psx_analyzer = PSXAnalyzer(psx_scraper.table_data, psx_scraper.chart_data)

table_DF = psx_analyzer.preprocessingTable()
chart_DF = psx_analyzer.preprocessingChart()

psx_analyzer.topTenChange()
psx_analyzer.maxValue()


   
    
    
    
    

    