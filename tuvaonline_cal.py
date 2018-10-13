import requests
from bs4 import BeautifulSoup as bs
import re
import datetime

def tuvaonline():
    url = "https://www.tuvaonline.ru/dates/"
    r = requests.get(url)
    table = bs(r.text, 'lxml').find("table", attrs={"cellpadding": "5"})
    calendar = []
    for row in table.find_all('td'):
        #if (row.find('font', {'color':'red'})):
        now = datetime.datetime.now()
        if (row.find('font')):
            if (row.find('font').text) == " СЕГОДНЯ":                
                tit = (row.text)
                if re.findall(r'День рождения',tit):
                    zero = 0                    
                else:
                    tit = re.sub(r'СЕГОДНЯ: ', '', tit)
                    tit = re.sub(r'new!  ', '', tit)
                    tit = re.sub(r'', '', tit)[3:]
                    tit = re.sub(r'^\s+|\n|\r|\s+$', '', tit)
                    tit = re.sub(r'[\ \n]{2,}', '', tit)
                    tit = re.sub(r'\([^)]*\)', '', tit)
                    place = re.findall(r'\((.*?)\)',row.text)
                    h = re.findall(r'Начало в (\d+)',tit)
                    date = now.strftime("%d/%m/%Y")
                    if h:
                        time = (now.strftime("%s:00" % h[0])) 
                    else:
                        time = "время не определено"

                    if place:
                        mesto = (place[0])
                    else:
                        mesto = "место не определено"
                    cal ={"date":date,"tit":tit,"time":time,"mesto":mesto,"region":"Туваонлайн"}
                    calendar.append(cal)

            if (row.find('font').text) == " ЗАВТРА":
                tit = (row.text)
                if re.findall(r'День рождения',tit):
                    zero = 0                    
                else:
                    tit = re.sub(r'ЗАВТРА: ', '', tit)
                    tit = re.sub(r'new!  ', '', tit)
                    tit = re.sub(r'', '', tit)[3:]
                    tit = re.sub(r'^\s+|\n|\r|\s+$', '', tit)
                    tit = re.sub(r'[\ \n]{2,}', '', tit)
                    tit = re.sub(r'\([^)]*\)', '', tit)
                    place = re.findall(r'\((.*?)\)',row.text)
                    h = re.findall(r'Начало в (\d+)',tit)
                    date = ((datetime.datetime.now() + datetime.timedelta(days=1))).strftime("%d/%m/%Y")
                    if h:
                        time = (now.strftime("%s:00" % h[0])) 
                    else:
                        time = "время не определено"
                    if place:
                        mesto = (place[0])
                    else:
                        mesto = "место не определено"
                    cal ={"date":date,"tit":tit,"time":time,"mesto":mesto,"region":"Туваонлайн"}
                    calendar.append(cal)
    return calendar
 
def message():
    now = datetime.datetime.now()
    for text in tuvaonline():
        if (text['date']) == now.strftime("%d/%m/%Y"):
            print ("Сегодня (%s)- %s(место: %s) Время: %s " % (text['date'],text['tit'],text['mesto'],text['time']))
            print ("-------------------")
        else:
            print ("Завтра (%s)- %s(место: %s) Время: %s " % (text['date'],text['tit'],text['mesto'],text['time']))
            print ("-------------------")
