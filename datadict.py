from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys  import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os
import re
import requests
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.options import Options

base_path="/home/harsh/work_dir/Ipindia/docs"
def setup_environment(base_path):
    

     option = Options()
     option.add_experimental_option("prefs", {
    "download.default_directory": base_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Set the download directory
     return webdriver.Edge(options=option)

def driver_get(driver,url):
    return driver.get(url)
    
def get_window_handles0(driver):
     return driver.window_handles[0]

def enter_date_and_captcha(driver, date_value,to_Date_value,captcha_value):
    date_element = driver.find_element(By.NAME, "FromDate")
    to_date_element= driver.find_element(By.NAME, "ToDate")
    captcha_element = driver.find_element(By.NAME, "CaptchaText")

    date_element.send_keys(date_value)
#     time.sleep(100)
    to_date_element.send_keys(to_Date_value)
    time.sleep(10)
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
     # print("working till here")
     Applicant_modified_dict={}
     # print("working2")
     for k,v in Applicant_Details.items():
          # print('till here')
          for i,value in enumerate(v,start=1):
          #   print('in the loop')
            time.sleep(2)
            new_key= f"Applicant_{k}_{i}"
          #   print('got the key')
            time.sleep(1)
            Applicant_modified_dict[new_key]=value
          #   print('got thr value')
            time.sleep(2)
            # Applicant_modified_dict[new_key]
     return Applicant_modified_dict

    # dict name_= invertor# "name":[val,val,val]
                #Address = ["val1",val2,val3]
    #dict name Applicant
                # str= key= name=[nam31,name2,name3]
            # val= [address1,address2,address3]

def GetYear(dataframe):
      yearFiling=pd.to_datetime(dataframe["Application Filing Date"])
      return str(yearFiling.dt.year.iloc[0])
def GetMonth(dataframe):
     MonthFiling=pd.to_datetime(dataframe["Application Filing Date"],format="%d/%m/%Y")
     
     MonthFiling=str(MonthFiling.dt.month_name().iloc[0])
     # val=convertMonth(str(MonthFiling))
     return MonthFiling

def getDate(dataframe):
     DateFiling=pd.to_datetime(dataframe["Application Filing Date"],format="%d/%m/%Y")
     return str(DateFiling.dt.day.iloc[0])

     

def createFolder_subfolders(basepath,year,month,date):
     os.makedirs(basepath,exist_ok=True)
     year_folder_path= os.path.join(basepath,year,month,date)

     os.makedirs(year_folder_path,exist_ok=True)
     return year_folder_path


    #  os.makedirs(dateFolderPath,exist_ok=True)
def GetStatus(driver):
     green_val='45,147,45'
     not_green="199,199,199"

     patth='//*[@id="Content"]/table/tbody'
     status=driver.find_element(By.XPATH,patth)
     td=status.find_element(By.TAG_NAME,"td")
     innerHTML=td.get_attribute('innerHTML')
     soup=BeautifulSoup(innerHTML,'html.parser')
     class_lst=soup.find_all('span')
     status_dict={}
    #  soup.find(class_=)
     for i in range(1,len(class_lst),2):
          style_attr=class_lst[i].get('style')

# Use regular expression to extract numeric values and commas
          numeric_values=re.findall(r'\b\d+\b|,', style_attr)

# Concatenate the extracted values into a string
          result = ''.join(numeric_values)
          if result==green_val:
               
        #   time.sleep(3)
            status_dict[class_lst[i].text]=True
          else:
            status_dict[class_lst[i].text]=False

        #   print(result,class_lst[i].text)
        #   print(type(result))
     return status_dict


     
def DownloadPdfs(driver,path,window_before):
     documents=WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.NAME,"DocumentName")))
     print("got document names")
    #  print("pass level 1")
     document_name= [x.get_attribute("value") for x in documents]
     print("got all document names")
     buttons= [x for x in documents]
     for val in range(len(buttons)):
          # print(document_name[val])
          buttons[val].click()
          print("clicked on button 1")
          window_after=driver.window_handles[2]
          driver.switch_to.window(window_after)
          ss_path=path+f"{document_name[val][:-3]}"
          print('pathname done')

          print(driver.current_url)
          time.sleep(5)
          action_chains = ActionChains(driver)
          action_chains.key_down(Keys.CONTROL).send_keys('s').perform()

          time.sleep(5)

          file_name=document_name[val]
          file_path=path +'/'+f"{file_name}"
          pyautogui.typewrite(file_path)
          pyautogui.press('enter')
          # action_chains.key_up(Keys.CONTROL).send_keys('s').perform()
          # action_chains.send_keys(Keys.ENTER)

          # pdf_viewer = WebDriverWait(driver,40).until(EC.presence_of_element_located((By.CLASS_NAME,"c0173 c0188 c0178 c0187 c0162 c0165")))
          # print(pdf_viewer)
          print('pdf workded')# Replace with the actual class name or other locator

          print('worked download key')

          # download_button = driver.find_element_by_id('download')



# Click on the download button to trigger the download
          # download_button.click()
          time.sleep(5)

          # driver.get_full_page_screenshot_as_file(ss_path)

          # pyautogui.hotkey('ctrl','s')

        #   time.sleep(5)

#           print("switched to window Documents")
          time.sleep(5)
          driver.close()
          time.sleep(3)
          print('closed')
          driver.switch_to.window(driver.window_handles[1])
          time.sleep(5)
          print('switched')
        #   file_name=document_name[val]
        #   print(file_name)
        #   file_path=path +'/'+f"{file_name}"
        #   #filepath (application Number se after 19th date use application NUmber Folder then download pdf)
        #   print(file_path)
        #   print('working here')
        #   pyautogui.typewrite(file_path)
        #   print("type write filepath ")

        #   pyautogui.press('enter')
        #   print("pressed enter")

        #   f = open(f"{file_path}.pdf", 'wb')
#           for uchar in driver.page_source:
#                f.write(bytearray([ord(uchar)]))
#           f.close()
#           driver.close()
#           driver.switch_to.window(window_before)

          




     



     #create year folders
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

                for j in range(0,len(application_number_button_links)):
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
                    #  time.sleep(5)
                    #  dict1={}
                         # Wait for the element to be present on the page

    # )
                     time.sleep(5)

                    #  print(tags)
                    #  print(len(tags))
                     
                     dict_data=get_data(tags,dict1)
                     Inventor_data=getInvertorTable_helper(driver,dict_data)
                        
                     data=getApplicantTable_helper(driver,dict_data)
                     data= Inventor_data|dict_data|data
                    #  print(dict_data)

                     print('working till tags')
                     driver.close()
                    #  time.sleep(5)
                     driver.switch_to.window(window_before)
                     application_statuses_button_links[j].click()
                     time.sleep(5)

                     window_after=driver.window_handles[1]
                     driver.switch_to.window(window_after)
                     tags=WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.TAG_NAME,'tr')))
                     print("TIll extra tags")
                     dict_data2=get_data(tags,dict1)
                    # #  time.sleep(3)

                    # #  time.sleep(3)
                     dict_data2=get_data(tags,dict1)
                     data=data|dict_data2
                    #  print(data)
                     status_data= GetStatus(driver)
                     data=data|status_data
                     







                    # #  time.sleep(5)
                     
                     dic=pd.DataFrame(data)
                     Year=GetYear(dic)
                     Month=GetMonth(dic)
                     date=getDate(dic)
                     new_path=createFolder_subfolders(base_path,Year,Month,date)
                    #  print(GetStatus)
                     


                    #add here
                    #  DocumentFolder=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME,"SubmitAction")))
                    #  DocumentFolder.click()
                    #  time.sleep(5)
                    #  DownloadPdfs(driver,new_path,window_before)

                    #  time.sleep(10)
                     driver.close()

                     
                     driver.switch_to.window(window_before)
                     dataframes.append(dic)
            return pd.concat(dataframes,ignore_index=True)
#getting the whole data but need pdf files in a folder(having name= Application No)
# ps- create folder having application nos and store pdfs
# task1 - download pdfs
#task2- create folders
# task3 - do that in loop
# task 4 - clean the cols(write a func)
 

            
                # Button_next(driver)     
                # application_button_elements= WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.NAME,"ApplicationNumber")))
            # return application_number_button_links

def main():
    driver = setup_environment(base_path)
    

    # URL of ipsearch
    url = "https://iprsearch.ipindia.gov.in/PublicSearch"
    driver_get(driver,url)


    window_before = get_window_handles0(driver)



    # Enter date and captcha
    enter_date_and_captcha(driver,input("Month :") +'/'+input("Date :") +"/"+input("fromYear :") ,"03/13"+input("Year : "), input("Enter captcha: "))

    # Submit the form
    submit_form(driver)
    df=get_application_numbers(driver)
    # df.to_csv("data.csv")
#     print(df)
    df.to_csv("data2.csv")

    time.sleep(10)

if __name__=="__main__":
     main()

# create a folder of that user(application number )
# and one table with all_data