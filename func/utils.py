from datetime import datetime
import pandas as pd

ACTUAL_YEAR = datetime.now().year

MONTHS = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}
YEAR_SEASONS = ("Verano", "Otoño", "Invierno", "Primavera")
YEARS_IN_DATA = tuple(range(2017, ACTUAL_YEAR + 1))

PUNTOS_CARDINALES = [
    {"punto_cardinal": "N", "viento_d": 0},
    {"punto_cardinal": "NE", "viento_d": 45},
    {"punto_cardinal": "E", "viento_d": 90},
    {"punto_cardinal": "SE", "viento_d": 135},
    {"punto_cardinal": "S", "viento_d": 180},
    {"punto_cardinal": "SO", "viento_d": 225},
    {"punto_cardinal": "O", "viento_d": 270},
    {"punto_cardinal": "NW", "viento_d": 315},
]
DF_PUNTOS_CARDINALES = pd.DataFrame(PUNTOS_CARDINALES)

def angulo_a_cardinal(a):
    angulo = a % 360

    if 337.5 <= angulo or angulo < 22.5:
        return "N"
    elif 22.5 <= angulo < 67.5:
        return "NE"
    elif 67.5 <= angulo < 112.5:
        return "E"
    elif 112.5 <= angulo < 157.5:
        return "SE"
    elif 157.5 <= angulo < 202.5:
        return "S"
    elif 202.5 <= angulo < 247.5:
        return "SO"
    elif 247.5 <= angulo < 292.5:
        return "O"
    elif 292.5 <= angulo < 337.5:
        return "NO"

def season(day: pd.Timestamp, season: str) -> bool:
    
    año = day.year

    if season.lower() == 'verano':
        return (day >= pd.Timestamp(f'{año}-12-21') and day < pd.Timestamp(f'{año}-03-20'))
    elif season.lower() == 'otoño':
        return (day >= pd.Timestamp(f'{año}-03-20') and day < pd.Timestamp(f'{año}-06-21'))
    elif season.lower() == 'invierno':
        return (day >= pd.Timestamp(f'{año}-06-21') and day < pd.Timestamp(f'{año}-09-23'))
    elif season.lower() == 'primavera':
        return (day >= pd.Timestamp(f'{año}-09-23') and day < pd.Timestamp(f'{año}-12-21'))
    return False
