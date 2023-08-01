import requests

from bs4 import BeautifulSoup as bs4

# TODO should refactor to use main function like in ext-stats.py


def separate_contracts(futures: str) -> list:
    response = requests.get(futures).content
    soup = bs4(response, "html.parser")
    body = soup.find("body").text.strip()
    chunks = body.split("\r\n \r\n \r\n")
    return chunks


futures = "https://www.cftc.gov/dea/futures/deanymesf.htm"
chunks = separate_contracts(futures)

print("contract,open_interest")
for chunk in chunks:
    name = chunk.split(" - NEW YORK MERCANTILE EXCHANGE")[0]
    open_interest = chunk.split("OPEN INTEREST:")[1].split("\r")[0].strip()
    open_interest = open_interest.replace(",", "")
    print(name + "," + open_interest)
