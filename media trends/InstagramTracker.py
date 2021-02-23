"""Progam to locally save the total posts from a certain Instagram hashtag"""
import bs4
from selenium import webdriver
import csv
from datetime import datetime as dt
from datetime import timedelta
import time

filename = 'instagramstats.csv'
yesterday = dt.today() - timedelta(days=1)
log_time = yesterday.strftime("%Y-%m-%d")

def get_count(pages):
    #Open chrome and go to Instagram
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    driver.get('https://www.instagram.com/')
    time.sleep(5)
    #Enter credenitals and click login
    driver.find_element_by_name('username').send_keys('USERNAME')
    driver.find_element_by_name('password').send_keys('PASSWORD')
    driver.find_element_by_css_selector(".y3zKF:not(.yWX7d)").click()
    time.sleep(3)
    totals = []
    num = 1
    #Loop through hashtag pages and save total post count
    for i in pages:
        driver.get(i)
        soup = bs4.BeautifulSoup(driver.page_source, features="html.parser")
        count = soup.find("span", attrs={"class": "g47SY"})
        number = int(count.text.replace(',', ''))
        totals.append(number)
        driver.save_screenshot(
            'FILE_PATH/' + log_time + '(' + str(num) + ')' + '.png')
        num += 1
    driver.quit()
    return totals

def log(totals):
    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([log_time, '#Blacklivesmatter', totals[0]])
        csvwriter.writerow([log_time, '#BLM', totals[1]])
        csvwriter.writerow([log_time, 'BLM combined', totals[0] + totals[1]])
        csvwriter.writerow([log_time, '#GeorgeFloyd', totals[2]])
        csvwriter.writerow([log_time, '#Protest', totals[3]])
        csvwriter.writerow([log_time, '#Defundthepolice', totals[4]])
        day_total = totals[0] + totals[1] + totals[2] + totals[3] + totals[4]
        csvwriter.writerow([log_time, '#TOTAL', day_total])
    print('Logged at ' + log_time)

def main():
    pages = ['https://www.instagram.com/explore/tags/blacklivesmatter/', 'https://www.instagram.com/explore/tags/blm/',
             'https://www.instagram.com/explore/tags/georgefloyd/', 'https://www.instagram.com/explore/tags/protest/',
             'https://www.instagram.com/explore/tags/defundthepolice/'
             ]
    totals = get_count(pages)
    log(totals)
    
if __name__ == "__main__":
    print('Running')
    main()
