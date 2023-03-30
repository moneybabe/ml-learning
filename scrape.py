from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import re
from configparser import ConfigParser
import pymysql


class Scrape:

    def __init__(self, url):
        self.url = url

    def __truncate_unwanted_date(self, date):
        date = re.sub('[^0-9]','/', date)
        indices = [x for x, v in enumerate(date) if v == '/']
        date = date[0:indices[1]]

        return date

    def scrape(self):
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
        rows = driver.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        for i in range(0, len(rows)):
            date = rows[i].find_element_by_class_name("left").text
            percentage = rows[i].find_element_by_class_name("noWrap").text
            date = self.__truncate_unwanted_date(date)
            rows[i] = (date, percentage)

        driver.quit()
        rows.pop(0)

        return rows

    def export_to_csv(self, rows):
        # export csv file
        with open("data.csv", "w") as data:
            for i in rows:
                data.write(i[0] + ", " + i[1] + "\n")

    def export_to_mysql(self, rows):
        config = ConfigParser()
        config.read("mysql_config.txt")
        host = config.get("mysql", "host")    
        username = config.get("mysql", "username")
        password = config.get("mysql", "password")    
        database = config.get("mysql", "database")

        with pymysql.connect(host=host, user=username, password=password, db=database) as connection:
            cursor = connection.cursor()
            
            # drop table if exists
            cursor.execute("DROP TABLE IF EXISTS cpi;")

            # create table
            cursor.execute("CREATE TABLE cpi (date VARCHAR(10), percentage VARCHAR(10));")

            # insert data
            sql = "INSERT INTO cpi (date, percentage) VALUES (%s, %s);"
            cursor.executemany(sql, rows)

            # commit changes
            connection.commit()

            # confirm data
            assert cursor.rowcount == len(rows)

if __name__ == "__main__":
    url = "https://hk.investing.com/economic-calendar/cpi-733"
    web = Scrape(url)
    rows = web.scrape()
    web.export_to_csv(rows)
    web.export_to_mysql(rows)