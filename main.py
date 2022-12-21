from indeed import extract_indeed_jobs

keyword = input("job title")
jobs = extract_indeed_jobs(keyword)
for job in jobs:
    print(job)
