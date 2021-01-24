import requests
from bs4 import BeautifulSoup


def fetch(url, number_of_pages):
    """Gets the blog post based on the number_of_pages(max 100) and returns as array of dictionary

    Parameters
    ----------
    url : str
        The url of the blog page
    number_of_pages : int, optional
        Number of pages to fetch from the blog

    Returns
    -------
    lines
        Array of blog post properties
    """
    lines = []
    if number_of_pages > 100:
        number_of_pages = 100

    try:
        for i in range(1, number_of_pages + 1):
            r = requests.get(str(url) + '/page/'+str(i))
            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.content, 'html.parser')

            articles = soup.findAll("article")
            for article in articles:
                childHead = ""
                childBody = ""
                link = ""
                entryTitle = article.find(class_="entry-title")
                if entryTitle is not None:
                    childHead = entryTitle.contents[0].get_text()
                    link = entryTitle.contents[0].get("href")

                entryContent = article.find(class_="entry-content")
                if entryContent is not None:
                    childBody = entryContent.p.get_text()

                if childHead != "" or childBody != "":
                    row = {"link": link, "title": childHead,
                           "summary": childBody}
                    lines.append(row)
    except:
        lines = None

    return lines


def get_query_url(base_url, site_url, number_of_pages):
    """Gets the query url for the seached blog

    Parameters
    ----------
    base_url : str
        The base url of the site
    site_url : str
        The blog post url
    number_of_pages : int
        Number of pages to fetch from the blog

    Returns
    -------
    query_url
        URL in the format "[base_url]?url=[site_url]&pages=[number_of_pages]"
    """
    return base_url + "?url=" + \
        site_url+"&pages="+str(number_of_pages)
