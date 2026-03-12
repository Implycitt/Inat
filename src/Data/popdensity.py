'''
    fetches population density maps from worldpop, gets population density at given latitude and longitude
    @file popdensity.py
    @author Quentin Bordelon
    <pre>
    Date: 12-03-2026

    MIT License

    Contact Information: qborde1@lsu.edu
    Copyright (c) 2026 Quentin Bordelon

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    </pre>
''' 

import requests, os, rasterio, time, pycountry, math
import pandas as pd
import geopandas as gpd
import reverse_geocoder as rg

US_STATES = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

def buildUrl(iso: str, year: int, stateCode: str) -> str:
    if year >= 2015:
        base = f"https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/{year}"
        if iso == "USA" and stateCode:
            return f"{base}/USA_States/{stateCode}/v1/100m/constrained/{stateCode.lower()}_pop_{year}_CN_100m_R2025A_v1.tif"
        else:
            return f"{base}/{iso.upper()}/v1/100m/constrained/{iso.lower()}_pop_{year}_CN_100m_R2025A_v1.tif"
    
    else:
        targetYear = max(2000, year)
        base = "https://data.worldpop.org/GIS/Population/Global_2000_2020"
        return f"{base}/{targetYear}/{iso.upper()}/{iso.lower()}_ppp_{targetYear}.tif"

def downloadCountryMap(url: str, downloadPath: str) -> None:
  os.makedirs(os.path.dirname(downloadPath), exist_ok=True)

  writePath = downloadPath + "populationDensity.tif"

  with requests.get(url, stream = True) as request:

    with open(writePath, 'wb') as file:
      # the 1024*1024 = 1MiB, insane magic number im sorry
      for chunk in request.iter_content(1024*1024):
        file.write(chunk)

def getCountry(latitude: float, longitude:float):
  results = rg.search((latitude, longitude))
  iso2 = results[0]['cc']
  stateName = results[0]['admin1']

  country = pycountry.countries.get(alpha_2=iso2) 

  if country:
    iso3 = country.alpha_3
    countryName = country.name.replace(' ', '_')
  else:
    iso3 = "USA"
    countryName = "United_States_of_America"

  stateCode = US_STATES.get(stateName) if iso3 == "USA" else None
  return iso3, countryName, stateCode, stateName

def getPopDensity(latitude: float, longitude: float, year: int) -> float:
  isoCode, countryName, stateCode, stateName = getCountry(latitude, longitude)

  if stateCode:
    path = f'./Research/Countries/{isoCode}/{stateCode}/{year}/'
  else:
    path = f'./Research/Countries/{isoCode}/{year}/'

  url = buildUrl(isoCode, year, stateCode) 
  filePath = path + "populationDensity.tif"

  if not os.path.exists(path) or not os.path.isfile(filePath):
    downloadCountryMap(url, path)

  try:
    with rasterio.open(filePath) as source:
      coordinate = [(longitude, latitude)]

      for val in source.sample(coordinate):
        ppp = max(0.0, float(val[0]))

        # this math will be explained in the README. again im sorry
        radiusEarth = 6371.0008
        threeArcSeconds = math.radians(3/3600)
        baseArea = radiusEarth**2 * threeArcSeconds**2
        pixelAreaKm2 = baseArea * math.cos(math.radians(latitude))

        return ppp / pixelAreaKm2
  except: 
    return 0.0
  return 0.0
