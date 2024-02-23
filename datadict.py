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

def get_data(tags,dict1):
    for tag in tags:
        cells=tag.find_elements(By.TAG_NAME,'td')

        for i in range(0, len(cells), 2):
            key = cells[i].text.strip()
            if i + 1 < len(cells):
                value = cells[i + 1].text.strip()
                dict1[key] = [value]
    return dict1
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

def DownloadPdfs(driver,path,window_before,app):
     documents=WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.NAME,"DocumentName")))
     print("pass level 1")
     document_name= [x.get_attribute("value") for x in documents]
     print("got all document names")
     buttons= [x for x in documents]
     for val in range(len(buttons)+1):
          buttons[val].click()
          print("clicked on button 1")
          window_after=driver.window_handles[2]
          driver.switch_to.window(window_after)
          print("switched to window Documents")
          time.sleep(5)

          file_name=document_name[val]
          file_path=path +'/'+file_name
          f = open(f"{file_path}.pdf", 'wb')
          for uchar in driver.page_source:
               f.write(bytearray([ord(uchar)]))
          f.close()
          driver.close()
          driver.switch_to.window(window_before)

          




     



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

                for j in range(len(application_number_button_links)-1,len(application_number_button_links)):
                    #  using application 
                     dict1={}
                     application_number_button_links[j].click()
                     time.sleep(10)
                     #inside application number
                     #changed the window to current window
                     window_before= get_window_handles0(driver)
                     window_after = driver.window_handles[1]
                     driver.switch_to.window(window_after)
                     print("till window handles:",j)
                     #find all the data in the appliation button
                     tags=WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.TAG_NAME,'tr')))
                    #  time.sleep(5)
                    #  dict1={}
                     dict_data=get_data(tags,dict1)
                     print('working till tags')
                     driver.close()
                     time.sleep(5)
                     driver.switch_to.window(window_before)
                     application_statuses_button_links[j].click()
                     time.sleep(5)

                     window_after=driver.window_handles[1]
                     driver.switch_to.window(window_after)
                     tags=WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.TAG_NAME,'tr')))
                     print("TIll extra tags")
                     dict_data2=get_data(tags,dict1)
                     time.sleep(3)

                    #  time.sleep(3)
                    #  dict_data2=get_data(tags,dict1)
                     dict_data.update(dict_data2)





                     time.sleep(5)
                     
                     dic=pd.DataFrame(dict_data)
                     Year=GetYear(dic)
                     Month=GetMonth(dic)
                     date=getDate(dic)
                     new_path=createFolder_subfolders(base_path,Year,Month,date)



                    #add here
                     DocumentFolder=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME,"SubmitAction")))
                     DocumentFolder.click()
                     time.sleep(5)
                     DownloadPdfs(driver,new_path,window_before)

                     time.sleep(10)
                     driver.close()
                     
                     driver.switch_to.window(window_before)
                     dataframes.append(dic)
            # return pd.concat(dataframes,ignore_index=True)
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
    driver = setup_environment()
    

    # URL of ipsearch
    url = "https://iprsearch.ipindia.gov.in/PublicSearch"
    driver_get(driver,url)


    window_before = get_window_handles0(driver)



    # Enter date and captcha
    enter_date_and_captcha(driver, "02/01/2024", input("Enter captcha: "))

    # Submit the form
    submit_form(driver)
    df=get_application_numbers(driver)
    # df.to_csv("data.csv")
    print(df)
    # df.to_csv("data.csv")

    time.sleep(10)

if __name__=="__main__":
     main()

# create a folder of that user(application number )
# and one table with all_data