from urllib.request import urlopen as uReq, Request
from bs4 import BeautifulSoup as soup
import re
print('INSTRUCTIONS')
print("Have a .txt file near this one that contains any number of addresses you want tract codes for.")
print('Have each address be on a new line.')
print('The address you type in the next line should look similar to this: /Users/frankie/Documents/freelance/address_list.txt')
address_file = input('type in the path for the file containing your list of addresses: ')
with open(address_file) as f:
    lines = f.readlines()


def tract_code_finder(full_address):
    full_address = full_address.strip()
    address, city, state_zip_code = full_address.split(', ')
    state, zip_code = state_zip_code.split(' ') # AS LONG AS STATE NAME IS NOT 2 WORDS
    #House number & Street name
    address = address.replace(' ', '%20')
    #City
    city = city.replace(' ', '%20')
    #State
    state = state.replace(' ', '%20')
    #Zip Code
    zip_code = zip_code.replace(' ', '%20')
    url = f'https://geocoding.geo.census.gov/geocoder/geographies/address?street={address}&city={city}&state={state}&zip={zip_code}&benchmark=4&vintage=4'

    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=hdr)
    UClient = uReq(req)
    page_html = UClient.read()
    UClient.close()
    page_soup = soup(page_html, "html.parser")
    values = page_soup.findAll('div')

    pre_info = list(values[19])
    info = []
    for i in pre_info:
        info.append(str(i))

    #print(info)
    index_tract_code = info.index('<span class="resultItem">TRACT CODE: </span>')
    #print(index_tract_code)
    tract_code = info[index_tract_code+1]
    #print(info[index_tract_code])

    return f'{full_address} : {tract_code}'


for addy in lines:
    print(tract_code_finder(addy))


#go = True
#print('Please format the addresses with abbrevated state names and correct commas')
#while go:
#    address = input('type in an address: ')
#    try:
#        print(tract_code_finder(address))
#        keep_on = input('are there any more addresses (y/n)? ')
#        if keep_on == 'n':
#            go = False
#    except Exception:
#        print('Please re-enter the address and check the formatting')