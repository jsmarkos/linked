from selenium import webdriver
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

# LINKS

# HOMEPAGE_URL = 'https://www.linkedin.com'
# LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'
# CONNECTIONS_URL = 'https://www.linkedin.com/mynetwork/invite-connect/connections/'


query_keyword = "geomatic"
query_keyword_Education='"yıldız teknik üniversitesi"'
no_of_pages = 2
username = ""
password = ""

driver_path='/home/markos/İndirilenler/geckodriver-v0.28.0-linux64/geckodriver'
driver=webdriver.Firefox(executable_path=driver_path)
driver.get('https://www.linkedin.com/')

email_box = driver.find_element_by_id('session_key')
email_box.send_keys('e.birinnci@gmail.com')
pass_box = driver.find_element_by_id('session_password')
pass_box.send_keys('markos61')
submit_button = driver.find_element_by_class_name('sign-in-form__submit-button')
submit_button.click()

## text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view


## get profile name 
def getProfileName(page):
    profile_Name=page.find('ul', class_ ="pv-top-card--list inline-flex align-items-center")
    name_Profile=profile_Name.find('li', class_="inline t-24 t-black t-normal break-words").get_text(strip=True)
    name_Profile=str(name_Profile)
    
    for i in name_Profile:
        i=i.replace('>','')
        i=i.replace('</li','')
        i=i.split(",")
    return name_Profile


## get education
def getProfile_Education(page):
    
    profile_Education=page.find('div',class_="pv-entity__degree-info")
    education=profile_Education.find('h3','pv-entity__school-name t-16 t-black t-bold').get_text(strip=True)
    education=str(education)
    
    for i in education:
        i=i.replace('>','')
        i=i.replace('</h3','')
        i=i.split(",")
    return education


## get jobs
def getJobs(page):
    user_Jobs=page.find('section',class_="pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view")
    userProfileJobs=user_Jobs.find('p',"pv-entity__secondary-title t-14 t-black t-normal").get_text(strip=True)
    userProfileJobs=str(userProfileJobs)
    
    for i in userProfileJobs:
        i=i.replace('>','')
        i=i.replace('</p','')
        i=i.split(",")
        
    return userProfileJobs

## get projects
def getProjects(page):
    soup = page.find("section", class_="projects")
    soup = soup.find_all("span")
    soup = soup[1].string
    return soup

with open("Url_linked.txt" , "r") as f:
    urls = f.read().splitlines()

with open(".csv", "w") as file:
	file.write(
		"Profile name, Education, Jobs, received, "
		"No. of Projects\n"
	)
for i, soup in enumerate(tqdm(urls)):
    driver.get(soup)
    scheight = .1
    while scheight < 20:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight/%s);"
            % scheight
        )
        scheight += .01

    try:
        arrow = driver.find_element_by_css_selector(
            'button.pv-profile-section'
            '__see-more-inline'
        )
        arrow.click()
    except Exception as e:
        print(e)
    try:
        arrow = driver.find_element_by_css_selector(
            'button.pv-skills-section'
            '__additional-skills'
        )
        arrow.click()
        time.sleep(1)
    except Exception as e:
        print(e)

    page = BeautifulSoup(driver.page_source, 'lxml')

    row = ''


        # Profile Name

    try:
        profileName_ = getProfileName(page)
        print("Profile Name: ", profileName_)
    except Exception as e:
        print("Profile Name: ", "not found profile name")


        # Education

    try:
        education_ = getProfile_Education(page)
        print("Education: ", education_)
    except Exception as e:
        print("Education: ", "not found education!")
        
    
        # Jobs
    try:
        jobs_ = getJobs(page)
        print("Jobs: ", jobs_)
    except Exception as e:
        print("Jobs: ", "not found job!")
        
      
        
    # Projects
    try:
        project_ = getProjects(page)
        print("Projects: ", project_)
    except Exception as e:
        print("Projects: ", "not found project!")


    print()
    print()
    with open(".csv", "a") as file:
        file.write(row + '\n')
