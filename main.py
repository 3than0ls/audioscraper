from bs4 import BeautifulSoup
import requests
from pathlib import Path

# https://cafeaudiobooks.com/haruki-murakami-norwegian-wood-audiobook/


def download_audio(url: str, name: str):
    data = requests.get(url)
    with open(Path(f'./output/{name}.mp3'), 'wb') as f:
        f.write(data.content)


def main():
    url = input('CafeAudioBook book URL:\n')
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    audio_tag = soup.find_all('audio')
    for audio in audio_tag:
        audio_id = audio['id']
        src = audio.find('source')
        if src and src.get('type', None) == "audio/mpeg" and src.get('src', None) != None:
            print(f"Downloading {audio_id}:\t\t{src['src']}")
            download_audio(src['src'], audio_id)


if __name__ == '__main__':
    main()
