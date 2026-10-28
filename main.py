import requests
from bs4 import BeautifulSoup
import json
import csv
import os


url = "https://realpython.github.io/fake-jobs/"

def fetch_job(url):

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an error for bad status codes

        print("Request successful")
        

    except requests.exceptions.Timeout:
        print("The request took too long")
        return []

    except requests.exceptions.ConnectionError:
        print("Could not connect to the server, check your internet connection.")
        return []

    except requests.exceptions.HTTPError as error:
        print(f"HTTP error occurred: {error}")
        return []

    except requests.exceptions.RequestException as error:
        print(f"Something went wrong: {error}")
        return []
        

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("div", class_="card-content")

    job_list = []

    for job in jobs:
        title_element = job.find("h2", class_="title")

        title = title_element.text.strip() if title_element else ""

        company = job.find("h3", class_="company").text.strip()

        if not company:
            company = ""

        location = job.find("p", class_="location").text.strip()

        if not location:
            location = ""

        # Get job detail URL
        link_element = job.find("a")

        link = link_element["href"] if link_element else ""

        job_list.append(
            {
            "title":title,
            "company": company,
            "location": location,
            "url": link
            }
        
        )
    return job_list


result = fetch_job(url)


def save_list(result):
    
    os.makedirs("data", exist_ok=True)

    
    with open("data/job_list.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["title", "company", "location", "url"]
        )

        writer.writeheader()
        writer.writerows(result)

if result:
    save_list(result)
else:
    print("No jobs found")

