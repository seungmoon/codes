# -*- coding: utf-8 -*-
"""
News Scrap coding for Nexis
Excel file datascrap with dates in 'date' sheet
and chromedriver.exe file is needed in the same directory
conda install selenium
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

    def __init__(self, urlAddress, naver_id, naver_pw):
        self.urlAddress = urlAddress
        self.naver_id = naver_id
        self.naver_pw = naver_pw



    def RenewUntilClick(self):

            driver = webdriver.Chrome()
            
            # login naver
            driver.get('http://www.naver.com')
            
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, 'link_login')))
            login_bt=driver.find_element_by_class_name('link_login')
            login_bt.click()

            naverid=driver.find_element_by_id('id')
            naverid.send_keys(self.naver_id)


            naverpw=driver.find_element_by_id('pw')
            naverpw.send_keys(self.naver_pw)

            naver_loginchk=driver.find_element_by_id('label_login_chk')
            naver_loginchk.click()
            naver_submit=driver.find_element_by_class_name('btn_global')
            naver_submit.click()
            time.sleep(3)
            id_captcha = 1

            while id_captcha == 1:
                try:
                    WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.ID, 'captcha')))

                    #WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.ID, 'pw')))
                    naverpw=driver.find_element_by_id('pw')
                    naverpw.send_keys(self.naver_pw)
                    
                            
                    time.sleep(15)
                    naver_submit=driver.find_element_by_class_name('btn_global')
                    naver_submit.click()
                    time.sleep(2)

                except:
                    id_captcha = 0
            
                
            #driver.get('http://www.naver.com')
            WebDriverWait(driver, 20).until(
                expected_conditions.presence_of_element_located((By.ID, 'query')))
            naverqr=driver.find_element_by_id('query')
            naverqr.send_keys("잔여백신예약")
            naver_submit=driver.find_element_by_class_name('ico_search_submit')
            naver_submit.click()
            
            
            WebDriverWait(driver, 20).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, 'vaccine_reserve')))
            enter_url = driver.find_element(By.CLASS_NAME, 'vaccine_reserve')
            enter_url.click()
            
            # reservation site
            #driver.get(self.urlAddress)

            duration = 200  # milliseconds
            freq = 2500  # Hz

            WebDriverWait(driver, 30).until(
                expected_conditions.presence_of_element_located((By.LINK_TEXT, '목록보기')))
            enter = driver.find_element(By.LINK_TEXT, '목록보기')
            enter.click()
            
            
            time.sleep(2)
            enterRenew = driver.find_element(By.LINK_TEXT, '새로고침')
            enterRenew.click()

            id_renew = 1
            while id_renew == 1:
                WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((By.LINK_TEXT, '잔여백신 보유 병원')))
                enter2 = driver.find_element(By.LINK_TEXT, '잔여백신 보유 병원')
                enter2.click()
                
                try:
                                
                    enterReserve = driver.find_element(By.LINK_TEXT, '접종 예약신청')
                    enterReserve.click()
                    certCheck = driver.find_element(By.LINK_TEXT, '네이버 인증서로 인증')
                    certCheck.click()
                    WebDriverWait(driver, 20).until(
                        expected_conditions.element_to_be_clickable((By.LINK_TEXT, '예약 신청')))
                    enterReserve1 = driver.find_element(By.LINK_TEXT, '예약 신청')
                    enterReserve1.click()

                    id_renew = 0


                except:
                    time.sleep(1)
                    enterRenew = driver.find_element(By.LINK_TEXT, '새로고침')
                    enterRenew.click()
                        
                    
            print('available')
            #enterReserve = driver.find_element(By.LINK_TEXT, '접종 예약신청')
            #enterReserve.click()
            for j in range(10):
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
    naverid1 = '네이버 아이디'
    naverpw1 = '네이버 패스워드'

    EX1input = {'urlAddress': urlAddress1, 'naver_id': naverid1, 'naver_pw': naverpw1}

    EX1 = ReserveJab(**EX1input)
    EX1result = EX1.Procedure()
    
