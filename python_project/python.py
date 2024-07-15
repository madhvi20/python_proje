import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website
base_url = "https://hprera.nic.in/PublicDashboard"
projects_url = "https://hprera.nic.in/PublicDashboard"

# Function to get the HTML content of a page
def get_html(url):
    response = requests.get(url)
    return response.content

# Function to get project details from a detail page
def get_project_details(detail_url):
    html = get_html(detail_url)
    soup = BeautifulSoup(html, 'html.parser')
    
    details = {}
    details['GSTIN No'] = soup.find('td', text='GSTIN No').find_next_sibling('td').text.strip()
    details['PAN No'] = soup.find('td', text='PAN No').find_next_sibling('td').text.strip()
    details['Name'] = soup.find('td', text='Name').find_next_sibling('td').text.strip()
    details['Permanent Address'] = soup.find('td', text='Permanent Address').find_next_sibling('td').text.strip()
    
    return details

# Function to get the first 6 project links
def get_first_6_projects():
    html = get_html(projects_url)
    soup = BeautifulSoup(html, 'html.parser')
    
    project_links = []
    for link in soup.select('a[href^="/ProjectDetails"]')[:6]:
        project_links.append("https://hprera.nic.in" + link['href'])
    
    return project_links

# Main script
if __name__ == "__main__":
    project_links = get_first_6_projects()
    project_details_list = []
    
    for project_link in project_links:
        details = get_project_details(project_link)
        project_details_list.append(details)
    
    # Creating a DataFrame to display the scraped data
    df = pd.DataFrame(project_details_list)
    print(df)
