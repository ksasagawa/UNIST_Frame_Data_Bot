import aiohttp
from contextlib import closing
from bs4 import BeautifulSoup
import requests
import re

#unused alternative to requests library using aiohttp and asychronous subcommands to get websites. Would be a better alternative to requests 
async def get_asyncHTML(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.read()
            return response.url, html

def get_HTML_requests(url):
    return requests.get(url)

def find_normal(page, move):
    output = []
    soup = BeautifulSoup(page.text, 'lxml')
    info = soup.find('big', text = move)
    info = info.parent
    info = info.find_next_sibling("td")
    for data in info.find_all('td')[0:7]:
        output.append(data.text.strip())
    return output

#converts input from A,B,C to X and searches for it. If the move is type A then it takes the first 6 html results, B takes 9-15, C takes 18-24 due to how Mizzumi wiki is set up    
def find_special(page, move):
    output = []
    soup = BeautifulSoup(page.text, 'lxml')
    #checks if there is a specific version of the special in which it would not be notated with X
    if(soup.find('small', text = move) == None and any(character.isdigit() for character in move)):
        formatted_move = move.replace("A", "X").replace("B", "X").replace("C", "X")
        info = soup.find('small', text = formatted_move)
        info = info.parent
        info = info.find_next_sibling("td")
        if ("A" in move):
            for data in info.find_all('td')[0:7]:
                output.append(data.text.strip())
        elif ("B" in move):
            for data in info.find_all('td')[9:16]:
                output.append(data.text.strip())
        else:
            for data in info.find_all('td')[18:25]:
                output.append(data.text.strip())
    elif(not any(character.isdigit() for character in move)):
        move = "+".join(move)
        print(move)
        info = soup.find('small', text = move)
        info = info.parent
        info = info.find_next_sibling("td")
        for data in info.find_all('td')[0:7]:
            output.append(data.text.strip())
    else:
        info = soup.find('small', text = move)
        info = info.parent
        info = info.find_next_sibling("td")
        for data in info.find_all('td')[0:7]:
            output.append(data.text.strip())
    return output

#conditions for a normal are being one number and one letter or being 66 and a number
def is_normal(input):
    number_of_numbers = 0
    for char in input:
        if char.isdigit():
            number_of_numbers += 1
    if (number_of_numbers < 3 and "22" not in input and not (len(input) == 3 and "[" in input) and number_of_numbers != 0):
        return True
    else:
        return False