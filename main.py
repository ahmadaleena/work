from selenium import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

from bs4 import BeautifulSoup

def ProcessTable(table, table_data):
    #given any HTML table, will loop over rows to get content 
        
    #accessing table header to get column names
    header_list = [] #will contain content of each cell in header
    table_header = table.find_all('th')
    for cell in table_header:
        header_list.append(cell.text)
    table_data.append(header_list)

    #accessing table body to get row content
    table_rows = table.find_all('tr')
    for row in table_rows: 
        trow_list = []  
        trow_cells = row.find_all('td')
        for cell in trow_cells:
            trow_list.append(cell.text)
        table_data.append(trow_list)

#Getting content from url
url = "https://dps.psx.com.pk/"
driver = webdriver.Chrome()
driver.get(url)

html_content = driver.page_source #HTML including dynamic content after js execution

# Parsing HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html5lib')

# Locate the table within the page
required_class = "tbl__wrapper tbl__wrapper--scrollable"
tableParentDiv = soup.find('div', class_=required_class)
table = tableParentDiv.find('table')

# Check if the table is found
if table:
    table_data = []
    ProcessTable(table, table_data)
else:
    print("No table found")

#ANALYSIS
column_names = table_data[0]
data = table_data[2:]
df = pd.DataFrame(data, columns=column_names) #creating Pandas DataFrame object

# Remove '%' sign to process column
df["CHANGE (%)"] = df["CHANGE (%)"].str.rstrip('%').astype('float')

top_ten_indices = df['CHANGE (%)'].nlargest(10).index

top_ten_change = df.loc[top_ten_indices, ['SYMBOL', 'CHANGE (%)']]

print("Top 10 symbols with most change today: ", top_ten_change)

# Close the WebDriver
driver.quit()

