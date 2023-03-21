from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import re

url = "https://hk.investing.com/economic-calendar/cpi-733"

def truncate_unwanted_date(date):
    date = re.sub('[^0-9]','/', date)
    indices = [x for x, v in enumerate(date) if v == '/']
    date = date[0:indices[1]]

    return date

def scrape_to_csv():
    # load webpage
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    driver = webdriver.Chrome(desired_capabilities=caps)
    driver.get(url)

    # expand the table fully
    expand_button = driver.find_element_by_id("showMoreHistory733")
    while True:
        try:
            expand_button.click()
            time.sleep(0.05)
        except Exception as e:
            print(e)
            break

    # copy the wanted data
    table = driver.find_element_by_tag_name("tbody")
    rows = table.find_elements_by_tag_name("tr")
    for i in range(0, len(rows)):
        date = rows[i].find_element_by_class_name("left").text
        percentage = rows[i].find_element_by_class_name("noWrap").text
        date = truncate_unwanted_date(date)
        rows[i] = date + "," + percentage + "\n"

    driver.quit()

    # export csv file
    with open("output.csv", "w") as output:
        for i in rows:
            output.write(i)

def main():
    scrape_to_csv()

if __name__ == "main":
    main()