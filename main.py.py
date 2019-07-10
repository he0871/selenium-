"""
ENTS669G's Homework 3
Data mining
2018/7/28
Aurthor: Jingyuan He
"""
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import csv
import numpy as np
import statis #custom lib
from scipy.spatial.distance import pdist


def get_historical_data():
    HisData_present = EC.element_to_be_clickable((By.LINK_TEXT, "Historical Data"))
    WebDriverWait(driver,20).until(HisData_present)
    #wait one more second to guarantee that button is clickable
    time.sleep(1)
    HisData = driver.find_element_by_link_text("Historical Data")
    HisData.click()
    download_present = EC.element_to_be_clickable((By.LINK_TEXT, "Download Data"))
    WebDriverWait(driver,20).until(download_present)
    #wait one more second to guarantee that button is clickable
    time.sleep(2)
    Download = driver.find_element_by_link_text("Download Data")
    Download.click()


    
    
    
"""
main
"""    


stocks_list = ['INTC','MSFT', 'CSCO', 'AAPL', 'AMZN', 'GOOG', 'JNPR', 'VZ', 'T', 'S', 'TMUS']

driver = webdriver.Chrome()
driver.get("http://www.finance.yahoo.com")
#download all the files
for stock in stocks_list:
    search_box = driver.find_element_by_name('p') #get the search box
    search_box.send_keys(stock)
    time.sleep(1) #wait for send keys
    search_box.send_keys(Keys.RETURN)
    get_historical_data()
    time.sleep(1) #wait to guarantee visiting web page in order

time.sleep(2) #sleep for a while to wait the download process finish

#read csv file
all_stocks = []
for stock in stocks_list:
    temp = []
    file_path = 'C:/Users/jingy/Downloads/' + stock + '.csv'
    with open(file_path) as csv_file:
        next(csv_file)
        table = csv.reader(csv_file)
        for row in table:
            #print(row)
            temp.append(row[4])
    all_stocks.append(temp)	
stocks_matrix = np.array(all_stocks,dtype='f')
#print(stocks_matrix)
nmatrix = statis.normalize(stocks_matrix)
Euclidean = pdist(nmatrix)
MaxIndex = np.unravel_index(np.argmax(Euclidean, axis=None), Euclidean.shape)[0]  #int works much better than tuple
MinIndex = np.unravel_index(np.argmin(Euclidean, axis=None), Euclidean.shape)[0] 
MaxDistant = statis.located(MaxIndex,len(nmatrix))
MinDistant = statis.located(MinIndex,len(nmatrix))
print("base on Euclidean distance (index start with 1)")
print("the longest distant is between" + str(MaxDistant))
statis.TendCmpPlot(nmatrix[MaxDistant[0]-1],nmatrix[MaxDistant[1]-1],'least similar')
print("the shortest distant is between" + str(MinDistant))
statis.TendCmpPlot(nmatrix[MinDistant[0]-1],nmatrix[MinDistant[1]-1],'most similar')

cov_matrix = np.cov(nmatrix)
corrcoef_matrix = np.corrcoef(nmatrix)
n = 0
while n < len(cov_matrix):
    cov_matrix[n][n] = 0
    corrcoef_matrix[n][n] = 0
    n += 1

print("according to cov (index start with 0)")
MaxIndex = np.unravel_index(np.argmax(cov_matrix, axis=None), cov_matrix.shape) 
print("the most similar stocks by cov are " + str(MaxIndex))
MinIndex = np.unravel_index(np.argmin(cov_matrix, axis=None), cov_matrix.shape) 
print("the least similar stocks by cov are " + str(MinIndex))

statis.TendCmpPlot(nmatrix[MaxIndex[0]],nmatrix[MaxIndex[1]],'max cov')
statis.TendCmpPlot(nmatrix[MinIndex[0]],nmatrix[MinIndex[1]],'min cov')

print("according to corrcoef (index start with 0)")
MaxIndex = np.unravel_index(np.argmax(corrcoef_matrix, axis=None), corrcoef_matrix.shape) 
print("the most similar stocks by corrcoef  are " + str(MaxIndex))
MinIndex = np.unravel_index(np.argmin(corrcoef_matrix, axis=None), corrcoef_matrix.shape) 
print("the least similar stocks by corrcoef  are " + str(MinIndex))

statis.TendCmpPlot(nmatrix[MaxIndex[0]],nmatrix[MaxIndex[1]],'max corr')
statis.TendCmpPlot(nmatrix[MinIndex[0]],nmatrix[MinIndex[1]],'min corr')
#regression
mb = statis.linear_re(np.arange(1,len(stocks_matrix[0])+1,1),stocks_matrix)

#plot, figures will be saved in disk rather than manifest
statis.RegressionPlot(mb, stocks_matrix)

#predict
result = statis.predict(mb[0][0],mb[1][0],22,47.69)
print(result)

