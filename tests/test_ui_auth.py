import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class UniReviewsAuthTest(unittest.TestCase):
    def setUp(self):
        #initiliazes the chrome browser before each test
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000")
        self. wait = WebDriverWait(self.driver, 10) #explicitly wait for dynamic elements

    def tearDown(self):
        self.driver.quit()

    def test_1_successful_login(self):
        '''
        Verifies successful login redirects to index and logout redirects to login page
        
        In this test it is replicating a user's action:
        - going to login
        - inputting credentials
        - submitting login form
        - successful login and redirect to index
        - logging out and answering confirmation
        - redirected back to login page
        '''
        login_btn = self.driver.find_element(By.CSS_SELECTOR, ".login-btn")
        login_btn.click()

        #waits for login container to render
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

        #looks for the logout button and clicks it
        logout_confirm = self.driver.find_element(By.CSS_SELECTOR, ".logout-btn")
        logout_confirm.click()

        #wait till the logout alert opens
        self.wait.until(EC.alert_is_present())

        logout_alert = self.driver.switch_to.alert
        
        #accepts logout alert
        logout_alert.accept()

        # verifies redirect to login
        login_redirect = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-container")))

        self.assertTrue(login_redirect.is_displayed())

        

    def test_2_silent_login_failures(self):
        '''
        Verifies invalid credentials trigger the flash error message

        In this test it is replicating a user's action:
        - going to login page
        - inputting incorrect credentials
        - receiving flash error of mismatching credentials
        '''

        
        login_btn = self.driver.find_element(By.CSS_SELECTOR, ".login-btn")
        login_btn.click()

        #waits for login container to render
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-container")))

        #enter credentials
        self.driver.find_element(By.NAME, "email").send_keys("keithlin@unireviews.com")
        self.driver.find_element(By.NAME, "password").send_keys("badpassword")
        self.driver.find_element(By.NAME, "submit_login").click()

        #wait for the flash-error CSS class to appear
        error_msg = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".flash-error")))

        self.assertTrue(error_msg.is_displayed())

    def test_3_signup_validation(self):
        '''
        Verifies failed signup triggers a flash error message
        
        In this test it is replicating a user's action:
        - going to login
        - opening signup form
        - inputting credentials that already exist in database
        - submitting signup form
        - receiving a flash error for failed signup
        '''
        login_btn = self.driver.find_element(By.CSS_SELECTOR, ".login-btn")
        login_btn.click()

        #waits for login container to render
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-container")))
        
        #click the text to pop open the signup modal
        self.driver.find_element(By.CSS_SELECTOR, ".signup-popup").click()

        #wait until the specific signup username field appears
        username_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#SignUpForm [name='username']"))
        )
        
        #input data intended to trigger a backend error
        self.driver.find_element(By.CSS_SELECTOR, "#SignUpForm [name='username']").send_keys("keithlin_student")

        #target specific email and password
        self.driver.find_element(By.CSS_SELECTOR, "#SignUpForm [name='email']").send_keys("keithlin.student@unireviews.com")
        self.driver.find_element(By.CSS_SELECTOR, "#SignUpForm [name='password']").send_keys("weakpassword")

        #click to submit
        self.driver.find_element(By.CSS_SELECTOR, ".signup-btn").click()

        # wait for the page to reload and generic flash message to appear
        flash_msg = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".flash-msg"))
        )
        self.assertTrue(flash_msg.is_displayed())

        self.driver.find_element(By.CSS_SELECTOR, ".signup-popup").click()

        inline_error =  self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#SignUpForm .error-text"))
        )

        self.assertTrue(inline_error.is_displayed())

    def test_4_successful_signup_login_with_new_account(self):
        '''
        Verifies new accounts can login

        In this test it is replicating a user's action:
        - going to login page and opening signup form
        - fill in signup form with new credentials
        - submit signup form
        - receive generic flash message showing that the submission was successful
        - sign in with the new credentials
        - logout and accept alert
        - redirected to login page
        '''

        #--Create account--
        login_btn = self.driver.find_element(By.CSS_SELECTOR, ".login-btn")
        login_btn.click()
        #waits for login container to render
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-container")))
        
        #click the text to pop open the signup modal
        self.driver.find_element(By.CSS_SELECTOR, ".signup-popup").click()

        #wait until the specific signup username field appears
        username_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#SignUpForm [name='username']"))
        )

        #create new account with these credentials
        self.driver.find_element(By.CSS_SELECTOR, "#SignUpForm [name='username']").send_keys("new_user")
        self.driver.find_element(By.CSS_SELECTOR, "#SignUpForm [name='email']").send_keys("new_user@unireviews.com")
        self.driver.find_element(By.CSS_SELECTOR, "#SignUpForm [name='password']").send_keys("Newuserpassword1!")

        #click to submit
        self.driver.find_element(By.CSS_SELECTOR, ".signup-btn").click()

        # wait for the page to reload and generic flash message to appear
        flash_msg = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".flash-msg"))
        )
        self.assertTrue(flash_msg.is_displayed())
        
        #--Login with new credentials--
        #waits for login container to render
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-container")))

        #enter new account credentials
        self.driver.find_element(By.NAME, "email").send_keys("new_user@unireviews.com")
        self.driver.find_element(By.NAME, "password").send_keys("Newuserpassword1!")
        self.driver.find_element(By.NAME, "submit_login").click()

        #verify logout button renders
        logout_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".logout-btn")))

        #verify the greeting text span renders
        greeting_span = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.text-white.small")))

        self.assertTrue(greeting_span.is_displayed())

        #looks for the logout button and clicks it
        logout_confirm = self.driver.find_element(By.CSS_SELECTOR, ".logout-btn")
        logout_confirm.click()

        #wait till the logout alert opens
        self.wait.until(EC.alert_is_present())

        logout_alert = self.driver.switch_to.alert
        
        #accepts logout alert
        logout_alert.accept()

        # verifies redirect to login
        login_redirect = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-container")))

        self.assertTrue(login_redirect.is_displayed())



    def test_5_redirect_guest_to_login_if_they_attempt_to_submit_review_form(self):
        ''' 
        Verifies that the guest users are redirected to the login page when they try to submit reviews
        
        In this test it is replicating a user's action:
        - navigating to reviews
        - clicking the review button
        - being redirected to login page
        '''
        # clicks on the first button that is of class feature-title-box
        # figured since all the buttons are all redirecting to the home-page the test shouldn't need to look into each specific button
        self.driver.find_element(By.CSS_SELECTOR, ".feature-title-box").click()

        # this waits for unit cards to show up before it clicks
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".review-content"))).click()

        #this waits for the forum button redirects before it clicks
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fab-review"))).click()

        checkfor_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-container")))

        self.assertTrue(checkfor_login.is_displayed())

    def test_6_loggedIn_Submit_Form(self):
        '''
        Verifies that the user's submission was added to the page
        
        In this test it is replicating a user's action:
        - going to the login and input credentials
        - navigating to reviews
        - filling up the reviews form
        - submitting the form and being redirected to the extend html of content list
        '''
        # --login process--
        login_btn = self.driver.find_element(By.CSS_SELECTOR, ".login-btn")
        login_btn.click()

        #waits for login container to render
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-container")))

        #enter credentials
        self.driver.find_element(By.NAME, "email").send_keys("keithlin.student@unireviews.com")
        self.driver.find_element(By.NAME, "password").send_keys("hash6")
        self.driver.find_element(By.NAME, "submit_login").click()

        # --navigation to form--
        self.driver.find_element(By.CSS_SELECTOR, ".feature-title-box").click()

        # this waits for unit cards to show up before it clicks
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".review-content"))).click()

        #this waits for the forum button redirects before it clicks
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fab-review"))).click()

        # waits until the ratings have rendered and click it once it is
        four_star_label = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[data-value='4']")))
        four_star_label.click()

        #--filling out the form--
        # checks that the user was able to interact with the star rating
        four_star_input = self.driver.find_element(By.ID, "rating-4")
        self.assertTrue(four_star_input.is_selected(), "star rating failed to select")

        #clicks on the hour glass
        hourglass_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-value='7']")))
        hourglass_button.click()
        button_input = self.driver.find_element(By.ID, "workload")

        #checks for the value of workload
        self.assertEqual(
            button_input.get_attribute("value"),
            "7",
            "The workload input did not update to 7!"
        )

        #looks for the content and type in review
        self.driver.find_element(By.ID, "content").send_keys(
            "The workload is heavy, but the project were fantastic. Make sure to start the assingment early."
        )

        #submit the form
        submit_btn = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )

        actions = ActionChains(self.driver)

        actions.scroll_to_element(submit_btn).perform()

        self.wait.until(EC.element_to_be_clickable(submit_btn))

        submit_btn.click()

        #waits until it locates the flash
        flash_msg = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )

        #verifies the flash appeard
        self.assertTrue(flash_msg.is_displayed(), "Success flash message did not appear!")

        # --verification for the latest review card by user appeared with correct meta--
        #waits until it locates the lates review card
        latest_review_card = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".review-card"))
        )

        # --compares the meta with what it found--
        meta_text = latest_review_card.find_element(By.CSS_SELECTOR, ".review-meta").text
        self.assertIn("You", meta_text, "author meta tag does not say 'you'")

        preview_text = latest_review_card.find_element(By.CSS_SELECTOR, ".review-preview").text
        self.assertIn("The workload is heavy, but the project were fantastic. Make sure to start the assingment early.", preview_text, "review-mismatched")

        star_text = latest_review_card.find_element(By.CSS_SELECTOR, ".stat-value").text
        self.assertEqual(star_text.strip(), "4", "the rendered star rating was not 4")

        workload_container = latest_review_card.find_elements(By.CSS_SELECTOR, ".review-stat")[1]
        self.assertIn("7", workload_container.text, "workload mismatch")
    
    def test_7_reply_comment_in_discussion(self):
        '''
        Verifies logged in users can reply to discussion comments
        This replicates a user's interaction:
        - login using correct credentials
        - search for a unit 
        - enter its unit page
        - enter its discussion page
        - search for a discussion topic
        - enter the discussion topic
        - leave a reply to an existing comment
        '''
        # --login process--
        login_btn = self.driver.find_element(By.CSS_SELECTOR, ".login-btn")
        login_btn.click()

        #waits for login container to render
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-container")))

        #enter credentials
        self.driver.find_element(By.NAME, "email").send_keys("keithlin.student@unireviews.com")
        self.driver.find_element(By.NAME, "password").send_keys("hash6")
        self.driver.find_element(By.NAME, "submit_login").click()

        #--navigation to cits3403 discussion--
        #this button will redirect to the browsing unit page
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary=large").click()

        #inside the browsing unit page, users will search for CITS3403
        self.driver.find_element(By.NAME, "search").send_keys("CITS3403")

        unit_review_card = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".review-content"))
        )
        #they will then click into the unit page
        unit_review_card.click()

        #further navigate to discussions 
        to_discussions = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='discussions']"))
        )

        actions = ActionChains(self.driver)

        actions.scroll_to_element(to_discussions).perform()

        self.wait.until(EC.element_to_be_clickable(to_discussions))

        to_discussions.click()

        #--search specific discussion by title--
        self.driver.find_element(By.NAME, "search").send_keys("How hard is")

        search_result = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".content-card"))
        )
        
        # --compares the meta with what it found--
        meta_block = search_result.find_element(By.CSS_SELECTOR, ".card-meta")
        meta_spans = meta_block.find_element(By.TAG_NAME, "span")
        author_text = meta_spans[0].text
        timestamp_text = meta_spans[1].text
        reply_count_text = meta_spans[2].text

        timestamp_pattern = r"(just now|second|minute|hour|day|ago)"
        text_fragments = reply_count_text.split()
        extracted_number_str = text_fragments[1]

        self.assertTrue(extracted_number_str.isdigit())
        self.assertEqual(int(extracted_number_str), 9, f"expected 9 initial replies, but found: {extracted_number_str}")
        self.assertIn("Posted by mambwe_admin", author_text, f"expected author text to show 'Posted by mambwe_admin', but found: {author_text}")
        self.assertTrue(
            re.search(timestamp_pattern, timestamp_text, re.IGNORECASE),
            f"Timestamp text format is invalid. Found: '{timestamp_text}"
        )

        #--to specific discussion page and reply to a comment--
        search_result.click()

        target_comment = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".comment"))
        )

        actions.scroll_to_element(target_comment).perform()
        reply_btn = target_comment.find_element(By.CSS_SELECTOR, ".reply-btn")

        self.wait.until(EC.element_to_be_clickable(reply_btn))
        reply_btn.click()

        reply_textarea = self.wait.until(
            EC.visibility_of_element_located(By.CSS_SELECTOR, ".comment textarea, .reply-input-field")
        )

        #fills in the reply form 
        reply_textarea.send_keys("This is a valuable advice, thanks.")

        submit_reply_btn = target_comment.find_element(By.CSS_SELECTOR, "button[type='submit'], submit-reply")
        submit_reply_btn.click()

        new_reply_card = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".comment .replies .comment"))
        )

        #checks for the new reply in the nested comment
        self.assertTrue(new_reply_card.is_displayed(), "nested reply comment block failed to render in UI layout")
        
        #--Check for update in meta value and if existing author value is the same--
        sticky_header = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".thread-sticky"))
        )

        meta_text_block = sticky_header.find_element(By.CSS_SELECTOR, ".sticky-meta").text
        self.assertIn("Posted by mambwe_admin", meta_text_block, f"author name verification failed in sticky header")

        #reply count will update, so we are checking here if it turns to 10. 
        reply_count = sticky_header.find_element(By.CSS_SELECTOR, ".thread-reply-count")
        reply_count_value = reply_count.text.strip()

        self.assertTrue(reply_count_value.isdigit())
        self.assertEqual(int(reply_count_value), 10, f"expected 10 initial replies, but found: {reply_count_value}")









if __name__ == "__main__":
    unittest.main()
