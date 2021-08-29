import argparse
import requests
from bs4 import BeautifulSoup
from datetime import date

parser = argparse.ArgumentParser(description='Japán Alapítvány keresõ')
parser.add_argument('-u', '--username', type=str, nargs='?', help='Felhasználónév')
parser.add_argument('-p', '--password', type=str, nargs='?', help='Jelszó')
parser.add_argument('-f', '--full', dest='full', action='store_true', help='Nem kolcsonozheto konyveket is listazza')
parser.add_argument('-l', '--limit', type=int, nargs='?', help='Ha ennyi napja nem hoztak meg vissza a konyvet a lejarati ido vege utan, akkor mar nem remenykeduk, hogy valaha vissza lesz hozva')
parser.set_defaults(username='guest', password='guest', full=False, limit=90)
args = parser.parse_args()

today = date.today()

def login(username = 'guest', password = 'guest'):
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	data = {'felhasznalo': username, 'jelszo': password, 'belepbtn': ''}
	r = requests.post('https://library.japanalapitvany.hu/belep.php', headers=headers, data=data, allow_redirects=False)
	if r.status_code != 302:
		print('Rossz felhasználónév vagy jelszó')
	return r.cookies['PHPSESSID']

def buildDatabase(sessid, full):
	url = 'https://library.japanalapitvany.hu/keres.php?keres={}&nyelv=0'
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	cookies = dict(PHPSESSID=sessid)
	tableheader = ['Kolcsonozheto?', 'Belso ID', 'Azonosító', 'Szerző', 'Cím', 'Műfaj', 'Megjegyzés', 'Nyelv', 'Visszavárható']
	ids = []
	f = open("database.csv",'w')
	f.write("\t".join(tableheader)+"\n")
	for i in range(2001,2022):
		r = requests.get(url.format(i), headers=headers, cookies=cookies, allow_redirects=False)
		soup = BeautifulSoup(r.text, features="html.parser")
		rows = soup.find_all('tr')
		for r in rows:
			id = str(r['onclick'][10:-1])
			if id not in ids:
				if 'table-light' in r['class']:
					data = ['Nem']
				else:
					data = ['Igen']
				data.append(id)
				cols = r.find_all('td')
				data += [ele.text.strip().replace('\n',' ').replace('\r',' ') for ele in cols]
				lostCause = False
				if not full and data[8] != "":
					backdate = date.fromisoformat(data[8])
					if (today-backdate).days > args.limit:
						lostCause = True
				if full or ('table-light' not in r['class'] and not lostCause):
					f.write("\t".join(data)+"\n")
				ids.append(id)
	f.close()
	print("Tablazat letoltese kesz")

def logout(sessid):
	url = 'https://library.japanalapitvany.hu/kilep.php'
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	cookies = dict(PHPSESSID=sessid)
	r = requests.get(url, headers=headers, cookies=cookies, allow_redirects=False)

sessid = login(args.username, args.password)
buildDatabase(sessid, args.full)
logout(sessid)
