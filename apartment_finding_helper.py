# -*- coding: utf-8 -*-
import json
import re
from mpl_toolkits.mplot3d import Axes3D
from const import *
from apartment_morizon import mor_prepare_data

import bs4
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import requests

location_rate = location_mapper[CITY]

main_url = "https://www.otodom.pl/sprzedaz/mieszkanie/{}/".format(CITY)


def del_duplicates_and_merge(lists_A, lists_B):
    v, x, y, z = [], [], [], []
    for i in range(len(lists_A[0])):
        dup = False
        for j in range(len(lists_B[0])):
            if (lists_A[0][i] == lists_B[0][j] and lists_A[1][i] == lists_B[1][j] and
                    lists_A[2][i] == lists_B[2][j]):
                dup = True
        if not dup:
            v.append(lists_A[0][i])
            x.append(lists_A[1][i])
            y.append(lists_A[2][i])
            z.append(lists_A[3][i])
        elif DEBUG_MODE:
            print("Duplicated result: {}".format(
                (lists_A[0][i], lists_A[1][i], lists_A[2][i], lists_A[3][i])))

    v += lists_B[0]
    x += lists_B[1]
    y += lists_B[2]
    z += lists_B[3]
    return v, x, y, z


def prepare_data():
    if not OFFLINE_DATA:
        prices, locations, areas, links = [], [], [], []
        for i in range(1, SEARCHING_DEPTH):
            handler = requests.get(main_url, params={"page": str(i)})
            soup = bs4.BeautifulSoup(handler.text, 'lxml')
            divs = soup.find_all("div", {"class": "offer-item-details"})
            price_re_pattern = r"(\d{1} )?\d{2,3} \d{3} zł"
            location_pattern = "({}, )(.*)".format(name_to_utf[CITY])

            area_pattern = r"\d{2,3}\.\d{1,2}|\d{2,3}"

            for div in divs:
                link_url = div.find('a')['href']
                price_match = re.search(price_re_pattern,
                                        div.find("li", {"class": "offer-item-price"}).getText())

                location_match = re.search(location_pattern,
                                           div.find("p",
                                                    {"class": "text-nowrap hidden-xs"}).getText(),
                                           re.IGNORECASE)
                raw_area = div.find("li", {"class": "hidden-xs offer-item-area"}).getText()

                area_range = re.findall(area_pattern, raw_area.replace(",", "."))

                if location_match and price_match and area_range:
                    locations.append(location_rate.get(location_match.group(2).lower(), 1))
                    if locations[-1] == 1:
                        print(location_match.group(2))
                    if len(area_range) == 2:
                        areas.append(int((float(area_range[0]) + float(area_range[1])) / 2))
                    else:
                        areas.append(int(float(area_range[0])))
                    areas[-1] = areas[-1] if areas[-1] < AREA_UPPER_LIMIT else AREA_UPPER_LIMIT
                    price_int = int("".join(price_match.group(0)[:-3].split()))
                    prices.append(price_int) if price_int < PRICE_UPPER_LIMIT else prices.append(
                        PRICE_UPPER_LIMIT)
                    links.append(link_url)
        if SEARCH_MOR:
            m_p, m_lo, m_a, m_li = mor_prepare_data()
            prices, locations, areas, links = \
                del_duplicates_and_merge([m_p, m_lo, m_a, m_li], [prices, locations, areas, links])

    else:
        with open(OFFLINE_DATA) as data_file:
            data_loaded = json.load(data_file)

        prices, locations, areas, links = data_loaded["prices"], data_loaded["locations"], \
                                          data_loaded["areas"], data_loaded["links"]

    if SAVE_DATA and not OFFLINE_DATA:
        with open(SAVE_NAME, "w") as file_handler:
            json.dump({"prices": prices, "locations": locations, "areas": areas, "links": links},
                      file_handler, ensure_ascii=False)
    if DEBUG_MODE:
        print(len(prices))
        print(prices, locations, areas, links)

    for i, lnk in enumerate(links, 1):
        print(i, lnk)
    return areas, locations, prices


def plot_chart(areas, locations, prices):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # ax.scatter(areas, locations, prices, c=prices, cmap='viridis', linewidth=0.5)
    ax.plot_trisurf(areas, locations, prices, linewidth=0.2, antialiased=True, cmap=plt.cm.CMRmap)
    if SHOW_LABELS:
        for i in range(len(prices)):
            raw_text = ax.text(areas[i], locations[i], prices[i], i + 1, size=6, color='white')
            raw_text.set_path_effects([path_effects.Stroke(linewidth=1, foreground='black'),
                                       path_effects.Normal()])

    ax.set_xlim(10, 120)
    ax.set_ylim(100, 0)
    ax.set_zlim(0, 750000)
    ax.set_xlabel('area [m2]')
    ax.set_ylabel('location [a. u.]')
    ax.set_zlabel('prices [PLN]')

    plt.show()


if __name__ == '__main__':
    x, y, z = prepare_data()
    plot_chart(x, y, z)
