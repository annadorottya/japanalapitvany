import argparse
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Japán Alapítvány keresõ')
parser.add_argument('-u', '--username', type=str, nargs='?', help='Felhasználónév')
parser.add_argument('-p', '--password', type=str, nargs='?', help='Jelszó')

args = parser.parse_args()

def login(username = 'guest', password = 'guest'):
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	data = {'felhasznalo': username, 'jelszo': password, 'belepbtn': ''}
	r = requests.post('https://library.japanalapitvany.hu/belep.php', headers=headers, data=data, allow_redirects=False)
	if r.status_code != 302:
		print('Rossz felhasználónév vagy jelszó')
	return r.cookies['PHPSESSID']

def buildDatabase(sessid):
	url = 'https://library.japanalapitvany.hu/keres.php?keres={}&nyelv=0'
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	cookies = dict(PHPSESSID=sessid)
	tableheader = ['Kolcsonozheto?', 'Belso ID', 'Azonosító', 'Szerző', 'Cím', 'Műfaj', 'Megjegyzés', 'Nyelv', 'Visszavárható']
	f = open("database.csv",'w')
	f.write("\t".join(tableheader)+"\n")
	for i in range(2001,2022):
		r = requests.get(url.format(i), headers=headers, cookies=cookies, allow_redirects=False)
		soup = BeautifulSoup(r.text, features="html.parser")
		rows = soup.find_all('tr')
		for r in rows:
			if 'table-light' in r['class']:
				data = ['Nem']
			else:
				data = ['Igen']
			data.append(str(r['onclick'][10:-1]))
			cols = r.find_all('td')
			data += [ele.text.strip().replace('\n',' ').replace('\r',' ') for ele in cols]
			if 'table-light' not in r['class']:
				f.write("\t".join(data)+"\n")
	f.close()

def logout(sessid):
	url = 'https://library.japanalapitvany.hu/kilep.php'
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	cookies = dict(PHPSESSID=sessid)
	r = requests.get(url, headers=headers, cookies=cookies, allow_redirects=False)


username = args.username if args.username != None else 'guest'
password = args.password if args.password != None else 'guest'

sessid = login(username, password)
buildDatabase(sessid)
logout(sessid)