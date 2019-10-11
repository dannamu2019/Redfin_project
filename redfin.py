from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time
import pandas as pd
import numpy as np

driver = webdriver.Chrome()

df_zipcode = pd.read_csv('./zipcode/zipcode.csv', dtype={'zipcode':str})
urls = ["https://www.redfin.com/zipcode/" + zipcode for zipcode in df_zipcode.zipcode]
zipped = list(zip(df_zipcode.zipcode, urls))
csv_file = open('redfin.csv', 'w', encoding='utf-8',newline='')
writer = csv.writer(csv_file)
writer.writerow(['zipcode', 'med_list_price','avg_sale','med_list_per_sqft',\
    'avg_num_offers','med_sale_price','avg_down_payment','med_sale_per_sqft','num_sold',\
    'ele_school_mean','mid_school_mean','high_school_mean'])

for zipcode, url in zipped:
    # Go to page 
    driver.get(url)
    print('on page:', url)

    # Grab data
    keys = driver.find_elements_by_xpath('//span[@class="label"]')
    values = driver.find_elements_by_xpath('//span[@class="value"]/span')
    values = [e.text for e in values]
    keys = [e.text for e in keys]
    value_dict = dict(zip(keys,values))

    elementary_ratings = driver.find_elements_by_xpath('//div[@class="rating"]')
    elementary_ratings = [e.text for e in elementary_ratings]

    # handle errors
    # use re match to filter list for only digits

    good_data = []
    for e in elementary_ratings:
        try:
            e = int(e)
            good_data.append(e)
        except:
            pass

    elementary_mean = np.mean(good_data)

    print(elementary_mean)

    button = driver.find_element_by_xpath('//button[@class="schoolTab medium unpadded pill-center middle-tab clickable button-text"]')
    button.click()

    middle_ratings = driver.find_elements_by_xpath('//div[@class="rating"]')
    middle_ratings = [e.text for e in middle_ratings]

    good_data=[]
    for e in middle_ratings:
        try:
            e = int(e)
            good_data.append(e)
        except:
            pass


    middle_mean = np.mean(good_data)

    time.sleep(.5)

    button = driver.find_element_by_xpath('//button[@class="schoolTab medium unpadded pill-right last-tab clickable button-text"]')
    button.click()


    high_ratings = driver.find_elements_by_xpath('//div[@class="rating"]')
    high_ratings = [e.text for e in high_ratings]

    good_data=[]
    for e in high_ratings:
        try:
            e = int(e)
            good_data.append(e)
        except:
            pass            

    high_mean = np.mean(good_data)
    

    # Write to csv
    data_dict = {}
    data_dict['zipcode'] = zipcode
    data_dict.update(value_dict)
    data_dict['elementary_mean'] = elementary_mean
    data_dict['middle_mean'] = middle_mean
    data_dict['high_mean'] = high_mean

    writer.writerow(data_dict.values())


csv_file.close()
driver.close()



    