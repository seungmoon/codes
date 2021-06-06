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
#import numpy as np
import time, datetime, xlrd, xlwt

class ScrapeData:

    def __init__(self, urlAddress, year, month, xlsForDates):
        self.urlAddress = urlAddress
        self.year = year
        self.month = month
        self.xlsForDates = xlsForDates


    def EnterQueryWrite(self):
        # prepare xl file
        writebook = xlwt.Workbook()
        writesheet = writebook.add_sheet("result")


        # setting workbook for dates
        workbook = xlrd.open_workbook(self.xlsForDates)
        sheet = workbook.sheet_by_name('date')
        row_num = sheet.nrows
        for i_date in range(0, row_num):  #check dates
            year_tmpval = sheet.cell_value(i_date, 0)
            month_tmpval = sheet.cell_value(i_date, 1)
            #print('year')
            #print(year_tmpval)
            #print('month')
            #print(month_tmpval)

            # start
            driver = webdriver.Chrome()
            driver.get(self.urlAddress)
            #enter = driver.find_element_by_xpath('//*[@title="I accept the Terms & Conditions"]')
            #enter.click()

            # check conditions
            elem1 = driver.find_element_by_name("BankAll") # 전체
            elem1.click()
            elem2 = driver.find_element_by_id("opt_1_3") # 일반신용대출
            elem2.click()
            elem3 = driver.find_element_by_id("all_show_2") # 대출금리
            elem3.click()

            #for i in range(self.years-1):
            #    for j in range(self.months-1):
            dropdown1 = Select(driver.find_element_by_id("year"))
            #dropdown1.select_by_index(0)
            dropdown1.select_by_value(year_tmpval)
            dropdown2 = Select(driver.find_element_by_id("month"))
            #dropdown2.select_by_index(0)
            dropdown2.select_by_value(month_tmpval)

            enter1 = driver.find_element_by_link_text("검색")
            enter1.click()
            #WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "SearchResult")))
            WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'resultList_ty02')))
            #WebDriverWait(driver, 10)
            #elem1.clear()
            #elem1.send_keys(self.search_terms)

            # get numbers
            #print(self.banknames)
            #

            table_id = driver.find_element_by_class_name('resultList_ty02')
            #table_id = driver.find_element_by_xpath("// *[ @ id = 'SearchResult']")
            #table_id = driver.find_element_by_xpath("// *[ @ id = 'Content']")
            tbody = table_id.find_element_by_tag_name("tbody")
            tr_list = tbody.find_elements_by_tag_name("tr")

            if i_date==0:
                for i_bank in range(2, len(tr_list)):
                    td_list = tr_list[i_bank].find_elements_by_tag_name("td")
                    names_tmp = td_list[0].text

                    # text_tmp.append(rates_tmp)
                    print(names_tmp)
                    writesheet.write(1, 2 + i_bank, names_tmp)

            for i_bank in range(2, len(tr_list)):
                td_list = tr_list[i_bank].find_elements_by_tag_name("td")
                for i_credit in range(2, 7):
                    rates_tmp = td_list[i_credit].text

                    #text_tmp.append(rates_tmp)
                    #print(rates_tmp)
                    if i_bank==2:
                        writesheet.write(5*i_date + i_credit, 0, year_tmpval)
                        writesheet.write(5*i_date + i_credit, 1, month_tmpval)
                        writesheet.write(5*i_date + i_credit, 2, i_credit-1)

                    writesheet.write(5*i_date + i_credit, 2 + i_bank, rates_tmp)
            #for i_row in range(2, len(tr_list)):
            #    text_tmp.append(tr_list[i_row].text)

            #print(tr_list[2].text)
            #print()
            #print(text_tmp)
            #print(text_tmp[0])
            #rates1=text_tmp[0]
            #print(rates1[0])


            # setting workbook for dates
            writebook.save('DatascrapResult0.xls')

    def EnterQueryCheck(self):
        # prepare xl file
        writebook = xlwt.Workbook()

        # setting workbook for dates
        year_tmpval = self.year
        month_tmpval = self.month
        print('year')
        print(year_tmpval)
        print('month')
        print(month_tmpval)

        # start
        driver = webdriver.Chrome()
        driver.get(self.urlAddress)
        #enter = driver.find_element_by_xpath('//*[@title="I accept the Terms & Conditions"]')
        #enter.click()

        # check conditions
        elem1 = driver.find_element_by_name("BankAll") # 전체
        elem1.click()
        elem2 = driver.find_element_by_id("opt_1_3") # 일반신용대출
        elem2.click()
        elem3 = driver.find_element_by_id("all_show_2") # 대출금리
        elem3.click()

        #for i in range(self.years-1):
        #    for j in range(self.months-1):
        dropdown1 = Select(driver.find_element_by_id("year"))
        #dropdown1.select_by_index(0)
        dropdown1.select_by_value(year_tmpval)
        dropdown2 = Select(driver.find_element_by_id("month"))
        #dropdown2.select_by_index(0)
        dropdown2.select_by_value(month_tmpval)

        enter1 = driver.find_element_by_link_text("검색")
        enter1.click()
        #WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "SearchResult")))
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'resultList_ty02')))
        #WebDriverWait(driver, 10)
        #elem1.clear()
        #elem1.send_keys(self.search_terms)

        # get numbers
        #print(self.banknames)
        #

        table_id = driver.find_element_by_class_name('resultList_ty02')
        #table_id = driver.find_element_by_xpath("// *[ @ id = 'SearchResult']")
        #table_id = driver.find_element_by_xpath("// *[ @ id = 'Content']")
        tbody = table_id.find_element_by_tag_name("tbody")
        tr_list = tbody.find_elements_by_tag_name("tr")
        text_tmp = []
        for i_bank in range(2, len(tr_list)):
            td_list = tr_list[i_bank].find_elements_by_tag_name("td")
            names_tmp = td_list[0].text

            # text_tmp.append(rates_tmp)
            print(names_tmp)

        for i_bank in range(2, len(tr_list)):
            td_list = tr_list[i_bank].find_elements_by_tag_name("td")
            for i_credit in range(2, 7):
                rates_tmp = td_list[i_credit].text

                #text_tmp.append(rates_tmp)
                print(rates_tmp)
        #for i_row in range(2, len(tr_list)):
        #    text_tmp.append(tr_list[i_row].text)

        #print(tr_list[2].text)
        #print()
        #print(text_tmp)
        #print(text_tmp[0])
        #rates1=text_tmp[0]
        #print(rates1[0])


        # setting workbook for dates



    def Procedure(self):
        start = time.perf_counter()
        result = self.EnterQueryWrite()

        end = time.process_time()
        print( 'time elapsed:   ', end - start )
        #printresult

        return result


###############################################################################

if __name__ == '__main__':
    urlAddress1 = 'https://portal.kfb.or.kr/compare/loan_household_new.php'
    year1 = '2017'
    month1 = '08'
    xlsfile = 'datascrap4.xls'


    EX1input = {'urlAddress': urlAddress1, 'year': year1, 'month': month1,
                'xlsForDates': xlsfile}

    EX1 = ScrapeData(**EX1input)
    EX1result = EX1.Procedure()
    #EX1check = EX1.EnterQueryCheck()
