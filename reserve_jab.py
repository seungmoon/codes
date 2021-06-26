# -*- coding: utf-8 -*-
"""
News Scrap coding for Nexis
Excel file datascrap with dates in 'date' sheet
and chromedriver.exe file is needed in the same directory
"""
import winsound
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
#import numpy as np
import time, datetime, xlrd, xlwt

class ReserveJab:

    def __init__(self, urlAddress):
        self.urlAddress = urlAddress



    def RenewUntilClick(self):

            driver = webdriver.Chrome()
            driver.get(self.urlAddress)

            duration = 200  # milliseconds
            freq = 2500  # Hz

            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((By.LINK_TEXT, '목록보기')))
            enter = driver.find_element(By.LINK_TEXT, '목록보기')
            enter.click()
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((By.LINK_TEXT, '잔여백신 보유 병원')))
            time.sleep(2)

            for i in range(5000):
                enter2 = driver.find_element(By.LINK_TEXT, '잔여백신 보유 병원')
                enter2.click()
                time.sleep(3)

                if expected_conditions.element_to_be_clickable((By.PARTIAL_LINK_TEXT, '현재 접종가능한 백신이 없습니다')):
                    #print('reservation not available')
                    enterRenew = driver.find_element(By.LINK_TEXT, '새로고침')
                    enterRenew.click()
                    #winsound.Beep(freq, duration)
                    time.sleep(2)

                else:
                    print('available')
                    enterReserve = driver.find_element(By.LINK_TEXT, '접종 예약신청')
                    enterReserve.click()
                    winsound.Beep(freq, duration)
                    winsound.Beep(freq, duration)
                    winsound.Beep(freq, duration)
                    winsound.Beep(freq, duration)
                    winsound.Beep(freq, duration)
                    time.sleep(300)



    def Procedure(self):
        start = time.perf_counter()
        result = self.RenewUntilClick()

        end = time.process_time()
        print( 'time elapsed:   ', end - start )
        #printresult

        return result


###############################################################################

if __name__ == '__main__':
    urlAddress1 = 'https://m.place.naver.com/rest/vaccine?vaccineFilter=used'


    EX1input = {'urlAddress': urlAddress1}

    EX1 = ReserveJab(**EX1input)
    EX1result = EX1.Procedure()
    #EX1check = EX1.EnterQueryCheck()
