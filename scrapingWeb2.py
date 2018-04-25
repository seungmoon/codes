# -*- coding: utf-8 -*-
"""
News Scrap coding for Nexis

Excel file datascrap with dates in 'date' sheet
and chromedriver.exe file is needed in the same directory
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
import time, datetime, xlrd, xlwt



class ScrapeData:
    
   def __init__(self, urlAddress, search_terms, selected_source, xlsForDates):
       self.urlAddress = urlAddress
       self.search_terms = search_terms
       self.selected_source = selected_source
       self.xlsForDates = xlsForDates
       
    
   def EnterQueryWrite(self):
       # prepare xl file
       writebook = xlwt.Workbook()
       writesheet = writebook.add_sheet("result")
       
       # start
       driver = webdriver.Chrome()
       driver.get(self.urlAddress)
       enter = driver.find_element_by_xpath('//*[@title="I accept the Terms & Conditions"]')
       enter.click()
    
       # agree terms   
       elem1 = driver.find_element_by_name("searchTerms1")
       elem1.clear()
       elem1.send_keys(self.search_terms)
       
       # initailize data   
       fromDate = []
       toDate = []
       data1 = []
       data2 = []
       
       # setting workbook for dates
       workbook = xlrd.open_workbook(self.xlsForDates)
       sheet = workbook.sheet_by_name('date')
       row_num = sheet.nrows    
    
       # date conversion to string dd/mm/yyyy
       fromDate_tmpval = sheet.cell_value(0,0)
       toDate_tmpval = sheet.cell_value(0,1)
       
       fromDate_y,fromDate_m,fromDate_d,t1,t2,t3 = xlrd.xldate_as_tuple(fromDate_tmpval, workbook.datemode)
       fromDate_tmp = str(fromDate_d)+'/'+str(fromDate_m)+'/'+str(fromDate_y)
       toDate_y,toDate_m,toDate_d,t1,t2,t3 = xlrd.xldate_as_tuple(toDate_tmpval, workbook.datemode)
       toDate_tmp = str(toDate_d)+'/'+str(toDate_m)+'/'+str(toDate_y)
       
       #print [fromDate_tmp, toDate_tmp]
       # select dates
       myselect1 = Select(driver.find_element_by_name("dateSelector"))
       my1 = myselect1.select_by_visible_text("Custom date")
       WebDriverWait(driver,5).until(expected_conditions.presence_of_element_located((By.NAME, "fromDate")))
    
       elem2 = driver.find_element_by_name("fromDate")
       elem2.clear()
       elem2.send_keys(fromDate_tmp)
    
       elem3 = driver.find_element_by_name("toDate")
       elem3.clear()
       elem3.send_keys(toDate_tmp)
       
       # select source 
       myselect2 = Select(driver.find_element_by_name("sourceList"))
       my2 = myselect2.select_by_visible_text(self.selected_source)

       # click search
       enter3 = driver.find_element_by_xpath("//*[@id='enableSearchImg']")
       enter3.click()
       
       # get number of reports
       data1_tmpt = driver.find_element_by_id("updateCountDiv").text
       data1_tmp = int(data1_tmpt[data1_tmpt.find("(")+1:data1_tmpt.find(")")])
       
       WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.NAME, "Publication")))
              
       enter4 = driver.find_element_by_name("Publication")
       enter4.click()
              
       WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//a[@class='multiple' and @id='multiple_1']/span")))
       
       if expected_conditions.visibility_of_element_located((By.XPATH, "//a[@href='javascript:showMoreOptions();' and @id='more1']/span"))   :
              #time.sleep(2)
           #WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//a[@href='javascript:showMoreOptions();' and @id='more1']/span")))
       
          enter5 = driver.find_element_by_xpath("//a[@href='javascript:showMoreOptions();' and @id='more1']/span")
          enter5.click()
       
          WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Fewer")))
              # get number of papers
          data2_tmp = len(driver.find_elements_by_xpath("//*/li[@id='0_1']/ul/li"))-2
           
       else:
               
              # get number of papers
          data2_tmp = len(driver.find_elements_by_xpath("//*/li[@id='0_1']/ul/li"))-2
       
       
       fromDate.append(fromDate_tmp)
       toDate.append(toDate_tmp)
       data1.append(data1_tmp)
       data2.append(data2_tmp)
       print fromDate[0], toDate[0], data1[0], data2[0]
       
       for xlcol in range(4):
                          
               if xlcol==0:
                   writesheet.write(1,xlcol,fromDate[0])
               elif xlcol==1:
                   writesheet.write(1,xlcol,toDate[0])
               elif xlcol==2:
                   writesheet.write(1,xlcol,data1[0])
               else:
                   writesheet.write(1,xlcol,data2[0])
       
       # click edit
       enter6 = driver.find_element_by_link_text("Edit")
       enter6.click()
       
       
       row = 1
       while row < row_num:
           
           print row, row_num
       
           
           # wait unter new page loaded
           WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.ID, "fromDate")))
           
           # date conversion to string dd/mm/yyyy
           fromDate_tmpval = sheet.cell_value(row, 0)
           toDate_tmpval = sheet.cell_value(row, 1)
       
           fromDate_y,fromDate_m,fromDate_d,t1,t2,t3 = xlrd.xldate_as_tuple(fromDate_tmpval, workbook.datemode)
           fromDate_tmp = str(fromDate_d)+'/'+str(fromDate_m)+'/'+str(fromDate_y)
           toDate_y,toDate_m,toDate_d,t1,t2,t3 = xlrd.xldate_as_tuple(toDate_tmpval, workbook.datemode)
           toDate_tmp = str(toDate_d)+'/'+str(toDate_m)+'/'+str(toDate_y)
           
           # input new dates           
           elem2 = driver.find_element_by_name("fromDate")
           elem2.clear()
           elem2.send_keys(fromDate_tmp)
    
           elem3 = driver.find_element_by_name("toDate")
           elem3.clear()
           elem3.send_keys(toDate_tmp)
           
           #window_before = driver.window_handles[0]
           #print window_before
           # click search
           enter3 = driver.find_element_by_xpath("//*[@id='enableSearchImg']")
           enter3.click()
           #time.sleep(1)
           
           # in case of more than 3000 results
           try:
               cond3000 = driver.find_element_by_xpath("//img[@title='Over 3000 Results']")
               
               #WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.XPATH, "//a[@href='javascript:hidePopWin(true);']/img[@title='Edit Search' and @alt='Edit Search']")))
               
               data1_tmpt = 3000
               data2_tmp = 3000
               
               time.sleep(5)
               #WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.ID, "popupContainer")))
               #WebDriverWait(driver, 30).until(expected_conditions.alert_is_present())
               #driver.switch_to_alert().dismiss()
               #window_after = driver.current_window_handle
               #print window_after
               #driver.switch_to.window(window_after)
               #driver.switch_to_active_element()
               #WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@title='Edit Search' and @alt='Edit Search']")))
               #enter3_1 = driver.find_element_by_xpath("//*[@title='Edit Search']")
               #enter3_1.click()
               row = row_num
               
                   
           except NoSuchElementException:
               WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.ID, "updateCountDiv")))
                  
               
           
            # gather data
           # get number of reports    
               data1_tmpt = driver.find_element_by_id("updateCountDiv").text
               data1_tmp = int(data1_tmpt[data1_tmpt.find("(")+1:data1_tmpt.find(")")])
       
           #time.sleep(2)
               WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//a[@class='multiple' and @id='multiple_1']/span")))
               
           #enter4 = driver.find_element_by_name("Publication")
           #enter4.click()
               try:
                  cond2 = driver.find_element_by_xpath( "//a[@href='javascript:showMoreOptions();' and @id='more1']/span")   
                  time.sleep(1)
           #WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//a[@href='javascript:showMoreOptions();' and @id='more1']/span")))
       
                  enter5 = driver.find_element_by_xpath("//a[@href='javascript:showMoreOptions();' and @id='more1']/span")
                  enter5.click()
       
                  WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Fewer")))
              # get number of papers
                  data2_tmp = len(driver.find_elements_by_xpath("//*/li[@id='0_1']/ul/li"))-2
           
               except NoSuchElementException:
               
              # get number of papers
                  data2_tmp = len(driver.find_elements_by_xpath("//*/li[@id='0_1']/ul/li"))-2
              
                  # click edit
               enter6 = driver.find_element_by_link_text("Edit")
               enter6.click()
       
           fromDate.append(fromDate_tmp)
           toDate.append(toDate_tmp)
           data1.append(data1_tmp)
           data2.append(data2_tmp)
           
           print fromDate[-1], toDate[-1], data1[-1], data2[-1]
           
           row +=1
           
           #writing on excel
           for xlcol in range(4):
                          
                 if xlcol==0:
                   writesheet.write(row+1,xlcol,fromDate[-1])
                 elif xlcol==1:
                   writesheet.write(row+1,xlcol,toDate[-1])
                 elif xlcol==2:
                   writesheet.write(row+1,xlcol,data1[-1])
                 else:
                   writesheet.write(row+1,xlcol,data2[-1])
       
       writebook.save('DatascrapResult0.xls')         
              
       return {'fromDate':fromDate, 'toDate':toDate, 'data1':data1, 'data2':data2}
   
   
   
   def WriteCsv(self, result):
       
       writebook = xlwt.Workbook()
       writesheet = writebook.add_sheet("result")
       
       for xlcol in range(4):
           for xlrow in range(len(result['fromDate'])):
               
               if xlcol==0:
                   writesheet.write(xlrow,xlcol,result['fromDate'][xlrow])
               elif xlcol==1:
                   writesheet.write(xlrow,xlcol,result['toDate'][xlrow])
               elif xlcol==2:
                   writesheet.write(xlrow,xlcol,result['data1'][xlrow])
               else:
                   writesheet.write(xlrow,xlcol,result['data2'][xlrow])
               
       writebook.save('DatascrapResult0.xls')         

   def Procedure(self):    
       start = time.clock()
       result = self.EnterQueryWrite()
       end = time.clock()
       print 'time elapsed:   ', end-start
       print result
       
       return result
   
###############################################################################

if __name__ == '__main__':
    
   
   urlAddress1 = "https://www.nexis.com/search/flap.do?flapID=news&random=0.4917396798757647" 
   search_terms = 'S&P 500'
   selected_source = 'US Newspapers and Wires'
   xlsfile = 'datascrap.xlsx'
         
   EX1input = {'urlAddress': urlAddress1, 'search_terms': search_terms, 'selected_source': selected_source,
               'xlsForDates': xlsfile}
   
   EX1 = ScrapeData(**EX1input)
   EX1result = EX1.Procedure()
   #EX1.WriteCsv(EX1result['fromDate'],EX1result['toDate'],EX1result['data1'],EX1result['data2'])
   #EX1.WriteCsv(EX1result)