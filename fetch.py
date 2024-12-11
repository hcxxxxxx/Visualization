import requests
from bs4 import BeautifulSoup
import json
import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
root = 'https://github.com/'
driver = webdriver.Safari()

repos = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

def get_person(i, followers='%2A'):
    path = "https://github.com/search?p={}&o=desc&q=followers%3A1..{}&s=followers&type=Users".format(i, followers)
    print(path)
    res = requests.get(path, headers=headers,
                       timeout=10)
    users = BeautifulSoup(res.content, "html5lib").select(".flszRz")
    for i, user in enumerate(users):
        links = user.select("a")
        name = links[1].getText().strip()

        if name == 'Follow':
            continue

        try:
            loc = user.select_one(".iyzdzM").getText().strip()
        except AttributeError:
            loc = None

        url = root + name
        
        print(url)
        det = BeautifulSoup(requests.get(
            url, headers=headers, timeout=10).content, "html5lib")
        card = det.select_one(".h-card")

        driver.get(url)

        try:
            element1 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "js-yearly-contributions"))
            )
            element2 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "year-link-2024"))
            )
            # print("元素已加载！")
            if element1 and element2:
                print("元素已加载！")

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            join_date_element = soup.select_one(".d-none.d-lg-block")
            if join_date_element:
                join_date_text = join_date_element.getText().strip()
                years = re.findall(r"\b\d{4}\b", join_date_text)
                join_date = years[-1]
                print(join_date)
            else:
                join_date = None
            contributions_element = soup.select_one(".js-yearly-contributions .position-relative h2.f4.text-normal.mb-2")
            if contributions_element:
                contributions_text = contributions_element.getText().strip()
                contributions = ''.join(filter(str.isdigit, contributions_text))
                # print(contributions)
            else:
                contributions = None
        except TimeoutException:
            contributions = None
            join_date = None
            print("TimeoutException")

        # not a personal repository
        if not card:
            return
        followers = card.select_one(
            "a.Link--secondary.no-underline.no-wrap>span").getText().strip()
        print(followers)
        
        try:
            if card.select_one(".p-org"):
                org = card.select_one(".p-org>div").getText().strip()
            elif card.select_one(".p-label"):
                org = card.select_one(".p-label").getText().strip()
            else:
                org = None
        except AttributeError:
            org = None
       
        try:
            repo_num =  det.select(
                ".UnderlineNav-body a")[1].select_one(".Counter").getText().strip()
        except AttributeError:
            repo_num = None

        try:
            stars = det.select_one("a[href$='?tab=stars'] .Counter").getText().strip()
        except AttributeError:
            stars = None

        try:
            languages = list(set(lang.getText().strip() for lang in det.select(".pinned-item-list-item .mb-0 .d-inline-block")))
        except AttributeError:
            languages = []

        is_pro = bool(det.select_one(".Label--secondary"))
        
        repo = {'name': name, 'loc': loc,
                'url': url, 'followers': followers, 'org': org,
                'repo_num': repo_num, 'stars': stars,
                'languages': languages, 'is_pro': is_pro,
                'join_date': join_date,
                'contributions_in_2024': contributions}
        repos.append(repo)
        write()


def write():
    with open('./person_data_top200.json', 'w', newline='\n') as file_object:
        json.dump(repos, file_object, indent=4)


if __name__ == "__main__":
    start = time.time()
    for i in range(1,500):
        get_person(i)
    end = time.time()
    print(end-start)
