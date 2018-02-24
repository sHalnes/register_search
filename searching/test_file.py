#latlon=(62.47122631331753, 6.152870260741565)
#with open('coords.txt', 'w') as file:
#    s = str(latlon[0]) + ' ' + str(latlon[1])
#    file.write(s)

try:
    with open('coords.txt', 'r') as file:
        s = file.readline().split()
        lat = float(s[0])
        lon = float(s[1])
            #if float(s[0]) > 0.0:
            #    latlon = [float(s[0]), float(s[1])]
except FileNotFoundError:
    pass


print(lat, lon)