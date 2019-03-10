import json
import re
from mpl_toolkits.mplot3d import Axes3D
import bs4
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import requests


CITY = "wroclaw"
DEBUG_MODE = True
SHOW_LABELS = True
SAVE_DATA = True
USE_OFFLINE = False
SAVE_NAME = "apartments_data.json"

location_rate = {"dolnośląskie": 5, "grabiszynek": 75, "krzyki": 70, "śródmieście": 100,
                   "centrum": 100, "lipa piotrowska": 10, "sępolno": 55, "gaj": 80, "ołbin": 75,
                   "kleczków": 70, "wojnów": 20, "popowice": 80, "stare miasto": 100,
                   "bieńkowice": 10, "muchobór mały":65, "pilczyce":70,"południe":15,
                   "fabryczna": 75, "grabiszyn": 85, "zacisze": 90, "borek": 85, "kłokoczyce": 5,
                   "gądów mały": 75, "księże wielkie": 60, "księże małe": 65, "jagodno": 45,
                   "oporów": 55, "klecina": 55, "poświętne": 40, "nowy dwór": 70, "partynice": 60,
                   "maślice": 65, "psie pole": 35, "karłowice": 45, "tarnogaj": 65, "złotniki": 50,
                   "stabłowice": 45, "żerniki": 45, "szczepin": 90, "biskupin": 85, "brochów": 30,
                   "swojczyce": 40, "kowale": 40, "plac grunwaldzki": 95, "sołtysowice": 35,
                   "ołtaszyn": 55, "huby": 85, "muchobór wielki":65, "zakrzów":10, "wojszyce": 45}

main_url = "https://www.otodom.pl/sprzedaz/mieszkanie/{}/".format(CITY)


def prepare_data():
    if not USE_OFFLINE:
        prices, locations, areas, links = [], [], [], []
        for i in range(1, 10):
            handler = requests.get(main_url, params={"page": str(i)})
            soup = bs4.BeautifulSoup(handler.text, 'lxml')
            # print(soup)
            divs = soup.find_all("div", {"class": "offer-item-details"})
            price_re_pattern = r"(\d{1} )?\d{2,3} \d{3} zł"
            location_pattern = r"(Wrocław, )(.*)"
            area_pattern = r"\d{2,3}\.\d{1,2}|\d{2,3}"

            for div in divs:
                link_url = div.find('a')['href']
                price_match = re.search(price_re_pattern,
                                        div.find("li", {"class": "offer-item-price"}).getText())

                location_match = re.search(location_pattern,
                                           div.find("p", {"class": "text-nowrap hidden-xs"}).getText(),
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
                    price_int = int("".join(price_match.group(0)[:-3].split()))
                    prices.append(price_int) if price_int < 750000 else prices.append(750000)
                    links.append(link_url)
    else:
        with open(SAVE_NAME) as data_file:
            data_loaded = json.load(data_file)

        prices, locations, areas, links = data_loaded["prices"], data_loaded["locations"], \
                                          data_loaded["areas"], data_loaded["links"]

    if SAVE_DATA and not USE_OFFLINE:
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