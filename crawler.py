from fints.client import FinTS3PinTanClient
import time
from datetime import datetime
from functions import *

def main():
    config = load_config('config.json')
    
    timestamp = datetime.today().strftime('%d.%m.%Y - %H:%M')

    for entry in config['accounts_nr'].items():
        f = FinTS3PinTanClient(entry[1]['blz'], entry[1]['nr'], entry[1]['pass'], 'https://fints.ing-diba.de/fints/')
        accountList = f.get_sepa_accounts()
        for account in accountList:
            if account.accountnumber in config['depots_nr']:
                accountholdings = f.get_holdings(account)
                for accountholding in accountholdings:
                    save_db(timestamp, entry[1]['name'], accountholding.ISIN, accountholding.name, accountholding.market_value, accountholding.value_symbol, accountholding.pieces, accountholding.total_value, accountholding.acquisitionprice)
                    print(timestamp)

if __name__ == '__main__':
    while True:
        main()
        time.sleep(7200)
