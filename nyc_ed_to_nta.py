#Used to sort election districts by nyc neighborhood

from collections import defaultdict
from shapely.geometry import Polygon, shape
import json

def intersection(l1, l2):
    return (list(set(l1) & set(l2)))


with open('geojson/ed_map.geojson') as f:
    ed_map = json.load(f)

with open('geojson/nta_map.geojson') as f:
    nta_map = json.load(f)

ed_list = defaultdict(list)
nta_list = defaultdict(list)
nta_names = []
nta_polys = {}
ed_polys = {}


for feat_nta in nta_map['features']:
    nta = shape(feat_nta['geometry'])
    nta_name = feat_nta['properties']['ntaname'] 
    nta_polys[nta_name] = nta
    nta_names.append(nta_name)
    for feat_ed in ed_map['features']:
        ed = shape(feat_ed['geometry'])
        ed_name = feat_ed['properties']['elect_dist']
        ed_polys[ed_name] = ed
        if ed.intersects(nta):
            nta_list[nta_name].append(ed_name)
for n1 in nta_names:
    for n2 in nta_names:
        if (n1 != n2):
            same_eds = intersection(nta_list[n1], nta_list[n2])
            if (len(same_eds) > 0):
                for e in same_eds:
                    inter_area1 = nta_polys[n1].intersection(ed_polys[e]).area
                    inter_area2 = nta_polys[n2].intersection(ed_polys[e]).area
                    if max(inter_area1, inter_area2) == inter_area1:
                        nta_list[n2].remove(e)
                    else:
                        nta_list[n1].remove(e)

with open('ntas/nta_eds.txt', 'w') as outfile:
    json.dump(nta_list, outfile)

