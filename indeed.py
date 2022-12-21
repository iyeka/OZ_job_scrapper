from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_page_count(keyword):
    base_url = f"https://au.indeed.com/jobs?q={keyword}"

    # option to be kept open
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options)
    driver.get(base_url)
    response = driver.page_source

    soup = BeautifulSoup(response, "html.parser")
    pages = soup.find_all('a', class_="css-e9oyys")
    if pages == None:
        return 1
    return len(pages)+1


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    results = []
    for page in range(pages):
        url = f"https://au.indeed.com/jobs?q={keyword}&start={page*10}"
        print("requesting", url)
        # option to be kept open
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options)
        driver.get(url)
        response = driver.page_source
        soup = BeautifulSoup(response, "html.parser")

        job_list = soup.find('ul', class_="jobsearch-ResultsList")
        if job_list:
            jobs = job_list.find_all('li', recursive=False)
            for job in jobs:
                mosaic_zone = job.find('div', class_="mosaic-zone")
                if mosaic_zone == None:
                    anchor = job.select_one('h2 a')
                    link = anchor['href']
                    span = anchor.find('span')
                    title = span['title']
                    company = job.find('span', class_="companyName")
                    location = job.find('div', class_="companyLocation")
                    print(type(location))
                    if location:
                        location = location.string.replace(",", "")
                    # salary = job.find('div', class_="salary-snippet-container")
                    # salary = salary.string.replace(",", "") if salary else None
                    job_data = {
                        'link': f"https://au.indeed.com{link}",
                        'company': company.string.replace(",", ""),
                        'location': location,
                        'position': title.replace(",", ""),
                        # 'pay': salary
                    }
                    results.append(job_data)
        else:
            pass
        driver.close()
    return results
