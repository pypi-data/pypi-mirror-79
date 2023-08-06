import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import download as dl

def run_mics(versions = [], overwrite = False, save_to = ".", sleep = 5):
    
    login_url = "https://mics.unicef.org/visitors/sign-in"
    target_url = "https://mics.unicef.org/surveys"
    def is_login(driver):
        return(driver.current_url == target_url)

    br = webdriver.Firefox()
    br.get(login_url)
    WebDriverWait(br,timeout=300).until(is_login) # reCaptcha is hard to solve man
    time.sleep(sleep)
    
    links = dl.get_links(br, versions, sleep)
    dl.download(links, overwrite, save_to)
    br.quit()
    print("Finished!")