from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import json


def scrape_small_page(url):
    result = {}
    page = urlopen(url).read()
    soup = BeautifulSoup(page,'html.parser')
    
    #get the title
    title = soup.find(itemprop="title").text
    result["Job Title"] = title
    
    #get the salary
    salary = soup.find(itemprop="baseSalary")
    salary = salary.find("a").text
    result["Salary"] = salary
    
    #get the category
    category = soup.find(itemprop="occupationalCategory")
    category = category.find("a").text
    result["Category"] = category
    
    #get the area
    address = soup.find(itemprop="address")
    address = address.find("a").text
    result["Area"] = address
    
    #get the education
    education = soup.find(itemprop="educationRequirements")
    if (education != None):
        result["Education"] = education.text
    
    #get the employment type
    employ = soup.find(itemprop="employmentType").text
    result["Employment type"] = employ
    
    return result

def scrape_big_page(url):
    page = urlopen(url).read()
    soup = BeautifulSoup(page,'html.parser')
    result = []
    
    #get all links
    links = soup.find_all(class_="media-heading h4")
    for link in links:
        link = link.find("a")['href']
        result.append(link)
    return result

url = 'https://www.loker.id/cari-lowongan-kerja'

data = []
for i in range(1,150):
    url_new = url + '/page/' + str(i)
    print("Scraping data from page " + str(i))
    for small_link in scrape_big_page(url_new):
        print("Getting data...")
        data.append(scrape_small_page(small_link))
    time.sleep(0.25)

print("Data has been extracted to data.json")

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)