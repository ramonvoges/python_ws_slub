from urllib.request import urlopen
from bs4 import BeautifulSoup as soup


def load_xml(path):
    with open(path) as f:
        xml = f.read()
        xml_soup = soup(xml, "lxml")
        return xml_soup


def find_records(path):
    records = load_xml(path).find_all('record')
    for record in records:
        yield record


def find_places(path):
    places = load_xml(path).find_all('mods:placeterm', {'type': 'text'})
    for place in places:
        place = place.get_text().strip().replace("[", "").replace("]", "")
        yield place


def find_titles(path):
    records = []
    for record in find_records(path):
        #print(record)
        slub_id = record.find("slub:id").string.strip()
        #title = record.find('mods:title').get_text().strip()
        subtitle = record.find('mods:subtitle').get_text().strip()
        records.append((slub_id, subtitle))
    return records


def write_files(input_path):
    for record in find_records(input_path):
        slub_id = record.find("slub:id").string.strip()
        with open("./data/" + slub_id + ".mets", mode='a+') as f:
            f.write(record.prettify())


def count_places(path):
    places = {}
    for place in find_places(path):
        if place in places.keys():
            places[place] += 1
        else:
            places[place] = 1
    return places