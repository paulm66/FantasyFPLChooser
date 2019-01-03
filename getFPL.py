import requests

def saveSite(url, filename):
    page = requests.get(url)
    open(filename, 'wb').write(page.content)
