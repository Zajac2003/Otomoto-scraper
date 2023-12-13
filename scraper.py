from bs4 import BeautifulSoup
import bs4
import requests
import unidecode
import csv

listaNadwozia = ['miejski', 'coupe', 'mini', 'cabrio', 'combi', 'compact', 'minivan', 'sedan', 'suv']


#DONE
def stanTechincznyPart():
    print("Stan techniczny: ")
    print("1. Dowolny")
    print("2. Nieuszkodzony")
    print("3. Uszkodzony")

    stan = input()
    stan = int(stan)

    if stan == 1:
        return ''
    elif stan==2 or stan == 3:
        return f'?search%5Bfilter_enum_damaged%5D={stan-2}'

#DONE
def nadwoziePart():
    print(listaNadwozia)
    nadwozie = input("Wybierz typ nadwozia: ")
    if nadwozie == 'miejski':
        nadwozie = 'city-car'
    return f'{nadwozie}'

#DONE
def markaPart():
    print("Najpopularniejsze marki: ")
    print("Toyota, Skoda, Kia, Volkswagen, Hyundai, Mercedes-Benz, Audi, BMW")
    marka = input("Wpisz marke: ")
    marka = marka.replace(' ', '-')
    marka = marka.lower()

    return f'/{marka}'

#DONE
def makeURL():
    marka = markaPart()
    nadwozie = nadwoziePart()
    stan = stanTechincznyPart()
    #kolor = kolorPart()
    sortowanie = '?search%5Border%5D=filter_float_price%3Adesc'

    url = f'https://www.otomoto.pl/osobowe{marka}/seg-{nadwozie}{stan}{sortowanie}'
    #print(url)
    return url

#DONE
def scrapeData(url):
    poprzednie = []
    obecne = []
    overall = []
    print("Scraping...")
    if isinstance(url, str):

        for nrStrony in range(1, 250):
            # print(url)
            if nrStrony == 2:
                url += f'&page={nrStrony}'
            elif nrStrony > 2:
                url = url.replace(f'&page={nrStrony-1}', f'&page={nrStrony}')

            # print(url)
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                auta = soup.find_all('article', class_ = 'ooa-1t80gpj ev7e6t818')
                print(soup)
                poprzednie = obecne
                obecne = []
                for auto in auta:
                    nazwa = auto.h1.text
                    link = auto.section.a['href']
                    przebieg = auto.dd.text
                    cena = auto.h3.text + ' zl'
                    dodatkowe = auto.p.text

                    try:
                        obraz = auto.img['src']
                    except Exception as e:
                        pass
                    paczka = [nazwa, cena, przebieg, dodatkowe, link, obraz]
                    #print(dodatkowe)
                    #print(cena)
                    #print(przebieg)
                    #print(link)
                    #print(obraz
                    overall.append(paczka)
                    obecne.append(paczka)

                if poprzednie == obecne and nrStrony != 1:
                    #print("listy sa takie same!")
                    break
            else:
                print(f"Nieudane żądanie. Kod odpowiedzi: {response.status_code}")

    else:
        print("Argument nie jest stringiem.")
    print("Scraping done!")
    print("Znaleziono ", len(overall)-1, " aut!")
    print("Kliknij okno na pasku")
    return overall

#DONE
def saveDataToCSV(data):
    with open('dane.csv', 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data)



