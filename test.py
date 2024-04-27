from bs4 import BeautifulSoup
import requests

def basicScrape():
    # URL of Google's homepage
    url = 'https://www.google.com'

    # Sending a GET request to the URL
    response = requests.get(url)
    print(response)

    # Parsing the HTML content of the response
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)

    # Extracting the title of the page
    title = soup.title.string

    # Printing the title
    # print("Title of Google's homepage:", title)




if __name__ == '__main__':
    basicScrape()