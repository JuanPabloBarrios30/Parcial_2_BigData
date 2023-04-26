import boto3
import urllib.request
import datetime


def download_page(url, bucket, nombre):
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    today = datetime.date.today().strftime('%Y-%m-%d')
    s3 = boto3.resource('s3')
    s3.Object(bucket,
              'headlines/raw/{}{}.html'.format(nombre,
                                               today)).put(Body=content)


download_page('https://www.eltiempo.com', 'parcial-2-bucketcito', 'ElTiempo-')
download_page('https://www.elespectador.com', 'parcial-2-bucketcito',
              'ElEspectador-')
