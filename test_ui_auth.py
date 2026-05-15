import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UniReviewsAuthTest(unittest.TestCase):
    def setUp(self):
        #initiliazes the chrome browser before each test
        self.driver = webdriver.Chrome
        self.driver.get("http://127.0.0.1:5000/")
        self. wait = WebDriverWait(self.driver, 10) #explicitly wait for dynamic elements

    def tearDown(self):
        self.driver.quit()

    def test_1_successful_login(self):
        '''Verifies successful login redirects to index'''
        self.driver.find_element(By.NAME, "email").send_keys("keithlin.student@unireviews.com")
        self.driver.find_element(By.NAME, "password").send_keys("hash6")
        self.driver.find_element(By.NAME, "submit_login").click()

        #verify logout button renders
        logout_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".logout-btn")))

        #verify the greeting text span renders
        greeting_span = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.text-white.small")))

        self.asserTrue(greeting_span.is_displayed())

        


