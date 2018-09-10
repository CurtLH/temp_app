#!/usr/bin/env python
# coding: utf-8

import psycopg2
import requests

conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="apassword",
                        host="192.168.0.104") 
conn.autocommit = True
cur = conn.cursor()
cur.execute("""SELECT condition -> 'current_observation' -> 'temp_f',
                      condition -> 'current_observation' -> 'observation_time'
               FROM arlington_weather_condition
               WHERE id = (SELECT MAX(id) 
                           FROM arlington_weather_condition
                           WHERE condition -> 'current_observation' ->> 'temp_f' != '')""")

results = [i for i in cur]
temp = results[0][0]
datetime = results[0][1]

results = {
    'temp': temp,
    'datetime': datetime
}

requests.post('https://dweet.io:443/dweet/for/dirty_curty', json=results)

#r = requests.get('https://dweet.io:443/get/latest/dweet/for/dirty_curty')
#r.json()
