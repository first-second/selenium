import time
import pandas as pd 
from getpass import getpass   
# ------------- # 
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Driver path
#path = '/Users/kurum/Downloads/chromedriver.exe'
driver = webdriver.Chrome()  

# Maximize Window
driver.maximize_window() 
driver.minimize_window()  
driver.maximize_window()  
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(10)

# Enter to the site
driver.get('https://www.linkedin.com/login');
time.sleep(5)

# Accept cookies
#driver.find_element(By.XPATH,"/html/body/div/main/div[1]/div/section/div/div[2]/button[2]").click()

# User Credentials
user_name = input("enter email : ")
password = getpass("enter password : ")
driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(user_name)
driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(password)
time.sleep(1)

# Login button
driver.find_element(By.XPATH,'/html/body/div/main/div[2]/div[1]/form/div[3]/button').click()
driver.implicitly_wait(30)

# Jobs page
driver.find_element(By.XPATH,'/html/body/div[5]/header/div/nav/ul/li[3]/a').click()
time.sleep(3)
# Go to search results directly
#driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3418556965&keywords=python&refresh=true")
driver.find_element(By.XPATH,'/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]').send_keys("python",Keys.ENTER)
time.sleep(10)
print("close")
# Get all links for these offers
links = []
# Navigate 13 pages
print('Links are being collected now.')
try: 
    for page in range(2,3):
        time.sleep(2)
        jobs_block = driver.find_element(By.CLASS_NAME,'jobs-search-results-list')
        jobs_list= jobs_block.find_elements(By.CSS_SELECTOR, '.job-card-list')
    
        for job in jobs_list:
            all_links = job.find_elements(By.TAG_NAME,'a')
            for a in all_links:
                if str(a.get_attribute('href')).startswith("https://www.linkedin.com/jobs/view") and a.get_attribute('href') not in links: 
                    links.append(a.get_attribute('href'))
                else:
                    pass
            # scroll down for each job element
            driver.execute_script("arguments[0].scrollIntoView();", job)
        
        print(f'Collecting the links in the page: {page-1}')
        # go to next page:
        driver.find_element("xpath",f"//button[@aria-label='Page {page}']").click()
        time.sleep(3)
except Exception as e:
    print(e)
print('Found ' + str(len(links)) + ' links for job offers')

# Create empty lists to store information
job_titles = []
company_names = []
company_locations = []
work_methods = []
post_dates = []
work_times = [] 
job_desc = []
#skills=[]

i = 0
j = 1
# Visit each link one by one to scrape the information
print('Visiting the links and collecting information just started.')
for i in range(len(links)):
    try:
        driver.get(links[i])
        i=i+1
        time.sleep(2)
        # Click See more.
        driver.find_element(By.CLASS_NAME,"artdeco-card__actions").click()
        time.sleep(2)
    except:
        pass
    
    # Find the general information of the job offers
    contents = driver.find_elements(By.CLASS_NAME,'p5')
    for content in contents:
        try:
            job_titles.append(content.find_element(By.TAG_NAME,"h1").text)
            company_names.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__company-name").text)
            company_locations.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__bullet").text)
            work_methods.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__workplace-type").text)
            post_dates.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__posted-date").text)
            work_times.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__job-insight").text)
            #driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[2]/ul/div/button').click()
            #skills.append(content.find_element(By.CLASS_NAME,'job-details-skill-match-status-list').text)
            print(f'Scraping the Job Offer {j} DONE.')
            j+= 1
            
        except Exception as e:
            print(e)
            
        time.sleep(2)
        
        # Scraping the job description
    job_description = driver.find_elements(By.CLASS_NAME,'jobs-description__content')
    for description in job_description:
        job_text = description.find_element(By.CLASS_NAME,"jobs-box__html-content").text
        job_desc.append(job_text)
        print(f'Scraping the Job Offer {j}')
        time.sleep(2)  
            
# Creating the dataframe 
df = pd.DataFrame(list(zip(job_titles,company_names,
                    company_locations,work_methods,
                    post_dates,work_times,job_desc)),
                    columns =['job_title', 'company_name',
                           'company_location','work_method',
                           'post_date','work_time','job_desc'])

# Storing the data to csv file
df.to_csv('job_offers.csv', index=False)

# Output job descriptions to txt file
with open('job_descriptions.txt', 'w',encoding="utf-8") as f:
    for line in job_desc:
        f.write(line)
        f.write('\n')