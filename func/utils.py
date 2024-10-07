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
        return "SW"
    elif 247.5 <= angulo < 292.5:
        return "W"
    elif 292.5 <= angulo < 337.5:
        return "NW"
