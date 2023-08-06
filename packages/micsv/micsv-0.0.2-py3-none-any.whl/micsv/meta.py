import os, urllib
from bs4 import BeautifulSoup
import csv, pandas, re, time

def is_login(driver):
    return(driver.current_url == target_url)
