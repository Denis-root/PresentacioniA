import geocoder

g = geocoder.ip('me')
print([g.latlng[0], g.latlng[1]])
# print("Latitud:", g.latlng[0])
# print("Longitud:", g.latlng[1])
