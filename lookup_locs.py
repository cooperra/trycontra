import json
from json import encoder
import urllib2
import time

def lookup_ll(loc):
  loc = loc.replace(" ", "+")
  q = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % loc
  j = urllib2.urlopen(q).read()
  r = json.loads(j)

  try:
    ll = r["results"][0]["geometry"]["location"]
  except Exception:
    import pprint
    pprint.pprint(r)
    return 0,0

  return ll["lat"], ll["lng"]

def build_loc_lookup():
  existing_locs = json.loads(open("dances_locs.json").read())
  loc_lookup = {}
  for url, loc, days, freq, lat, lng in existing_locs:
    loc_lookup[loc] = [lat, lng]
  return loc_lookup

def start():
  dances = json.loads(open("dances.json").read())
  loc_lookup = build_loc_lookup()

  loc_dances = []
  for url, loc, days, freq in dances:
    if loc in loc_lookup:
      lat, lng = loc_lookup[loc]
    else:
      lat, lng = lookup_ll(loc)
      time.sleep(1)
    loc_dances.append([url, loc, days, freq, lat, lng])
  with open("dances_locs.json", "w") as outf:
    # monkey-patch json to round floats

    old_float_repr = encoder.FLOAT_REPR
    encoder.FLOAT_REPR = lambda o: format(o, '.2f')
    outf.write(json.dumps(loc_dances).replace("],", "],\n"))
    encoder.FLOAT_REPR = old_float_repr

if __name__ == "__main__":
  start()

