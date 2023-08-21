import os
from tabulate import tabulate
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import re
import time

def clear():
    os.system('clear')

WEBSITES_LIST = [
    ['0', 'https://dl2.pesfa.com/pesfa'],
    ['1', 'http://b1g-arch1ve.buho.ch'],
    ['2', 'https://lira.epac.to/DOCS-TECH']
]

OTHER_COMMANDS = ['menu','exit', 'prev']

colors = {
    'red': "\033[1;31;48m",
    'green': "\033[1;32;48m",
    'yellow': "\033[1;33;48m",
    'blue': "\033[1;36;48m",
    'white': "\033[1;37;48m",
}

def app_title():
    clear()
    print(colors['green']+'########################################################')
    print('▒█▀▀▀█ ▒█▀▀▀ ▒█░░▒█ ▒█▀▀▀ ▒█▀▀█ ▒█░▒█ ▒█▀▀▀█ ')
    print('░▀▀▀▄▄ ▒█▀▀▀ ░▒█▒█░ ▒█▀▀▀ ▒█▄▄▀ ▒█░▒█ ░▀▀▀▄▄ ')
    print('▒█▄▄▄█ ▒█▄▄▄ ░░▀▄▀░ ▒█▄▄▄ ▒█░▒█ ░▀▄▄▀ ▒█▄▄▄█')
    print('########################################################\n')
    print('⚫ ℂ 𝕣 𝕖 𝕒 𝕥 𝕖 𝕕  𝕓 𝕪  𝔻 𝔸 ℝ 𝕂  𝕊 𝕀 𝔽 𝔸 𝕃 - 2023')
    print(colors['white'])
    print('This tool allows you to list and download files or archives from free download websites !')
    print('Before using the tool, please activate your VPN to secure your downloads.')
    print('There are several available free download websites on which you can list downloadable files.')
    print('You will have to pick one to start the listing or downloading process.')
    print('\n')

def app_options():
    print(colors['green']+'------------------------------------------')
    print('> INSTRUCTIONS')
    print('------------------------------------------'+colors['white'])
    print('Here is the complete list of available commands :')
    print('['+colors['yellow']+'stop'+colors['white']+'] - Go back to the website selection menu')
    print('['+colors['yellow']+'exit'+colors['white']+'] - Stop the application')
    print('['+colors['yellow']+'prev'+colors['white']+'] - Go back to previous directory')
    print('\n')

def app_menu():
    print(colors['green']+'------------------------------------------')
    print('> WEBSITE SELECTION')
    print('------------------------------------------'+colors['white'])
    print (tabulate(WEBSITES_LIST, headers=["ID", "Website"], tablefmt='psql'))
    choice = input('Which one do you choose ? : ')
    while not choice.isdigit() or (int(choice) not in range(0, (len(WEBSITES_LIST)))):
        print(colors['red']+'Error ! This choice is not acceptable !')
        choice = input(colors['white']+'Which website do you choose ? : ')
    url = WEBSITES_LIST[int(choice)][1]
    print(colors['green']+'=> '+url+' SELECTED !'+colors['white'])
    process(url)

# Function for b1g-arch1ve website using
def process(url):
    select = 0
    while select not in OTHER_COMMANDS:
        results = navigation(url)
        select = results['select']
        url = results['url']

    # Other commands
    if select == 'menu':
        print(colors['green']+'Going back to website selection menu ...'+colors['white'])
        time.sleep(1)
        clear()
        app_menu()
    elif select == 'exit':
        print(colors['green']+'Goodbye ! ;)'+colors['white'])
        time.sleep(1)
        clear()
        exit()
    elif select == 'prev':
        print(colors['green']+'Going back to previous directory ...'+colors['white'])
        rsplit = url.rsplit('/',1)
        url = rsplit[0]
        time.sleep(1)
        clear()
        process(url)

def navigation(url):
    links = navigate(url)
    select = show_table(links)
    if select not in OTHER_COMMANDS:
        selected_link = links[int(select)][0]
        if is_directory(selected_link):
            print(colors['green']+'Moving to '+colors['blue']+selected_link+colors['green']+' directory ...'+colors['white'])
            directory = selected_link[:-1]
            directory = quote(directory)
            url = url + '/' + directory

        elif is_previous_directory(selected_link):
            print(colors['green']+'Going back to previous directory ...'+colors['white'])
            rsplit = url.rsplit('/',1)
            url = rsplit[0]
        else:
            download_file(selected_link, url)
        time.sleep(1)
        clear()
    values = {'url':url,'select':select}
    return values

def download_file(filename, url):
    print('['+colors['yellow']+'WARNING'+colors['white']+'] You have selected a file !')
    confirmation = input('Would you like to download it ? (y/n) : ')
    while confirmation not in ['y','Y','n','N']:
        print(colors['red']+'Error ! Your answer is not correct !'+colors['white'])
        confirmation = input('Would you like to download the selected file ? (y/n) : ')
    if confirmation in ['y','Y']:
        filepath = url + '/' + quote(filename)
        file_extension = filename.split('.')
        os.system('mkdir -p downloads/'+file_extension[1])
        os.system('wget '+filepath+' -P downloads/'+file_extension[1]+'/')
    print(colors['green']+'File downloaded successfully !'+colors['white'])

# Getting filename from cd
def get_filename_from_cd(cd):
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


# Moving to another url
def navigate(url):
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "html.parser")
    all_links = soup.findAll('a')
    links = links_list(all_links)
    links = links[4:]
    return links

# Displaying styled table
def show_table(links):
    table = tabulator(links)
    print (tabulate(table, headers=["ID", "Link", "Type"], tablefmt='psql'))
    select = input('Select one link by entering the ID : ')
    while (select.isdigit() and int(select) not in range(0, len(links))) or (not select.isdigit() and select not in OTHER_COMMANDS):
        print(colors['red']+'Error ! This link ID doesn\'t exist !')
        select = input(colors['white']+'Select another one : ')
    return select

def is_directory(link):
    if '/' in link:
        return True
    return False

def is_previous_directory(link):
    if link.replace(' ','_').lower() == 'parent_directory':
        return True
    return False

# Creating a list containing links
def links_list(bs4_elements):
    a_list = []
    index = 0
    for item in bs4_elements:
        a_list.insert(index, item.contents)
        index += 1
    return a_list

# Making a styled table with links list
def tabulator(elements):
    table = []
    for index,element in enumerate(elements):
        link_type = 'file'
        # If element contains a slash
        if is_directory(element[0]) or is_previous_directory(element[0]):
            link_type = 'directory'
            label = colors['blue']+element[0]+colors['white']
        else:
            label = colors['yellow']+element[0]+colors['white']
        table.append([index, label, link_type])
    return table

app_title()
app_options()
app_menu()