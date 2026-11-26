#!/usr/bin/env python3
"""Sync one cooked dish to the website.

Usage: update_dish.py COUNTRY RECORD.json [PHOTO.jpg]
RECORD.json is the country's record from cookbook/recipes/<region>.json
(title, description, ingredients, directions, optional personal_note).
Updates recipes.json (card text) and dishes.json (tile name, photo, cooked state).
"""
import sys, json, io, base64
from PIL import Image, ImageOps

country, rec_path = sys.argv[1], sys.argv[2]
photo = sys.argv[3] if len(sys.argv) > 3 else None
rec = json.load(open(rec_path))
dishes = json.load(open('dishes.json'))
recipes = json.load(open('recipes.json'))
d = next(x for x in dishes if x['country'].lower() == country.lower())
r = {'t': rec['title'], 's': rec['description'], 'i': rec['ingredients'], 'd': rec['directions']}
if rec.get('personal_note'):
    r['n'] = rec['personal_note']
recipes[d['id']] = r
d['name'] = rec['title']
if photo:
    im = ImageOps.fit(ImageOps.exif_transpose(Image.open(photo)).convert('RGB'), (480, 480))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=82)
    d['img'] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    d['photo'] = True
json.dump(dishes, open('dishes.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(recipes, open('recipes.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('updated', d['id'], d['country'], '| cooked:', sum(1 for x in dishes if x.get('photo')))
