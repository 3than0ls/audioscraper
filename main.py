from bs4 import BeautifulSoup
import requests
from pathlib import Path

# https://cafeaudiobooks.com/haruki-murakami-norwegian-wood-audiobook/


def download_audio(url: str, name: str):
    data = requests.get(url)
    with open(Path(f'./output/{name}.mp3'), 'wb') as f:
        f.write(data.content)


def download_all_audio_on_page(url: str, page: int):
    full_url = url
    if page != 1:
        full_url += f"/{page}"

    print(f'Downloading from "page" {page} (URL: {full_url})')

    soup = BeautifulSoup(requests.get(full_url).content, "html.parser")

    audio_tag = soup.find_all('audio')
    for audio in audio_tag:
        audio_id = audio['id']
        src = audio.find('source')
        if src and src.get('type', None) == "audio/mpeg" and src.get('src', None) != None:
            audio_name = src['src'].split('/')[-1].split(".mp")[0]
            print(f"Downloading {audio_id}:\t\t{src['src']}")
            download_audio(src['src'], audio_name)


def main():
    base_url = input('Enter book URL:\n')

    num_pages = int(input('Number of "pages": '))

    for page in range(1, num_pages):
        download_all_audio_on_page(base_url, page)


if __name__ == '__main__':
    main()
