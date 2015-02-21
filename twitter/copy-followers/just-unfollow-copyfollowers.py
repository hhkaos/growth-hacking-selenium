# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class JustUnfollowCopyfollowers(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.justunfollow.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        
        self.justunfollow_user = "your_user"
        self.justunfollow_pass = "your_pass"

        # Twitter accounts with the same profile of followers
        self.common = [
            'hhkaos', 
            'geo_developers', 
            'actitudstartup'
        ]
        self.max_followers = 10
    
    def test_just_unfollow_copyfollowers(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        driver.find_element_by_id("username_or_email").clear()
        driver.find_element_by_id("username_or_email").send_keys(self.justunfollow_user)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(self.justunfollow_pass)
        driver.find_element_by_id("allow").click()
        driver.find_element_by_link_text("Copy Followers (Grow)").click()
        
        for c in self.common:
            driver.find_element_by_css_selector("input.span3.jq-username").clear()
            driver.find_element_by_css_selector("input.span3.jq-username").send_keys(c)
            driver.find_element_by_css_selector("form.well.form-search > button.btn").click()
            for x in range(0, self.max_followers):
                driver.find_element_by_css_selector("img.btnfollow").click()
                time.sleep(2)
            

    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
