
import requests
import bs4

import lib_tibasic

# TODO da dovursha

# AVTOBUSI = ['88']

# class Spirka:
#     def __init__(s, v_kolko_chasa_idva):
#         s.v_kolko_chasa_idva = v_kolko_chasa_idva

# class Posoka:
#     def __init__(s, ime, spirki):
#         s.ime = ime
#         s.spirki = spirki
    
# class Avtobus:
#     def __init__(s, ime, posoki):
#         s.ime = ime
#         s.posoki = posoki

# raspisanie = []

# for avtobus in AVTOBUSI:
#     url = f'http://schedules.sofiatraffic.bg/autobus/{avtobus}'
#     page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0'})
#     assert page.ok
#     soup = bs4.BeautifulSoup(page.content, 'lxml')

#     breakpoint()

#     found = soup.find('ul', {'class': 'schedule_active_list_tabs'})
#     found = found.find('a', {'class': 'schedule_active_list_active_tab'})
#     delnik_ili_praznik = found.text.strip()
#     print(f'{delnik_ili_praznik=}') # dnes kakvo sme

#     found = soup.findAll('div', {'class': 'schedule_active_list_content'})
#     assert len(found) == 2
#     for soup in found:
#         if soup.find('h3').text.startswith('делник'):
#             delnik = True
#             praznik = False
#         elif soup.find('h3').text.startswith('предпразник, празник'):
#             delnik = False
#             praznik = True
#         else:
#             assert False

#         soup = soup.find('div', {'class': 'schedule_view_direction_content'})

#         found = soup.findAll('div', {'class': 'hours_cell'})
#         while found[0].text.strip() == '':
#             del found[0]
#         first_time = found[0].text.strip().split(' ')[0]

#         # found = soup.findAll('li')
#         # found = soup.findAll('span', 'stop_minutes_print')

#         breakpoint()

with lib_tibasic.TiBasicLib(
    ) as tb:

    tb.print_str('"ZA SEGA SAMO RASPISANIETO NA 88 BA4KA"')
