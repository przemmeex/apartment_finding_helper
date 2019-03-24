# -*- coding: utf-8 -*-
from datetime import datetime

CITY = "wroclaw"
# CITY = "gdansk"
DEBUG_MODE = True
SHOW_LABELS = True
SAVE_DATA = True
SEARCH_MOR = True
PRICE_UPPER_LIMIT = 750000
AREA_UPPER_LIMIT = 120
SEARCHING_DEPTH = 4
OFFLINE_DATA = ""
SAVE_NAME = "apartments_data_{}_{}.json".format(datetime.now().timetuple().tm_yday,
                                                datetime.now().strftime("%H_%M"))

location_rate_w = {"dolnośląskie": 5, "grabiszynek": 75, "krzyki": 70, "śródmieście": 100,
                   "centrum": 100, "lipa piotrowska": 10, "sępolno": 55, "gaj": 80, "ołbin": 75,
                   "kleczków": 70, "wojnów": 20, "popowice": 80, "stare miasto": 100,
                   "osobowice": 75, "bieńkowice": 10, "muchobór mały": 65, "pilczyce": 70,
                   "fabryczna": 75, "grabiszyn": 85, "zacisze": 90, "borek": 85, "kłokoczyce": 5,
                   "gądów mały": 75, "księże wielkie": 60, "księże małe": 65, "jagodno": 45,
                   "oporów": 55, "klecina": 55, "poświętne": 40, "nowy dwór": 70, "partynice": 60,
                   "maślice": 65, "psie pole": 35, "karłowice": 45, "tarnogaj": 65, "złotniki": 50,
                   "stabłowice": 45, "żerniki": 45, "szczepin": 90, "biskupin": 85, "brochów": 30,
                   "swojczyce": 40, "kowale": 40, "plac grunwaldzki": 95, "sołtysowice": 35,
                   "ołtaszyn": 55, "huby": 85, "muchobór wielki": 65, "zakrzów": 10, "wojszyce": 45,
                   "rynek": 100, "kuźniki": 55, "leśnica": 20, "kozanów": 70, "różanka": 60,
                   "południe": 15, "nadodrze": 80, "os. psie pole": 35}

location_rate_g = {"śródmieście": 100, "wrzeszcz": 100, "oliwa": 85, "przymorze": 90,
                   "stare miasto": 100, "chełm": 55, "brętowo": 65, "ujeścisko": 45, "brzeźno": 80,
                   "osowa": 85, "morena": 80, "stogi": 40, "sobieszowo": 30, "pomorskie": 10,
                   "matemblewo": 55, "jasień": 45, "aniołki": 75, "niedżwiednik": 50,
                   "łostowice": 35, "zaspa": 70, "nowy port": 40, "jelitkowo": 85, "żabianka": 70,
                   "karczemki kiełpińskie": 30}

location_mapper = {"wroclaw": location_rate_w, "gdansk": location_rate_g}
name_to_utf = {"gdansk": "Gdańsk", "wroclaw": "Wrocław"}
