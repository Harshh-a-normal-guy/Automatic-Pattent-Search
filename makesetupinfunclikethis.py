# import unittest
# from selenium import webdriver

# class GoogleOrgSearch(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Firefox()

#     def test_google_search_page(self):
#         driver = self.driver
#         driver.get("http://www.cdot.in")
#         window_before = driver.window_handles[0]
#         print window_before
#         driver.find_element_by_xpath("//a[@href='http://www.cdot.in/home.htm']").click()
#         window_after = driver.window_handles[1]
#         driver.switch_to.window(window_after)
#         print window_after
#         driver.find_element_by_link_text("ATM").click()
#         driver.switch_to.window(window_before)

#     def tearDown(self):
#         self.driver.close()

# if __name__ == "__main__":
#     unittest.main()