from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json, time

def get_browser():
    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('log-level=3')
    browser = wd.Chrome(chrome_options=chrome_options)
    return browser

company_list = json.load(open("company_list.json"))

browser = get_browser()

url = {}
failed = []

scraped = 0
fail = 0

for company in company_list:
    company_cap = company.title()
    print(company_cap)
    browser.get("https://www.glassdoor.com/Reviews/index.htm")

    elem = browser.find_element_by_id("KeywordSearch")
    elem.send_keys(company_cap)
    elem.send_keys(Keys.RETURN)
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[1])
    try:
        elem = browser.find_element_by_link_text(company_cap)
        elem.send_keys(Keys.RETURN)
        url[company] = browser.current_url
        # browser.close()
        # browser.switch_to.window(browser.window_handles[0])
        # browser.close()
        print(company_cap + " added!")
        scraped += 1
    except:
        print(company_cap + " failed.")
        failed.append(company)
        fail += 1
        pass
    print("\nscraped: ", scraped, " failed: ", fail)

json.dump(url, open("url_dict.json", 'w'))
json.dump(failed, open("failed.json", 'w'))