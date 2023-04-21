import boto3
import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

S3_BUCKET = 'parcial-2-bucketcito'
fecha = date.today()

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')

def extraerTiempo(file):
    contenido = s3.get_object(Bucket=S3_BUCKET, Key=file)["Body"].read() 
    soup = BeautifulSoup(contenido, 'html.parser')

    texto='titulo,categoria,link\n'
    
    for articles in soup.find_all('article'):
        for links in articles.find_all('a',class_='title page-link'):
            try:
              link='"'+links["href"]+'"'
              #print(link)
              categoria='"'+link.split('/')[1]+'"'
              #print(categoria)
              titulo='"'+(links.text)+'"'
              texto+=f'{titulo},{categoria},{link}\n'
            except:
                ...
             

    url="headlines/final/periodico=ElTiempo/year="+str(fecha.year)+"/month="+str(fecha.strftime('%m'))+"/elTiempo"
    s3_resource.Object(S3_BUCKET, url+'{}.csv'.format(fecha.strftime('%Y-%m-%d'))).put(Body=texto)
 
def extraerEspectador(file):
    contenido = s3.get_object(Bucket=S3_BUCKET, Key=file)["Body"].read() 
    soup = BeautifulSoup(contenido, 'html.parser')
    texto='titulo,categoria,link\n'

    for articles in soup.find_all('h2',class_='Card-Title Title Title'):
      for links in articles.find_all('a'):
        try:
          link=links["href"]
          categoria=link.split('/')[1]
          titulo=((link.replace('-',' ')).replace(categoria,'')).replace('/','')
          texto+=f'{titulo},{categoria},{link}\n'
        except:
          ...
    url="headlines/final/periodico=ElEspectador/year="+str(fecha.year)+"/month="+str(fecha.strftime('%m'))+"/elEspectador"
    s3_resource.Object(S3_BUCKET, url+'{}.csv'.format(fecha.strftime('%Y-%m-%d'))).put(Body=texto)

extraerTiempo("headlines/raw/ElTiempo-"+str(fecha.year)+"-"+str(fecha.strftime('%m'))+"-"+str(fecha.strftime('%d'))+".html")
extraerEspectador("headlines/raw/ElEspectador-"+str(fecha.year)+"-"+str(fecha.strftime('%m'))+"-"+str(fecha.strftime('%d'))+".html")
 