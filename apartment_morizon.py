# -*- coding: utf-8 -*-


from const import *
import bs4
import requests

location_rate = location_mapper[CITY]
main_url = "https://www.morizon.pl/mieszkania/{}/".format(CITY)


def mor_prepare_data():
    prices, locations, areas, links = [], [], [], []
    for i in range(1, SEARCHING_DEPTH):
        handler = requests.get(main_url, params={"page": str(i)})
        soup = bs4.BeautifulSoup(handler.text, 'lxml')
        heads = soup.find_all("header")
        once = True
        for head in heads:
            if head.find("meta", {"itemprop": "category"}) and once:

                raw_price = head.find("meta", {"itemprop": "price"})
                price = int(float(raw_price["content"]) if raw_price else "")

                raw_loc_list = head.find("h2",
                                         {"class": "single-result__title"}).getText().strip().split(
                    ", ")
                found = False
                for loc in raw_loc_list:
                    if location_mapper[CITY].get(loc.lower(), 0):
                        location = location_mapper[CITY][loc.lower()]

                        found = True
                        break
                if not found:
                    location = ""
                    if DEBUG_MODE:
                        print(raw_loc_list)

                raw_area = head.find("p", {
                    "class": "single-result__price single-result__price--currency"}).getText().strip().split()
                if price and location:
                    square_price = raw_area[0] if len(raw_area) == 2 else "".join(
                        (raw_area[0], raw_area[1]))

                    area = int(price / float(square_price.replace(",", ".")))
                    link_url = head.find('a')['href']

                if location and area and link_url:
                    prices.append(price) if price < PRICE_UPPER_LIMIT else prices.append(
                        PRICE_UPPER_LIMIT)
                    locations.append(location)
                    areas.append(area) if area < AREA_UPPER_LIMIT else areas.append(
                        AREA_UPPER_LIMIT)
                    links.append(link_url)

        return prices, locations, areas, links
