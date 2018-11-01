from fints.client import FinTS3PinTanClient
import time
from datetime import datetime
from functions import *
import requests
import json

def main():
    config = load_config('config.json')
    
    timestamp = datetime.today().strftime('%d.%m.%Y - %H:%M')

    for entry in config['accounts_nr'].items():
        #Mit Konto verbinden
        try:
            f = FinTS3PinTanClient(entry[1]['blz'], entry[1]['nr'], entry[1]['pass'], 'https://fints.ing-diba.de/fints/')
        
        except:
            #If connection not working wait a bit and try again. Better solution later...
            time.sleep(300)
            f = FinTS3PinTanClient(entry[1]['blz'], entry[1]['nr'], entry[1]['pass'], 'https://fints.ing-diba.de/fints/')

        #Konten abrufen
        accountList = f.get_sepa_accounts()
        for account in accountList:
            #Wenn das Konto ein Depot ist:
            if account.accountnumber in config['depots_nr']:
                accountholdings = f.get_holdings(account)
                #Für jede Position die aktuellen Werte abrufen
                for accountholding in accountholdings:
                    save_db(timestamp, entry[1]['name'], accountholding.ISIN, accountholding.name, accountholding.market_value, accountholding.value_symbol, accountholding.pieces, accountholding.total_value, accountholding.acquisitionprice)
                    print(timestamp)

    #Add Bitcoin holdings
    lastBTCPrice = 0
    BTCAmount = float(config['BTCAmount'][0])
    try:
        r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json', timeout=10)
        BTCPrice = json.loads(r.text)['bpi']['EUR']['rate_float']
        lastBTCPrice = BTCPrice
        save_db(timestamp, 'Gemeinschaftskonto', 'BTC', 'BTC', BTCPrice, 'EUR', BTCAmount, BTCPrice * BTCAmount, 4400)

    except requests.exceptions.RequestException as e:
        save_db(timestamp, 'Gemeinschaftskonto', 'BTC', 'BTC', lastBTCPrice, 'EUR', BTCAmount, lastBTCPrice * BTCAmount, 4400)
        print(e)

if __name__ == '__main__':
    while True:
        main()
        time.sleep(3600)
