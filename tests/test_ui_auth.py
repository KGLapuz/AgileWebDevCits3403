import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re

from app import create_app, db
from seed_tests import seed_tests
from config import SeleniumTestingConfig
import threading

class UniReviewsAuthTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(SeleniumTestingConfig)

        # seed TEST database
        seed_tests(cls.app)

        # run server in background thread
        def run():
            cls.app.run(port=5001, debug=False, use_reloader=False)

        cls.server = threading.Thread(target=run)
        cls.server.daemon = True
        cls.server.start()
        
    def setUp(self):
        
        #initiliazes the chrome browser before each test
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5001")
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

        login_email = self.driver.find_element(By.NAME, "email")
        login_email.clear()

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
        feature = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".feature-title-box")))
        feature.click()

        # this waits for unit cards to show up before it clicks
        unit_cards = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".review-content")))
        unit_cards.click()

        #this waits for the forum button redirects before it clicks
        fab = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fab-review")))
        fab.click()

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
        feature = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".feature-title-box")))
        feature.click()

        # this waits for unit cards to show up before it clicks
        unit_cards = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".review-content")))
        unit_cards.click()

        #this waits for the forum button redirects before it clicks
        fab = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fab-review")))
        fab.click()

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

        #--navigate to cits3403--
        browse_unit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary-large")))
        browse_unit.send_keys(Keys.ENTER)

        #inside the browsing unit page, users will search for CITS3403
        search_input = self.wait.until(
            EC.visibility_of_element_located((By.NAME, "search"))
        )

        search_input.send_keys("CITS3403", Keys.ENTER)

        target_xpath = "//a[contains(@class, 'unit-card') and .//*[contains(text(), 'CITS3403')]]"

        unit_review_card = self.wait.until(
            EC.presence_of_element_located((By.XPATH, target_xpath))
        )
        #they will then click into the unit page
        unit_review_card.click()

        self.wait.until(EC.url_contains("CITS3403"))

        #further navigate to discussions 
        to_discussions = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "main [data-test='discussions']"))
        )

        to_discussions.send_keys(Keys.ENTER)

        self.wait.until(EC.url_contains("discussions"))

        #--search specific discussion by title--
        card_search_input = self.driver.find_element(By.NAME, "search")
        
        card_search_input.send_keys("How hard is", Keys.ENTER)

        self.wait.until(EC.staleness_of(card_search_input))

        specific_card_xpath = "//*[contains(@class, 'content-card') and contains(., 'How hard is')]"

        search_result = self.wait.until(
            EC.presence_of_element_located((By.XPATH, specific_card_xpath))
        )
        
        # --compares the meta with what it found--
        meta_block = search_result.find_element(By.CSS_SELECTOR, ".card-meta")
        meta_spans = meta_block.find_elements(By.TAG_NAME, "span")
        
        author_text = ""
        timestamp_text = ""
        reply_count_text = ""

        for span in meta_spans:
            text = span.text.lower()
            if "posted by" in text:
                author_text = span.text
            elif "ago" in text or "now" in text or "minute" in text or "day" in text:
                timestamp_text = span.text
            elif "replies" in text or "reply" in text:
                reply_count_text = span.text

        self.assertNotEqual(reply_count_text, "", "could not find a span containing the words")

        digit_match = re.search(r'\d+', reply_count_text)
        extracted_number_str = digit_match.group() if digit_match else ""


        self.assertTrue(extracted_number_str.isdigit())
        initial_reply_count = int(extracted_number_str)
        self.assertGreaterEqual(initial_reply_count, 0)
        self.assertIn("mambwe_admin", author_text.lower(), f"expected author text to show 'Posted by mambwe_admin', but found: {author_text}")

        #--to specific discussion page and reply to a comment--
        search_result.click()

        target_comment = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".comment"))
        )

        actions = ActionChains(self.driver)
        actions.scroll_to_element(target_comment).perform()
        reply_btn = target_comment.find_element(By.CSS_SELECTOR, ".reply-btn")

        self.wait.until(EC.element_to_be_clickable(reply_btn))
        reply_btn.send_keys(Keys.ENTER)

        reply_textarea = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".comment textarea, .reply-input-field"))
        )

        #fills in the reply form 
        reply_textarea.send_keys("This is a valuable advice, thanks.")

        submit_reply_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".submit-reply")
            )
        )

        actions = ActionChains(self.driver)
        actions.scroll_to_element(submit_reply_btn).perform()

        self.driver.execute_script(
            "arguments[0].click();",
            submit_reply_btn
        )

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
        self.assertEqual(
            int(reply_count_value),
            initial_reply_count + 1
        )

    def test_8_create_comment_in_discussion(self):
        '''
        Verifies logged in users can create a comments
        This replicates a user's interaction:
        - login using correct credentials
        - search for a unit 
        - enter its unit page
        - enter its discussion page
        - search for a discussion topic
        - enter the discussion topic
        - leave a comment
        '''
        login_btn = self.driver.find_element(By.CSS_SELECTOR, ".login-btn")
        login_btn.click()

        #waits for login container to render
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-container")))

        #enter credentials
        self.driver.find_element(By.NAME, "email").send_keys("keithlin.student@unireviews.com")
        self.driver.find_element(By.NAME, "password").send_keys("hash6")
        self.driver.find_element(By.NAME, "submit_login").click()

        #--navigate to cits3403--
        browse_unit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary-large")))
        browse_unit.send_keys(Keys.ENTER)

        #inside the browsing unit page, users will search for CITS3403
        search_input = self.wait.until(
            EC.visibility_of_element_located((By.NAME, "search"))
        )

        search_input.send_keys("CITS3403", Keys.ENTER)

        target_xpath = "//a[contains(@class, 'unit-card') and .//*[contains(text(), 'CITS3403')]]"

        unit_review_card = self.wait.until(
            EC.presence_of_element_located((By.XPATH, target_xpath))
        )
        #they will then click into the unit page
        unit_review_card.click()

        self.wait.until(EC.url_contains("CITS3403"))

        #further navigate to discussions 
        to_discussions = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "main [data-test='discussions']"))
        )

        to_discussions.send_keys(Keys.ENTER)

        self.wait.until(EC.url_contains("discussions"))

        #--search specific discussion by title--
        card_search_input = self.driver.find_element(By.NAME, "search")
        
        card_search_input.send_keys("How hard is", Keys.ENTER)

        self.wait.until(EC.staleness_of(card_search_input))

        specific_card_xpath = "//*[contains(@class, 'content-card') and contains(., 'How hard is')]"

        search_result = self.wait.until(
            EC.presence_of_element_located((By.XPATH, specific_card_xpath))
        )
        
        # --compares the meta with what it found--
        meta_block = search_result.find_element(By.CSS_SELECTOR, ".card-meta")
        meta_spans = meta_block.find_elements(By.TAG_NAME, "span")
        
        author_text = ""
        timestamp_text = ""
        reply_count_text = ""

        for span in meta_spans:
            text = span.text.lower()
            if "posted by" in text:
                author_text = span.text
            elif "ago" in text or "now" in text or "minute" in text or "day" in text:
                timestamp_text = span.text
            elif "replies" in text or "reply" in text:
                reply_count_text = span.text

        self.assertNotEqual(reply_count_text, "", "could not find a span containing the words")

        digit_match = re.search(r'\d+', reply_count_text)
        extracted_number_str = digit_match.group() if digit_match else ""
        initial_reply_count = int(extracted_number_str)


        self.assertTrue(extracted_number_str.isdigit())
        self.assertGreaterEqual(initial_reply_count, 0)
        self.assertIn("mambwe_admin", author_text.lower(), f"expected author text to show 'Posted by mambwe_admin', but found: {author_text}")

        #--to specific discussion page and reply to a comment--
        search_result.click()

        #waiting until it finds the element where a comment to be put in
        comment_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "new-comment"))
        )

        #type in the comment
        comment_input.send_keys("Testing for new comment in this thread")
        
        #looked for the post button through ID
        post_btn = self.driver.find_element(By.ID, "post-comment-btn")

        self.wait.until(EC.element_to_be_clickable(post_btn))
        post_btn.click()

        #--checks if posting the comment was successful--
        #checks if the comment input field is now empty
        self.wait.until(lambda d: comment_input.get_attribute("value") == "")

        #wait until comments are rendered
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".comment")))

        #collects all the existing comments in the page
        all_comments = self.driver.find_elements(By.CSS_SELECTOR, ".comment")

        #latest comment would always be at the bottom. 
        newest_comment = all_comments[-1]

        actions = ActionChains(self.driver)
        #scroll to the bottom where the latest comment should be
        actions.scroll_to_element(newest_comment).perform()

        #confirm the meta values match
        comment_p = newest_comment.find_elements(By.TAG_NAME, "p")

        newest_comment_text = comment_p[1].text

        self.assertEqual(
            newest_comment_text, "Testing for new comment in this thread", f"the latest comment didn't match our post"
        )

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
        self.assertEqual(
            int(reply_count_value),
            initial_reply_count + 1
        )

    def test_9_guest_receive_flashmessage_if_attempted_to_comment(self):
        '''
        Verifies guest cannot reply to comments
        This replicates a user's interaction:
        - search for a unit 
        - enter its unit page
        - enter its discussion page
        - search for a discussion topic
        - enter the discussion topic
        - leave a comment
        - receive flash warning to log in
        '''
        #guest no login required. Straight into navigation
        #--navigation to cits3403 discussion--
        #this button will redirect to the browsing unit page
        browse_unit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary-large")))
        browse_unit.send_keys(Keys.ENTER)

        #inside the browsing unit page, users will search for CITS3403
        search_input = self.wait.until(
            EC.visibility_of_element_located((By.NAME, "search"))
        )

        search_input.send_keys("CITS3403", Keys.ENTER)

        target_xpath = "//a[contains(@class, 'unit-card') and .//*[contains(text(), 'CITS3403')]]"

        unit_review_card = self.wait.until(
            EC.presence_of_element_located((By.XPATH, target_xpath))
        )
        #they will then click into the unit page
        unit_review_card.click()

        self.wait.until(EC.url_contains("CITS3403"))

        #further navigate to discussions 
        to_discussions = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "main [data-test='discussions']"))
        )

        to_discussions.send_keys(Keys.ENTER)

        self.wait.until(EC.url_contains("discussions"))

        #--search specific discussion by title--
        card_search_input = self.driver.find_element(By.NAME, "search")
        
        card_search_input.send_keys("How hard is", Keys.ENTER)

        self.wait.until(EC.staleness_of(card_search_input))

        specific_card_xpath = "//*[contains(@class, 'content-card') and contains(., 'How hard is')]"

        search_result = self.wait.until(
            EC.presence_of_element_located((By.XPATH, specific_card_xpath))
        )
        
        # --compares the meta with what it found--
        meta_block = search_result.find_element(By.CSS_SELECTOR, ".card-meta")
        meta_spans = meta_block.find_elements(By.TAG_NAME, "span")
        
        author_text = ""
        timestamp_text = ""
        reply_count_text = ""

        for span in meta_spans:
            text = span.text.lower()
            if "posted by" in text:
                author_text = span.text
            elif "ago" in text or "now" in text or "minute" in text or "day" in text:
                timestamp_text = span.text
            elif "replies" in text or "reply" in text:
                reply_count_text = span.text

        self.assertNotEqual(reply_count_text, "", "could not find a span containing the words")

        digit_match = re.search(r'\d+', reply_count_text)
        extracted_number_str = digit_match.group() if digit_match else ""
        initial_reply_count = int(extracted_number_str)

        self.assertTrue(extracted_number_str.isdigit())
        self.assertGreaterEqual(initial_reply_count, 0)
        self.assertIn("mambwe_admin", author_text.lower(), f"expected author text to show 'Posted by mambwe_admin', but found: {author_text}")

        #--to specific discussion page and reply to a comment--
        search_result.click()

        target_comment = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".comment"))
        )

        actions = ActionChains(self.driver)
        actions.scroll_to_element(target_comment).perform()
        reply_btn = target_comment.find_element(By.CSS_SELECTOR, ".reply-btn")

        self.wait.until(EC.element_to_be_clickable(reply_btn))
        reply_btn.send_keys(Keys.ENTER)

        reply_textarea = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".comment textarea, .reply-input-field"))
        )

        #fills in the reply form 
        reply_textarea.send_keys("This is a valuable advice, thanks.")

        submit_reply_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".submit-reply")
            )
        )

        actions = ActionChains(self.driver)
        actions.scroll_to_element(submit_reply_btn).perform()

        self.driver.execute_script(
            "arguments[0].click();",
            submit_reply_btn
        )

        flash_alert = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert"))
        )

        self.assertTrue(flash_alert.is_displayed(), "flash alert failed to appear")

        #waiting until it finds the element where a comment to be put in
        comment_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "new-comment"))
        )

        #type in the comment
        comment_input.send_keys("Testing for new comment in this thread")
        
        #looked for the post button through ID
        post_btn = self.driver.find_element(By.ID, "post-comment-btn")

        self.wait.until(EC.element_to_be_clickable(post_btn))
        post_btn.click()

        second_flash_alert = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert"))
        )

        self.assertTrue(second_flash_alert.is_displayed(), "second flash alert failed to appear")

    def test_10_logged_in_user_create_discussion(self):
        '''
        Verifies that the user's submission was added to the page
        
        In this test it is replicating a user's action:
        - going to the login and input credentials
        - navigating to discussion
        - filling up the discussion form
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
        feature = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".feature-title-box")))
        feature.click()

        # this waits for unit cards to show up before it clicks
        unit_cards = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".review-content")))
        unit_cards.click()

        #this waits for the forum button redirects before it clicks
        fab = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fab-discussion")))
        fab.click()

        title_input = self.wait.until(EC.visibility_of_element_located((By.ID, "title")))


        test_title = "Is the CITS1401 final exam heavily based on project?"
        title_input.send_keys(test_title)

        typed_value = title_input.get_attribute("value")
        self.assertEqual(typed_value, test_title, f"expected input valued to be '{test_title}, but found 'typed_value'")

        body_input = self.wait.until(EC.visibility_of_element_located((By.ID, "body")))

        body_input.clear()

        test_body = "Testing the description of the discussion page"
        body_input.send_keys(test_body)

        body_value = body_input.get_attribute("value")
        self.assertEqual(body_value, test_body, f"mismatched")

        submit_btn = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )

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
        meta_block = self.driver.find_element(By.CSS_SELECTOR, ".card-meta")
        meta_spans = meta_block.find_elements(By.TAG_NAME, "span")
        
        author_text = ""
        timestamp_text = ""
        reply_count_text = ""

        for span in meta_spans:
            text = span.text.lower()
            if "posted by" in text:
                author_text = span.text
            elif "ago" in text or "now" in text or "minute" in text or "day" in text:
                timestamp_text = span.text
            elif "replies" in text or "reply" in text:
                reply_count_text = span.text

        self.assertNotEqual(reply_count_text, "", "could not find a span containing the words")

        digit_match = re.search(r'\d+', reply_count_text)
        extracted_number_str = digit_match.group() if digit_match else ""


        self.assertTrue(extracted_number_str.isdigit())
        self.assertEqual(int(extracted_number_str), 0, f"expected 0 initial replies, but found: {extracted_number_str}")
        self.assertIn("you", author_text.lower(), f"expected author text to show 'Posted by you', but found: {author_text}")

    def test_11_logged_in_user_create_project(self):
        '''
        Verifies that the user's submission was added to the page
        
        In this test it is replicating a user's action:
        - going to the login and input credentials
        - navigating to projects
        - filling up the project form
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
        feature = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".feature-title-box")))
        feature.click()

        # this waits for unit cards to show up before it clicks
        unit_cards = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".review-content")))
        unit_cards.click()

        #this waits for the forum button redirects before it clicks
        fab = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fab-project")))
        fab.click()

        title_input = self.wait.until(EC.visibility_of_element_located((By.ID, "project_title")))
        title_input.clear()

        project_title = "CITS1401 projest csv examples"
        title_input.send_keys(project_title)

        typed_value = title_input.get_attribute("value")
        self.assertEqual(typed_value, project_title, f"expected input valued to be '{project_title}, but found 'typed_value'")

        project_link = self.wait.until(EC.visibility_of_element_located((By.ID, "repo_link")))
        project_link.clear()

        project_input = "https://github.com/KGLapuz/AgileWebDevCits3403"
        project_link.send_keys(project_input)

        project_value = project_link.get_attribute("value")
        self.assertEqual(project_value, project_input, f"mismatched url")

        body_input = self.wait.until(EC.visibility_of_element_located((By.ID, "project_body")))

        body_input.clear()

        test_body = "Testing the description of the project page"
        body_input.send_keys(test_body)

        body_value = body_input.get_attribute("value")
        self.assertEqual(body_value, test_body, f"mismatched")

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
        meta_block = self.driver.find_element(By.CSS_SELECTOR, ".card-meta")
        meta_spans = meta_block.find_elements(By.TAG_NAME, "span")
        
        author_text = ""
        timestamp_text = ""

        for span in meta_spans:
            text = span.text.lower()
            if "ago" in text or "now" in text or "minute" in text or "day" in text:
                timestamp_text = span.text
            else:
                if span.text.strip():
                    author_text = span.text

        self.assertIn("keithlin_student", author_text.lower(), f"expected author text to show 'keithlin_student', but found: {author_text}")

if __name__ == "__main__":
    unittest.main()
