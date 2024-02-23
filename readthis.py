# # now setup standalone selenium setup check docs then use that. 
# from selenium import webdriver
# import time
# from selenium.webdriver.common.keys  import Keys
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup as bs
# from PIL import Image
# from selenium.webdriver.common.action_chains import ActionChains
# import requests
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# import pandas as pd

# try:

#     #setting up the environment
#     driver = webdriver.Edge()

#     #url of ipsearch
#     url="https://iprsearch.ipindia.gov.in/PublicSearch"

#     #driver-edge
#     driver.get(url)
#     window_before = driver.window_handles[0]

#     #from date 
#     Date= driver.find_element(By.NAME,"FromDate")

#     #captcha value
#     captcha= driver.find_element(By.NAME,"CaptchaText")

#     #put the date value
#     #and the captcha value
#     Date.send_keys("01/01/2024")
#     captcha.send_keys(input())

#     assert "No results found." not in driver.page_source
    
#     #submit both the values
 
#     submit=driver.find_element(By.NAME,"submit")
#     submit.click()
#     time.sleep(5)
#     try:
#         #get all the application no in page1
        
#         application_number_elements= WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.NAME,"ApplicationNumber"))
                                                           
#                                                            )
    
#         application_number_button_links=[x for x in application_number_elements]

#         #for 1 text only
#         # all_application_numbers=[x.text.strip() for x in application_number]
#         application_number_button_links[1].click()
#         time.sleep(5)
    
#         window_after = driver.window_handles[1]
#         driver.switch_to.window(window_after)

#         rows_data=[]
#         tags=driver.find_elements(By.TAG_NAME,'tr')
#         time.sleep(5)
#         dict1={}
#         for tag in tags:

#             cells=tag.find_elements(By.TAG_NAME,'td')

#             for i in range(0, len(cells), 2):
#                 key = cells[i].text.strip()
#                 if i + 1 < len(cells):
#                     value = cells[i + 1].text.strip()
#                     dict1[key] = [value]

    

#         # print(rows_data)
#         # df=pd.DataFrame(dict1)
#         # df.to_csv('csv_data.csv')
#         time.sleep(5)
#         driver.close()

#         driver.switch_to.window(window_before)

#         # time.sleep(5)
#         application_statuses= WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.NAME,"ApplicationSatus")))
#         application_statuses_button_links=[x for x in application_statuses]
#         # window_after=driver.window_handles[1]
#         # driver.switch_to.window(window_after)
#         # time.sleep(5)
#         application_statuses_button_links[1].click()

#         window_after=driver.window_handles[1]
#         driver.switch_to.window(window_after)
#         tags=driver.find_elements(By.TAG_NAME,'tr')
#         # for tag in tags:
#         #     print(tag.text.strip())

#         for tag in tags:

#             cells=tag.find_elements(By.TAG_NAME,'td')

#             for i in range(0, len(cells), 2):
#                 key = cells[i].text.strip()
#                 if i + 1 < len(cells):
#                     value = cells[i + 1].text.strip()
                    

#                     dict1[key] = [value]
#         # print(dict1)
        
#         df2=pd.DataFrame(dict1)
#         df2.to_csv('csv_data.csv')

#         # time.sleep(10)
#         # time.sleep(5)
       
#         # doc_button=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME,"SubmitAction")))
#         # doc_button.click()
#         # time.sleep(10)





# # forward close done
#         # data grab in btw.
#         #now do it in loop
#         # front back again and again first for 2 times. thtn 10 time and then for all
#         # then at last start extracting data then , first create folder functionaloty to save folders as pattent name with docs and folder name as pattent name




#     finally:
#         # print(driver.current_url)
            
#         driver.quit()

    



    

#     #get the url interface
    

#     # actions = ActionChains(driver)
#     # actions.move_to_element(captcha).perform()
#     # time.sleep(3)

#     # print(captcha.location)
#     # time.sleep(3)
#     #crop the location to captcha
#     # crop ss using pil

# except Exception as e:
#     print(e)





from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys  import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def setup_environment():
    return webdriver.Edge()

def navigate_to_url(driver, url):
    driver.get(url)
    return driver.window_handles[0]

def enter_date_and_captcha(driver, date_value, captcha_value):
    date_element = driver.find_element(By.NAME, "FromDate")
    captcha_element = driver.find_element(By.NAME, "CaptchaText")

    date_element.send_keys(date_value)
    captcha_element.send_keys(captcha_value)

def submit_form(driver):
    submit_button = driver.find_element(By.NAME, "submit")
    submit_button.click()
def Button_next(driver):
     button=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"next")))
     return button.click()
     time.sleep(5)
def button_return_page1(driver):
    button= WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"first")))
    button.click()
    time.sleep(5)

def get_application_numbers(driver):
            application_number_button_links=[]
            #get the last page int value (so that we can loop )
            last_page=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"last")))
            last_page=int(last_page.get_attribute("value"))

            

            application_number_elements= WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.NAME,"ApplicationNumber")))
            application_number_button_links.append(application_number_elements)
            #loop to all pages to get the application buttons
            for i in range(2,last_page+1):
                Button_next(driver)     
                application_button_elements= WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.NAME,"ApplicationNumber")))
                application_number_button_links.append(application_button_elements)
            return application_number_button_links

    
def flatten_list(input_list):
    result = []
    for item in input_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result       



def scrape_page_data(driver,dict_data):

    tags = driver.find_elements(By.TAG_NAME, 'tr')
    
    for tag in tags:
        cells = tag.find_elements(By.TAG_NAME, 'td')
        for i in range(0, len(cells), 2):
            key = cells[i].text.strip()
            if i + 1 < len(cells):
                value = cells[i + 1].text.strip()
                if key in dict_data:
                    dict_data[key].append(value)
                else:
                    dict_data[key] = [value]

    return dict_data

# def switch_window_and_scrape(driver, window_handle_index):
#     driver.switch_to.window(driver.window_handles[window_handle_index])
#     return scrape_page_data(driver)

def main():
    dict_data={}
    driver = setup_environment()

    # URL of ipsearch
    url = "https://iprsearch.ipindia.gov.in/PublicSearch"

    window_before = navigate_to_url(driver, url)

    # Enter date and captcha
    enter_date_and_captcha(driver, "02/01/2024", input("Enter captcha: "))

    # Submit the form
    submit_form(driver)
    #get 
    # application_numbers= get_application_numbers(driver)
    # all_application_buttons=flatten_list(application_numbers)
    # #return to page1
    # application_number_button_links=[x for x in all_application_buttons]
    # application_number_button_links[1].click()

    # button_return_page1(driver)




    # # Scraping data from the first page
    # dict_data_page1 = switch_window_and_scrape(driver, 1)

    # # Close the first window
    # driver.close()

    # # Switch back to the original window
    # driver.switch_to.window(window_before)

    # # Switch to the second page and scrape data
    # switch_window_and_scrape(driver, 1)

    # # Create a DataFrame and save it to a CSV file
    # df = pd.DataFrame(dict_data_page1)
    # df.to_csv('csv_data.csv')
    time.sleep(10)
    # # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()
