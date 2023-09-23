from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

FORMS_LINK = "https://forms.gle/1s8oPpTmC6d87rmm8"

header = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0',
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}

response = requests.get(
    "https://krisha.kz/arenda/kvartiry/astana/?das[live.rooms][]=1&das[live.rooms][]=2&das[price][to]=200000&areas=p51.115945,71.416980,51.117674,71.400673,51.111515,71.395351,51.097574,71.388313,51.081358,71.385910,51.076275,71.386940,51.069678,71.400158,51.068272,71.407539,51.069354,71.422302,51.071301,71.426937,51.074329,71.430542,51.089466,71.437236,51.097141,71.439125,51.106004,71.439296,51.112812,71.437236,51.116594,71.433460,51.118754,71.421615,51.118106,71.402561,51.115945,71.416980&zoom=13&lat=51.09352&lon=71.41260",
    headers=header)
data = response.text
soup = BeautifulSoup(data, "html.parser")

# ADDRESSES
address_elements = soup.select("div.a-card__subtitle")
all_addresses = []
for address in address_elements:
    all_addresses.append(address.get_text().strip())

# LINKS
link_elements = soup.find_all(name="a", class_="a-card__title")
all_links = []
for tag in link_elements:
    link = f'https://krisha.kz{tag.get("href")}'
    all_links.append(link)

# PRICES
price_elements = soup.select("div.a-card__price")
all_prices = []
for price in price_elements:
    formatted_price = price.get_text().replace("&nbsp", "").split()[0] + price.get_text().replace("&nbsp", "").split()[
        1]
    all_prices.append(formatted_price.strip())

driver = webdriver.Chrome()
for n in range(len(all_links)):
    driver.get(FORMS_LINK)
    time.sleep(2)

    form_address = driver.find_element(By.XPATH,
                                       '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_price = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_links = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    form_address.send_keys(all_addresses[n])
    form_price.send_keys(all_prices[n])
    form_links.send_keys(all_links[n])
    submit_button.click()
