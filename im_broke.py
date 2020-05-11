import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import pandas as pd

# This is to disable the info bar.

options = Options()
options.add_argument("--disable-infobars")
options.add_experimental_option("prefs",{"profile.default_content_setting_values.notifications":1})

# Here we have the website we will scrape and the path of the installed chromedriver.

chromedriver = "/home/marina/im-broke-scrapy/chromedriver"
driver = webdriver.Chrome(chromedriver,chrome_options=options)
driver.get("http://www.thisiswhyimbroke.com")

# It is necessary to update the website to have the latest products.

time.sleep(3)   
driver.refresh()


# We create a data frame where we will where we will keep all the information.

df = pd.DataFrame()

# We will scrape the images first.

image_elements = driver.find_elements_by_css_selector('#view > div.row.full-width-grid.ng-scope > div > article:nth-child(n) > div.ng-scope > div.image > a > img')


row = 0

for image in image_elements:
    row += 1
    image= image.get_attribute('src')
    df.loc[row, 'image'] = image
    
# Now we are going to scrape the URL of the products.
    
url_elements = image_elements = driver.find_elements_by_css_selector('#view > div.row.full-width-grid.ng-scope > div > article:nth-child(n) > div.ng-scope > div.image > a')  



row = 0

for url in url_elements:
    row +=1
    url= url.get_attribute('href')
    df.loc[row, 'url'] = url
    
# We close the window.
         
driver.quit()

# Once we have our data frame, we need to change the URL column type from "object" to "string".

df['url'] = df.url.astype('string')

# These are the parameters of the affiliate program and we don't need them.

df['url'] = df.url.str.replace(r'/?tag=097-20&ascsubtag.*','')

# We will also replace the URL from amazon.com to amazon.fr

df['url'] = df.url.str.replace(r'amazon.com','amazon.fr')

# We download a csv with all the information.

df.to_csv('products.csv')