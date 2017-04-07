import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class GradeDistribution(unittest.TestCase):


    @classmethod
    def setUpClass(inst):
        #Install extension
        chop = webdriver.ChromeOptions()
        chop.add_argument("load-extension=../Extension")        

        directory = os.path.dirname(os.path.abspath(__file__))
        inst.driver = webdriver.Chrome(executable_path = directory + '/chromedriver', chrome_options = chop)
        inst.driver.implicitly_wait(10)
        inst.driver.set_page_load_timeout(10)
        #Navigate to course guide
        driver = inst.driver
        driver.get('https://my.wisc.edu/web/expanded')
        url = 'https://login.wisc.edu/idp/profile/SAML2/Redirect/SSO'
        #login if not already logged in
        if (url in driver.current_url):
            inst.login(driver)
        try:
            time.sleep(5)
            cg_link = driver.find_element_by_link_text('Go to my course guide')
            #Navigate to course guide link and click it. TODO: fails sometimes
            time.sleep(1)
            ActionChains(driver).move_to_element(cg_link).perform()
            time.sleep(1)
            cg_link.click()
        except Exception as e:
            print(str(e))
            print("Failed to load the CG")
            driver.quit()

        #Switch to the course guide        
        driver.switch_to_window(driver.window_handles[-1])
        #Check if this worked
        source = driver.page_source
        if "Go to my course guide" in source:
            print("Old page still")
            driver.quit()
        else:
            print("New page")
    #Runs before every test
    def setUp(self):
        pass


    #Tests
    
    def test_cg_loaded(self): #Not passing
        driver = self.driver
        source = driver.page_source
        #Make sure do not have old page
        self.assertTrue("Go to my course guide" not in source)
        #And have the new page
        self.assertTrue("CG_Home" in source)
        #Make sure can get elements
        cg = driver.find_element_by_id('CG_browsePluto_29_u360303l1n15_118316_tw_')
        self.assertEqual("CG_browse", cg.get_attribute("class"))

    def test_ave_gpa(self):
        driver = self.driver
        #driver.refresh()
        #TODO: Issue, without the sleep delay, throwing staleelement exception
        time.sleep(3)
        #Go to computer science page
        termId = 'termChoice2'
        subjectValue = '266'
        self.findSubject(termId, subjectValue)
        time.sleep(7)
        #First courseResult card, block with ave gpa
        aveGPA = driver.find_element_by_xpath("//tr[@class='courseResult']/td[7]")
        self.assertIn("Ave. GPA: ", aveGPA.text)
        self.assertIn("2.971", aveGPA.text)    


    def test_grades_dropdown(self): #Not passing
        driver = self.driver
        time.sleep(3)
        #Go to computer science page
        termId = 'termChoice2'
        subjectValue = '266'
        self.findSubject(termId, subjectValue)
        dropdown = driver.find_element_by_xpath("//tr[@class='courseResult']/td[@colspan='8']/a[text()='grades']")
        dropdown.click()
        time.sleep(7)
        #Add assertion for grades dropdown
        gradeTable = driver.find_element_by_xpath("//table[@class='distTable']")
        fall2016gpa = gradeTable.find_element_by_xpath("/tr[2]/td[3]")
        self.assertEqual("3.104", fall2016gpa.text)

    def test_class_page(self):
        driver = self.driver
        #driver.refresh()
        #TODO: Issue, without the sleep delay, throwing staleelement exception
        time.sleep(3)
        #Go to computer science page
        termId = 'termChoice2'
        subjectValue = '266'
        self.findSubject(termId, subjectValue)
        time.sleep(7)
        #Find CS 577 and click on it
        course_card = driver.find_element_by_link_text("Introduction to Algorithms")
        course_card.click()
        
        driver.switch_to_window(driver.window_handles[-1])
        #Check if this worked
        source = driver.page_source
        time.sleep(5)
        
        #Hover over prof links
        prof_link = driver.find_element_by_xpath("//*[@class='CG_instructorDetailsLink']")
        
        time.sleep(5)
        
        hover = ActionChains(driver).move_to_element(prof_link)
        hover.perform()
        
        time.sleep(5)
        self.assertEqual("CHAWLA, SHUCHI", prof_link.text)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        terms = driver.find_element_by_xpath("//*[@id='terms']")
        profs = driver.find_element_by_xpath("//*[@id='professors']")
    
        driver.close();
        driver.switch_to_window(driver.window_handles[1]);
    
        time.sleep(5)
    

    
    #tear down after each test
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(inst):
        inst.driver.quit()
    
    #Helper functions
    def login(driver):
        #driver = self.driver
        username = os.environ.get('UW_USERNAME')
        password = os.environ.get('UW_PASSWORD')
        namebox = driver.find_element_by_name("j_username")
        passbox = driver.find_element_by_name("j_password")
        button = driver.find_element_by_xpath("//button[contains(text(), 'Login')]")
        namebox.send_keys(username)
        passbox.send_keys(password)
        time.sleep(1)
        button.click()

    def findSubject(self, termId, subjectValue):
        driver = self.driver
        term = driver.find_element_by_xpath("//input[@id='" + termId + "']")
        #try:
        #element_present = EC.presence_of_element_located((By.XPATH, driver.find_element_by_xpath("//option[text()='ACTUARIAL SCIENCE']")))
        #WebDriverWait(driver, 10).until(element_present)
            #subject.click()        
        #except Exception as e:
        #    print(str(e))
        #    print("Couldn't get subject")
        subject = driver.find_element_by_xpath("//option[@value='" + subjectValue + "']")
        findButton = driver.find_element_by_xpath("//button[@class='findBtn']")
        
        time.sleep(1)
        term.click()
        subject.click()
        findButton.click()
        time.sleep(2)
        

if __name__ == "__main__":
    unittest.main()
