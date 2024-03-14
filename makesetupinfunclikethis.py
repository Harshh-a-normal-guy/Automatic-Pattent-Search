from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys  import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os
base_path="/home/harsh/work_dir/Ipindia/docs"
def setup_environment():
    return webdriver.Edge()

def driver_get(driver,url):
    return driver.get(url)
    
def get_window_handles0(driver):
     return driver.window_handles[0]

def enter_date_and_captcha(driver, date_value,to_Date_value,captcha_value):
    date_element = driver.find_element(By.NAME, "FromDate")
    to_date_element= driver.find_element(By.NAME, "ToDate")
    captcha_element = driver.find_element(By.NAME, "CaptchaText")

    date_element.send_keys(date_value)
    to_date_element.send_keys(to_Date_value)
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

def get_data(tags,dict1):
    for tag in range(0,12):
        cells=tags[tag].find_elements(By.TAG_NAME,'td') #td


        for i in range(0, len(cells), 2):
            key = cells[i].text.strip()
            if i + 1 < len(cells):
                value = cells[i + 1].text.strip()
                dict1[key] = [value]
    
    return dict1
def getInvertorTable_helper(driver,dict1):
     keys=[]
     path='//*[@id="home"]/table/tbody/tr[13]/td/table/tbody'
     Inventor_tbody=driver.find_element(By.XPATH,path)
     tr=Inventor_tbody.find_elements(By.TAG_NAME,"tr")
     Inventor_keys=tr[0].find_elements(By.TAG_NAME,"th")
     
     tr1=tr[1:]
     total_dicts=len(tr1)
     list_of_dicts = [{} for _ in range(total_dicts)]
     Inventor={}
     for i in Inventor_keys:
          keys.append(i.text)
     print('correct')
     for i in range(0,len(tr1)):
          Inventor_values=tr1[i].find_elements(By.TAG_NAME,"td")
          for idx,v in enumerate(Inventor_values):
               list_of_dicts[i][keys[idx]]=v.text
     for d in list_of_dicts:
          for k,v in d.items():
               Inventor.setdefault(k, []).append(v)
     modified_inventor_dict={}
     for k,v in Inventor.items():
          for idx,val in enumerate(v,start=1):
               new_key=f"Inventor_{k}_{idx}"
               modified_inventor_dict[new_key]=val
     return modified_inventor_dict
def getApplicantTable_helper(driver,dict):
     keys=[]
     path_applicant_tbody='//*[@id="home"]/table/tbody/tr[15]/td/table/tbody'
     applicant_body=driver.find_element(By.XPATH,path_applicant_tbody)
     tr=applicant_body.find_elements(By.TAG_NAME,"tr")
     Applicant_keys=tr[0].find_elements(By.TAG_NAME,"th")
     Applicant_data_tr=tr[1:]
     for i in Applicant_keys:
          keys.append(i.text)
     total_dicts=len(Applicant_data_tr)
     list_of_dicts2 = [{} for _ in range(total_dicts)]
     Applicant={}
     for i in range(0,len(Applicant_data_tr)):
        Applicant_values=Applicant_data_tr[i].find_elements(By.TAG_NAME,"td")
        for idx,v in enumerate(Applicant_values):
            list_of_dicts2[i][keys[idx]]=v.text
     Applicant_Details={}
     for d in list_of_dicts2:
          for k,v in d.items():
               Applicant_Details.setdefault(k, []).append(v)
     print("working till here")
     Applicant_modified_dict={}
     print("working2")
     for k,v in Applicant_Details.items():
          print('till here')
          for i,value in enumerate(v,start=1):
            print('in the loop')
            time.sleep(2)
            new_key= f"Applicant_{k}_{i}"
            print('got the key')
            time.sleep(1)
            Applicant_modified_dict[new_key]=value
            print('got thr value')
            time.sleep(2)
            # Applicant_modified_dict[new_key]
     return Applicant_modified_dict





        
def get_application_numbers(driver):
            application_number_button_links=[]
            #get the last page int value (so that we can loop )
            # last_page=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"last")))
            # last_page=int(last_page.get_attribute("value"))
            last_page=1

            

            dataframes=[]
            #loop to all pages to get the application buttons
            for i in range(1,last_page+1):
                
                #get the all_application_buttons
                #application detail in page1 and loops through all
                application_number_elements= WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.NAME,"ApplicationNumber")))
                application_number_button_links=[x for x in application_number_elements]
                application_statuses= WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.NAME,"ApplicationSatus")))
                application_statuses_button_links=[x for x in application_statuses]

                for j in range(len(application_number_button_links)-2,len(application_number_button_links)):
                    #  using application 
                     dict1={}
                     application_number_button_links[j].click()
                    #  time.sleep(10)
                     #inside application number
                     #changed the window to current window

                     window_before= get_window_handles0(driver)
                     window_after = driver.window_handles[1]
                     driver.switch_to.window(window_after)

                     print("till window handles:",j)

                     #find all the data in the appliation button
                     tags=WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.TAG_NAME,'tr')))
                     print("till tags")
        
                     try:
                          
                        dict_data=get_data(tags,dict1)
                        Inventor_data=getInvertorTable_helper(driver,dict_data)
                        
                        data=getApplicantTable_helper(driver,dict_data)
                        return Inventor_data|dict_data|data
                        # return data
                        # return dict_data


                    #  time.sleep(10)
                     except Exception as e:
                          print(e)
                          driver.close()
def main():
    driver = setup_environment()
    

    # URL of ipsearch
    url = "https://iprsearch.ipindia.gov.in/PublicSearch"
    driver_get(driver,url)


    window_before = get_window_handles0(driver)



    # Enter date and captcha
    enter_date_and_captcha(driver, "01/01/2024","01/10/2024", input("Enter captcha: "))

    # Submit the form
    submit_form(driver)
    df=get_application_numbers(driver)
    # df.to_csv("data.csv")
    print(df)
    # df.to_csv("data.csv")

    time.sleep(10)

if __name__=="__main__":
     main()




