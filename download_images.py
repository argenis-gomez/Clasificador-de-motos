import requests
import concurrent.futures
import pandas as pd
import os
import time


def download(path, clase, link):
    response = requests.get(link)
    name = link.split("/")[-1]

    full_path = os.path.join(path, clase, name)

    with open(full_path, 'wb') as f:
        f.write(response.content)


def create_folders(clase, path):
    full_path = os.path.join(path, clase)
    if not os.path.isdir(full_path):
        print(f'Creando directorios {clase}...')
        os.makedirs(full_path)
    else:
        print(f'Directorios {clase} existente...')


def download_images(path, file):

    data = pd.read_csv(file)

    for clase in set(data.clase):
        create_folders(clase, path)

    clases = data.clase.values
    links = data.link.values
    paths = [path for _ in range(len(clases))]

    start = time.process_time()

    print('\n[INFO]: Descargando imágenes. Esto puede tardar unos minutos.')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download, paths, clases, links)

    print(f'\n[INFO]: Descarga finalizada - '
          f'Tiempo transcurrido: {(time.process_time() - start)/60:2.2f} mins - '
          f'Imágenes descargadas: {sum(len(os.listdir(os.path.join(path, clase))) for clase in os.listdir(path))}.')


if __name__ == '__main__':
    DATA_PATH = 'datasets/data2'
    FILE_PATH = 'Links.csv'
    download_images(DATA_PATH, FILE_PATH)
