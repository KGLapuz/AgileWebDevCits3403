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
        self.driver.find_element(By.CSS_SELECTOR, ".login-btn").click()

        #waits for login contianer to render
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-container")))

        #enter credentials
        self.driver.find_element(By.NAME, "email").send_keys("keithlin.student@unireviews.com")
        self.driver.find_element(By.NAME, "password").send_keys("hash6")
        self.driver.find_element(By.NAME, "submit_login").click()

        #verify logout button renders
        logout_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".logout-btn")))

        #verify the greeting text span renders
        greeting_span = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.text-white.small")))

        self.assertTrue(greeting_span.is_displayed())

        logout_confirm = self.driver.find_element(By.CSS_SELECTOR, ".logout-btn").click()

        # verifies redirect to login
        login_redirect = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-container")))

        self.assertTrue(login_redirect.is_displayed())

        

    def test_2_silent_login_failures(self):
        '''Verifies invalid credentials trigger the flash error message'''
        self.driver.find_element(By.NAME, "email").send_keys("keithlin@unireviews.com")
        self.driver.find_element(By.NAME, "password").send_keys("badpassword")
        self.driver.find_element(By.NAME, "submit_login").click()

        #wait for the flash-error CSS class to appear
        error_msg = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".flash-error")))

        self.assertTrue(error_msg.is_displayed())

    def test_3_signup_validation(self):
        '''Verifies failed signup triggers a flash error message'''
        #click the text to pop open the signup modal
        self.driver.find_element(By.CSS_SELECTOR, ".signup-popup").click()

        #wait until the specific signup username field appears
        username_field = self.wait.until(
            (EC.presence_of_element_located((By.CSS_SELECTOR, "#SigunpForm [name='username']")))
        )
        
        #input data intended to trigger a backend error
        username_field.send_keys("keithlin_student")

        #target specific email and password
        self.driver.find_element(By.CSS_SELECTOR, "#SigunpForm [name='email']").send_keys("keithlin.student@unireviews.com")
        self.driver.find_element(By.CSS_SELECTOR, "#SigunpForm [name='password']").send_keys("weakpassword")

        #click to submit
        self.driver.find_element(By.CSS_SELECTOR, ".signup-btn").click()

        # wait for the page to reloed and generic flash message to appear
        flash_msg = self.wait.until(
            (EC.presence_of_element_located((By.CSS_SELECTOR, ".flash-msg")))
        )
        self.assertTrue(flash_msg.is_displayed())

        self.driver.find_element(By.CSS_SELECTOR, ".signup-popup").click()

        inline_error =  self.wait.until(
            (EC.presence_of_element_located((By.CSS_SELECTOR, "#SignupForm .error-text")))
        )

        self.assertTrue(inline_error.is_displayed())

    def test_4_


        





        


