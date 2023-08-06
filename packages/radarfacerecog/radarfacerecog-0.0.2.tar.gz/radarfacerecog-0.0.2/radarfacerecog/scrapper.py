import pandas as pd
import requests
import io

from bs4 import BeautifulSoup
from PIL import Image



df = pd.read_csv('politicos.csv')
df.sort_values(by=['Id Parlamento'], inplace=True)
deputado = df[df['Cargo'].values == 'Deputado']
id_deputados = deputado['Id Parlamento'].astype(str).tolist()
senador = df[df['Cargo'].values == 'Senador']
id_senador = senador['Id Parlamento'].astype(str).tolist()


def scrapper():
    for ids in id_deputados:
        try:
            url = f'https://www.camara.leg.br/deputados/{ids}/biografia'
            r = requests.get(url)
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            image = soup.find_all('div', {'class': 'foto-deputado'})
            image_url = [i.find('img')['src'] for i in image]
            image_url = ''.join(image_url)
            nome = soup.select('h1.titulo-internal')[0].text.strip()
            re = requests.get(image_url)
            img = Image.open(io.BytesIO(re.content)).convert('RGB')
            img.save(f'data/{nome}.jpg', 'JPEG')
            print(f'Scrapper done for {nome}')
        except:
            print(f'Error while scraping {nome}')
            pass

count = 0
def scrapper_senador():
    for ids in id_senador:
        try:
            count += 1
            url = f'https://www25.senado.leg.br/web/senadores/senador/-/perfil/{ids}'
            r = requests.get(url)
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            image = soup.find_all('div', {'class': 'foto-deputado'})
            image_url = [i.find('img')['src'] for i in image]
            image_url = ''.join(image_url)
            nome = [i.find('img')['alt'] for i in image]
            nome = ''.join(nome)
            re = requests.get(image_url)
            img = Image.open(io.BytesIO(re.content)).convert('RGB')
            img.save(f'data/{nome}.jpg', 'JPEG')
            print(f'Scrapper done for {nome}')
        except:
            print(f'Error while scraping {nome}')
            pass
