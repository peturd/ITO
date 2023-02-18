from requests import get
from bs4 import BeautifulSoup
from bs4.element import Tag
from time import sleep
import os
from shutil import rmtree


TITLE = None


def InputURL() -> str:
    URL = input('Input website link: ')
    return URL


def RequestData(URL:str):
    print('Connecting...')
    headers = {'User-Agent': 'PostmanRuntime/7.31.0'} # pass the security of website
    try:
        sleep(1)
        data = get(URL, headers=headers)
    except:
        print('Can not connect to website.')
        print('Error code: Syntax error. Contact developer for more information.')
        exit()

    if (data.status_code != 200): 
        print('Can not connect to website.')
        print('Error code: Access denied. Contact developer for more information')
        exit()
    else: return BeautifulSoup(data.text, 'html.parser')


class Section:
    def __init__(self, index:int, name:str, audio_link:str, question:Tag) -> None:
        self.index = index
        self.name = name
        self.audio_link = audio_link
        self.question = question


def ProcessData(html_source:BeautifulSoup):
    global TITLE
    TITLE = html_source.find('h1', 'entry-title').text
    print(f'Connected: {TITLE}')
    print('Processing...')
    sleep(2)
    rows = html_source.find_all('div', 'et_pb_row')
    index = 0
    result : list[Section] = []
    while(index < len(rows)):
        if (len(rows[index].find_all('audio')) != 0):
            name = rows[index].find_all('h3', 'et_pb_module_header')[0].text
            audio_link = rows[index].find_all('audio')[0].text
            question = rows[index+1].find_all('div', 'et_pb_module')[0]
            result.append(
                Section(index, name, audio_link, question)
            )
        index += 1
    return result


def Download(sections:list[Section]) -> None:
    downloadPath = os.path.abspath(os.path.join(os.curdir, TITLE))

    folders = [ name for name in os.listdir(".") if os.path.isdir(name) ]
    if TITLE in folders:
        print(f'Folder "{TITLE}" existed. Do you want to replace this folder? (Y/N): ', end='')
        if input() == 'N':
            print('Download canceled.')
            exit()
        else:
            rmtree(downloadPath)
    
    os.mkdir(downloadPath)

    headers = {'User-Agent': 'PostmanRuntime/7.31.0'} # pass the security of website
    for section in sections:
        print(f'Download {section.name}...')
        file = get(section.audio_link, headers=headers)
        open(os.path.join(downloadPath, f'{section.name}.mp3'), 'wb').write(file.content)

    print('Download complete!')



if __name__ == '__main__':
    URL = InputURL()
    data = RequestData(URL)
    sections = ProcessData(data)
    Download(sections)