"""
This module provides functions for downloading, saving and processing of
mets files.

Developed by André Wendler and Ramon Voges.

"""

import os

from glob import glob
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

#  import matplotlib.pyplot as plt
#  import cartopy.crs as ccrs

import plotly.offline as py
import plotly.graph_objs as go

#  import seaborn as sns
#  sns.set()


def download_xml(url, output_path):
    """
    Download xml file with mets-mods from given <url> and save each record
    to an individual file in <output_path>.
    """
    xml = urlopen(url)
    xml_soup = soup(xml, 'lxml')
    for record in xml_soup.find_all('record'):
        slub_id = record.find("slub:id").string.strip()
        if os.path.exists(output_path) != True:
            os.mkdir(output_path)
        with open("{}/{}.mets".format(output_path, slub_id), mode='w') as f:
            f.write(record.prettify())
            print("Saved record {} to {}.".format(slub_id, f.name))


# def load_xml(file):
#     """Read the XML <file> and return a Beautiful Soup object."""
#     with open(file) as f:
#         xml = f.read()
#         xml_soup = soup(xml, "lxml")
#         return xml_soup


def load_mets(path):
    """Load the files in <path> and provide a generator."""
    mets = glob(path)
    for file in mets:
        with open(file) as f:
            xml = f.read()
            xml_soup = soup(xml, "lxml")
            yield xml_soup


def find_records(path):
    """Find all records in the given mets files and provide a generator."""
    for mets in load_mets(path):
        records = mets.find_all('record')
        for record in records:
            yield record


def find_places(path):
    """Find all places in the given mets files and provide a generator."""
    for record in find_records(path):
        places = record.find_all('mods:placeterm', {'type': 'text'})
        for place in places:
            place = place.get_text().strip().replace("[", "").replace("]", "")
            yield place


def find_titles(path):
    """Find all titles in the given mets files in <path> and provide a generator."""
    for record in find_records(path):
        titles = [title.get_text().strip() for title in record.find_all('mods:title')]
        yield titles


def find_authors(path):
    """Find all authors in the given mets files in <path>, put them in a list and provide a generator."""
    for record in find_records(path):
        authors = [author.get_text().strip() for author in record.find_all('mods:displayform')]
        yield authors


def find_publishers(path):
    """Find all authors in the given mets files in <path>, put them in a list and provide a generator."""
    for record in find_records(path):
        publishers = [publisher.get_text().strip() for publisher in record.find_all('mods:publisher')]
        yield publishers


def find_issue_date(path):
    """Find all issue dates in the given mets files in <path> and provide a generator."""
    for record in find_records(path):
        try:
            date = record.find('mods:dateissued').get_text().strip()
        except:
            date = '[unbekannt]'
        yield date


def works(path):
    """Return a list with dictionaries for every work in the given mets files."""
    works = []
    for record in find_records(path):
        slub_id = record.find("slub:id").get_text().strip()
        authors = [author.get_text().strip() for author in record.find_all('mods:displayform')]
        titles = [title.get_text().strip() for title in record.find_all('mods:title')]
        publisher = [publisher.get_text().strip() for publisher in  record.find_all('mods:publisher')]
        places = [place.get_text().strip() for place in record.find_all('mods:placeterm', {'type': 'text'})]
        date = record.find('mods:dateissued').string.strip() if record.find('mods:dateissued') else '[unbekannt]'
        works.append({'id': slub_id, 'author': authors, 'title': titles, 'publisher': publisher,
                    'place': places, 'date issued': date})
    return works


def write_files(input_path, output_path):
    """Save the records in <input path> to separate files in ./data/."""
    for record in find_records(input_path):
        slub_id = record.find("slub:id").string.strip()
        if os.path.exists(output_path) == False:
            os.mkdir(output_path)
        with open("{}/{}.mets".format(output_path, slub_id), mode='a+') as f:
            f.write(record.prettify())
            print("Saved record {} to {}.".format(slub_id, f.name))


def count_places(path):
    """Count the places in the given mets files."""
    places = {}
    for place in find_places(path):
        if place in places.keys():
            places[place] += 1
        else:
            places[place] = 1
    return places


def plot_places(path):
    """Plot the places found in the given mets files in a bar chart."""
    cp = count_places(path)
    keys = list(cp.keys())
    values = list(cp.values())

    #  plt.xticks(range(len(keys)), keys, rotation='vertical')
    #  plt.bar(keys, values)

    bar_chart = go.Bar(x=keys, y=values)
    figures = [bar_chart]
    py.plot(figures, filename='places.html', auto_open=True)


def find_geo(path):
    """Geolocate the places found in the given mets files."""
    geolocator = Nominatim(user_agent='SLUB Scraper')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    locations = [geocode(place) for place in find_places(path)]
    return locations


def plot_geo(path):
    """Plot the places found in the given mets files on a map."""
    locations = find_geo(path)

    #  ax = plt.axes(projection=ccrs.PlateCarree())
    #  ax.coastlines(resolution='50m')
    #  for loc in locations:
    #      x = loc.longitude
    #      y = loc.latitude
    #      plt.scatter(x, y, transform=ccrs.PlateCarree())
    #      plt.text(x+0.3, y+0.3, loc.address)

    lat = [loc.latitude for loc in locations]
    lon = [loc.longitude for loc in locations]
    text = [loc.address for loc in locations]
    geo = go.Scattergeo(lat=lat, lon=lon, text=text)
    figures = [geo]
    #  layout = {'geo': {'scope': 'europe', 'showcountries': False, 'showcoastlines': True}}
    #  fig = go.Figure(data=data, layout=layout)
    #  py.plot(fig, filename='map.html', auto_open=True)
    py.plot(figures, filename='map.html', auto_open=True)

if __name__ == "__main__":
    download_xml('https://digital.slub-dresden.de/oai/?verb=ListRecords&metadataPrefix=mets&set=15th-century-prints', 'data')
    print('Die folgenden Titel wurden heruntergeladen: ')
    files = 'data/*.mets'
    print(works(files))
    plot_places(files)
    plot_geo(files)
