"""
Scraper de propiedades desde bdhousing.com
Ciudades objetivo: Dhaka, Chattogram, Narayanganj, Gazipur, Cumilla
(las mismas que ya están en house_price_bd.csv)

REQUISITOS (ejecutar UNA VEZ antes de correr este script):
    pip install cloudscraper beautifulsoup4 pandas

POR QUÉ BDHOUSING.COM:
    - No usa Cloudflare, responde correctamente a requests normales
    - Mayor portal inmobiliario de Bangladesh (150,000+ listings)
    - HTML estático con selectores CSS claros y consistentes
    - No requiere ningún navegador
"""

import time
import re
import pandas as pd
import cloudscraper
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────────────────────

# Cada ciudad tiene su propia URL en bdhousing.
# La clave es el nombre que va al CSV, el valor es la lista de URLs a scrapear.
CIUDADES = {
    "dhaka": [
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=2",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=3",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=4",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=5",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=6",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=7",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=8",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=9",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=10",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=11",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=12",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=13",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=14",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=15",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=16",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=17",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=18",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=19",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=20",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=21",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=22",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=23",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=24",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=25",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=26",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=27",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=28",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=29",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=30",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=31",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=32",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=33",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=34",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=35",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=36",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=37",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=38",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=39",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=40",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=41",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=42",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=43",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=44",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=45",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=46",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=47",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=48",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=49",
        "https://www.bdhousing.com/pages/ready-flat-sale-in-dhaka?page=50",
    ],
    "chattogram": [
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=2",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=3",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=4",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=5",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=6",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=7",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=8",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=9",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=10",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=11",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=12",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=13",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=14",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=15",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=16",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=17",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=18",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=19",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=20",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=21",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=22",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=23",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=24",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=25",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=26",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=27",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=28",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=29",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=30",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=31",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=32",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=33",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=34",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=35",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=36",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=37",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=38",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=39",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=40",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=41",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=42",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=43",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=44",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=45",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=46",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=47",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=48",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=49",
        "https://www.bdhousing.com/search?city=Chattogram&purpose=Sale&type=Apartment&page=50",
    ],
    "narayanganj-city": [
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=2",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=3",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=4",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=5",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=6",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=7",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=8",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=9",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=10",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=11",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=12",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=13",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=14",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=15",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=16",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=17",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=18",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=19",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=20",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=21",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=22",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=23",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=24",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=25",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=26",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=27",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=28",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=29",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=30",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=31",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=32",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=33",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=34",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=35",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=36",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=37",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=38",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=39",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=40",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=41",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=42",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=43",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=44",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=45",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=46",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=47",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=48",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=49",
        "https://www.bdhousing.com/search?city=Narayanganj&purpose=Sale&type=Apartment&page=50",
    ],
    "gazipur": [
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=2",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=3",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=4",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=5",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=6",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=7",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=8",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=9",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=10",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=11",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=12",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=13",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=14",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=15",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=16",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=17",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=18",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=19",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=20",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=21",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=22",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=23",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=24",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=25",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=26",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=27",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=28",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=29",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=30",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=31",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=32",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=33",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=34",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=35",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=36",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=37",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=38",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=39",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=40",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=41",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=42",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=43",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=44",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=45",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=46",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=47",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=48",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=49",
        "https://www.bdhousing.com/search?city=Gazipur&purpose=Sale&type=Apartment&page=50",
    ],
    "cumilla": [
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=2",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=3",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=4",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=5",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=6",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=7",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=8",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=9",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=10",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=11",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=12",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=13",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=14",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=15",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=16",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=17",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=18",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=19",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=20",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=21",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=22",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=23",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=24",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=25",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=26",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=27",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=28",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=29",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=30",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=31",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=32",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=33",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=34",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=35",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=36",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=37",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=38",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=39",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=40",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=41",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=42",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=43",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=44",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=45",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=46",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=47",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=48",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=49",
        "https://www.bdhousing.com/search?city=Comilla&purpose=Sale&type=Apartment&page=50",
    ],
}

PAUSA_ENTRE_REQUESTS = 2  # segundos entre cada request (respetar el servidor)
CSV_DESTINO = "house_price_bd.csv"


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIONES DE LIMPIEZA
# ─────────────────────────────────────────────────────────────────────────────

def convertir_precio(texto):
    """
    Convierte el precio de bdhousing a entero en Takas.

    bdhousing usa dos formatos:
      - "৳ 2.99 Cr./total"  → 2.99 × 10,000,000 = 29,900,000 Takas
      - "৳ 80.60 Lac/total" → 80.60 × 100,000   =  8,060,000 Takas

    Retorna None si el texto no es parseable.
    """
    if not texto:
        return None
    texto = texto.replace('৳', '').replace(',', '').strip()
    try:
        if 'cr' in texto.lower():
            num = float(re.search(r'[\d.]+', texto).group())
            return int(num * 10_000_000)   # 1 Crore = 10,000,000 Takas
        elif 'lac' in texto.lower() or 'lakh' in texto.lower():
            num = float(re.search(r'[\d.]+', texto).group())
            return int(num * 100_000)      # 1 Lac = 100,000 Takas
        else:
            m = re.search(r'[\d.]+', texto)
            return int(float(m.group())) if m else None
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIÓN DE SCRAPING
# ─────────────────────────────────────────────────────────────────────────────

def extraer_propiedades(scraper, url, ciudad_csv):
    """
    Descarga una página de bdhousing.com y extrae todas las propiedades.

    Selectores CSS confirmados inspeccionando el HTML real del sitio:
      - Tarjeta:     div.flex-row
      - Título:      h1.title.fix_title
      - Precio:      label.control-label1.new
      - Ubicación:   p.location
      - Habitaciones: div.listing-info.bedroom → span.number
      - Baños:        div.listing-info.bath     → span.number
      - Área (sqft):  div.listing-info.size     → span.number
    """
    try:
        respuesta = scraper.get(url, timeout=15)
    except Exception as e:
        print(f"  ⚠ Error de conexión: {e}")
        return []

    if respuesta.status_code != 200:
        print(f"  ⚠ Status {respuesta.status_code} en {url}")
        return []

    soup = BeautifulSoup(respuesta.text, 'html.parser')

    # Cada propiedad está dentro de un div con clase "flex-row"
    tarjetas = soup.find_all('div', class_='flex-row')

    if not tarjetas:
        print(f"  ⚠ Sin tarjetas encontradas — puede que no haya más páginas")
        return []

    resultados = []
    for tarjeta in tarjetas:
        try:
            # ── TÍTULO ────────────────────────────────────────────────────
            titulo_tag = tarjeta.find('h1', class_='title')
            titulo = titulo_tag.get_text(' ', strip=True) if titulo_tag else None
            if not titulo:
                continue  # sin título no guardamos la propiedad

            # ── PRECIO ────────────────────────────────────────────────────
            precio_tag = tarjeta.find('label', class_='control-label1')
            precio = convertir_precio(precio_tag.get_text(strip=True)) if precio_tag else None
            if not precio:
                continue  # sin precio no tiene sentido guardar

            # ── UBICACIÓN ─────────────────────────────────────────────────
            loc_tag = tarjeta.find('p', class_='location')
            # get_text(' ') une el texto del ícono y la dirección con espacio
            ubicacion = loc_tag.get_text(' ', strip=True) if loc_tag else ciudad_csv

            # ── HABITACIONES, BAÑOS Y ÁREA ────────────────────────────────
            # Los tres están en divs con clase "listing-info" + tipo específico
            habitaciones = banos = area = None

            for info in tarjeta.find_all('div', class_='listing-info'):
                clases = info.get('class', [])
                numero_tag = info.find('span', class_='number')
                valor = numero_tag.get_text(strip=True) if numero_tag else None

                if 'bedroom' in clases:
                    habitaciones = float(valor) if valor else None
                elif 'bath' in clases:
                    banos = float(valor) if valor else None
                elif 'size' in clases:
                    # El área viene sin comas: "2850", "1300", etc.
                    area = float(valor.replace(',', '')) if valor else None

            resultados.append({
                'Title':            titulo,
                'Bedrooms':         habitaciones,
                'Bathrooms':        banos,
                'Floor_no':         None,       # bdhousing no muestra el piso en el listado
                'Occupancy_status': 'vacant',   # valor por defecto conservador
                'Floor_area':       area,
                'City':             ciudad_csv,
                'Location':         ubicacion,
                'Price_in_taka':    f"৳{precio:,}"
            })

        except Exception as e:
            print(f"  ⚠ Error procesando tarjeta: {e}")
            continue

    return resultados


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIÓN PARA GUARDAR EN CSV
# ─────────────────────────────────────────────────────────────────────────────

def agregar_al_csv(nuevos_datos, ruta_csv):
    """
    Une los datos scrapeados con el CSV original.
    Solo agrega filas cuyo Título NO existe ya en el CSV (evita duplicados).
    Nunca elimina filas del dataset original.
    """
    if not nuevos_datos:
        print("\n⚠ No se obtuvieron datos nuevos para agregar.")
        return

    df_nuevo    = pd.DataFrame(nuevos_datos)
    df_original = pd.read_csv(ruta_csv)
    filas_antes = len(df_original)

    # Crear un set de títulos ya existentes para comparar rápidamente
    titulos_existentes = set(df_original['Title'].dropna().str.strip().str.lower())

    # Filtrar: solo conservar las filas nuevas cuyo título no existe en el original
    df_unicos = df_nuevo[
        ~df_nuevo['Title'].str.strip().str.lower().isin(titulos_existentes)
    ].copy()

    # Concatenar y guardar
    df_final = pd.concat([df_original, df_unicos], ignore_index=True)
    df_final.to_csv(ruta_csv, index=False)

    print(f"\n{'─'*40}")
    print(f"Filas originales en CSV:   {filas_antes}")
    print(f"Propiedades scrapeadas:    {len(df_nuevo)}")
    print(f"Nuevas filas agregadas:    {len(df_unicos)}")
    print(f"Total final en CSV:        {len(df_final)}")
    print(f"✓ Guardado en: {ruta_csv}")


# ─────────────────────────────────────────────────────────────────────────────
# EJECUCIÓN PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  SCRAPER BDHOUSING.COM — Propiedades Bangladesh")
    print("  (sin navegador, requests directos)")
    print("=" * 60)

    # cloudscraper emula un navegador real a nivel de headers y TLS
    # para pasar protecciones básicas sin necesitar Chrome ni Firefox
    scraper = cloudscraper.create_scraper()

    todos_los_datos = []

    for ciudad_csv, lista_urls in CIUDADES.items():
        print(f"\n{'─'*40}")
        print(f"CIUDAD: {ciudad_csv.upper()}")
        print(f"{'─'*40}")

        for url in lista_urls:
            propiedades = extraer_propiedades(scraper, url, ciudad_csv)
            todos_los_datos.extend(propiedades)
            print(f"  {len(propiedades):2d} props ← {url.split('bdhousing.com')[-1]}")
            time.sleep(PAUSA_ENTRE_REQUESTS)

    print(f"\nTotal scrapeado: {len(todos_los_datos)} propiedades")

    # Guardar en el CSV del proyecto
    print(f"\n{'='*60}")
    print("  GUARDANDO EN CSV")
    print(f"{'='*60}")
    agregar_al_csv(todos_los_datos, CSV_DESTINO)

    print("\n✓ Proceso completado.")
