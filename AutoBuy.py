import csv
import sys
import os
import time
from os import path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


nstoppos = -1
#desturl = "https://catalog.usmint.gov"
desturl = "https://catalog.usmint.gov/account-login"

dir_path = os.path.dirname(os.path.realpath(__file__))


# read csv file

csvpath = dir_path + "\\UsMintBotSheet.csv"
with open(csvpath) as f:
    reader = csv.reader(f)
    userdata = [r for r in reader]
    userdata.pop(0)  # remove header

# start scrapping
browser = webdriver.Chrome(dir_path + '/chromedriver')

#uname = "3f@pinehurstcoins.com"
#upass = "Red1899w="
#uitem = "19EG"
#ucode = "486"


# here while

for udata in userdata:

    uname = udata[0]
    upass = udata[1]
    uitem = udata[2]
    ucode = udata[3]

    # log out
    try:
        browser.find_element_by_xpath(
            '''//*[@id="header"]/div[3]/div[2]/ul/li[1]/a''').click()
    except NoSuchElementException:
        print("can not log out\n")

    try:
        browser.find_element_by_xpath(
            '''//*[@id="primary"]/div[1]/span/a''').click()
    except:
        print("can not log out\n")

    try:
        # browser.find_element_by_link_text("https://catalog.usmint.gov/account-login").click()
        # browser.find_element_by_xpath('''//*[@id="header"]/div[3]/div[2]/ul/li[1]/a''').click()
        browser.get(desturl)
        time.sleep(2)

        browser.find_element_by_id("dwfrm_login_username").send_keys(uname)
        browser.find_element_by_id("dwfrm_login_password").send_keys(upass)

        browser.find_element_by_id("login").click()
        time.sleep(5)

        browser.find_element_by_id("q").send_keys(uitem)
        browser.find_element_by_id("q").send_keys(Keys.ENTER)
        time.sleep(1)

        butform = browser.find_element_by_id(
            "pdp-rc-1").find_element_by_tag_name("form")
        strpattern = butform.get_attribute("id")
        butxpath = '''//*[@id="''' + strpattern + \
            '''''''"]/div/div[5]/button[1]'''
        time.sleep(1)

        butshop = browser.find_element_by_xpath(butxpath)
        butshop.click()
        time.sleep(2)

        # browser.find_element_by_xpath('''//*[@id="mini-cart"]/div[2]/a''').click()
        butshopgo = browser.find_element_by_xpath(
            '''//*[@id="mini-cart"]/div[3]/div[2]/div[3]/a''')
        butshopgo.click()
        time.sleep(2)

        # login check
        try:
            recheckloginbut = browser.find_element_by_id(
                "checkoutMethodLoginSubmit")
            browser.find_element_by_id("dwfrm_login_username").send_keys(uname)
            browser.find_element_by_id("dwfrm_login_password").send_keys(upass)

            browser.find_element_by_id("checkoutMethodLoginSubmit").click()
            time.sleep(1)

        except NoSuchElementException:
            print("aleady selected login field")

        # shipping
        try:
            recheckshippingbut = browser.find_element_by_id(
                "submitshippingbtn")
            Select(browser.find_element_by_id(
                "dwfrm_singleshipping_addressList")).select_by_index(1)
            # browser.find_element_by_id("submitshippingbtn").click()
            time.sleep(2)

        except:
            print("aleady selected shipping")

        # payment

        try:
            bclickpay = 0
            recheckshippingbut = browser.find_element_by_id(
                "checkoutContinuePaymentDelegator")
            try:
                browser.find_element_by_id(
                    "dwfrm_billing_paymentMethods_creditCardList")
                Select(browser.find_element_by_id(
                    "dwfrm_billing_paymentMethods_creditCardList")).select_by_index(1)
                time.sleep(2)
                browser.find_element_by_id(
                    "dwfrm_billing_paymentMethods_creditCard_cvn").send_keys(ucode)
                bclickpay = 1
            except NoSuchElementException:
                print("aleady selected credit card")

            try:
                browser.find_element_by_id("dwfrm_billing_addressList")
                Select(browser.find_element_by_id(
                    "dwfrm_billing_addressList")).select_by_index(1)
                bclickpay = 0
                time.sleep(5)
            except NoSuchElementException:
                print("aleady selected billing address")

        except NoSuchElementException:
            print("aleady selected payment method")

        try:
            recheckshippingbut = browser.find_element_by_id(
                "checkoutContinuePaymentDelegator")
            recheckshippingbut.click()
        except:
            print("aleady selected payment method")

        # order

        try:
            prderbut = browser.find_element_by_id("submitOrderButton")
            browser.find_element_by_id("formAgreementLabel").click()

            prderbut.click()
        except:
            print("aleady selected order method")

        time.sleep(10)

    except NoSuchElementException:
        print("can not acess URL")
