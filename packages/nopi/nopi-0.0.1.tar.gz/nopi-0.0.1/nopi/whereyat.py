'''
http://whereyat.nola.gov/
'''

import requests

def find(address):
    url_1 = "https://gis.nola.gov/arcgis/rest/services/CompositePIN2/GeocodeServer/findAddressCandidates?SingleLine={}&f=json".format(address)

    req_1 = requests.get(url_1)
    resp = req_1.json()
    resp['candidates'][0]['location']
    x_val = resp['candidates'][0]['location']['x']
    y_val = resp['candidates'][0]['location']['y']


    base = "https://gis.nola.gov/arcgis/rest/services/apps/WhereYat/MapServer/identify?"
    base_geo = "geometry={x:" + str(x_val) +",y:" + str(y_val)+"}&"
    geo_type = "geometryType=esriGeometryPoint&layers=all&tolerance=2&"
    change_value = .00001
    x_lower = x_val - (x_val * change_value)
    x_upper = x_val + (x_val * change_value)
    y_lower = y_val - (y_val * change_value)
    y_upper = y_val + (y_val * change_value)
    map_extent = "mapExtent={},{},{},{}&".format(x_lower,y_lower,x_upper,y_upper)
    display_image = "imageDisplay=20,20,96&returnGeometry=false&f=json"
    url_3 = base + base_geo + geo_type + map_extent + display_image
    resp_2 = requests.get(url_3)
    return(resp_2)
