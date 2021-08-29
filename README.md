# Japan Alapitvany Library scraper
## Search faster, read moar books

The [Japan Foundation in Budapest](https://japanalapitvany.hu/en) has an [online catalog](https://library.japanalapitvany.hu/) for their library (using a webapp called [Kiskönyvtár.Net](https://kiskonyvtar.net/)). The search functionality has its limitations, so I decided to scrape the data from it to a csv file.

##Usage
```
usage: main.py [-h] [-u [USERNAME]] [-p [PASSWORD]]

Japán Alapítvány keresõ

optional arguments:
  -h, --help            show this help message and exit
  -u [USERNAME], --username [USERNAME]
                        Felhasználónév
  -p [PASSWORD], --password [PASSWORD]
                        Jelszó
```