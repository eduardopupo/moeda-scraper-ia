import requests
import pandas as pd
import logging
import os
from datetime import date, datetime, timedelta

log_directory = r'C:\\Users\\Eduardo\\OneDrive\\Documentos\\Portfolio\\logs' 
log_filename = os.path.join(log_directory, 'scraperMoeda.log')
logging.basicConfig(
   filename=log_filename,
   level=logging.INFO, 
   format='%(asctime)s - %(levelname)s - %(message)s',
   datefmt='%Y-%m-%d %H:%M:%S'
)

class Main():

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def executar(self):

        api_key = '3465a40fa027044d680948a265576559'
        url = f"https://api.exchangeratesapi.io/latest?base=EUR&symbols=USD,GBP,JPY,BRL&access_key={api_key}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rates = data['rates']
            #print(rates)

            for currency, rate in rates.items():
                moeda = ({f"{currency}: {rate:.4f}"})
                print(", ".join(map(str, moeda)))
        
        else:
            if "error" in data:
                print(f"Erro na API: {data['error']['info']}")
                return
        dataFrame(rates)
            
def dataFrame(rates):

    df = pd.DataFrame(rates.items(), columns=["Moeda", "Taxa"])
    df.to_csv("taxas_cambio.csv", index=False)
    print("Dados salvos em taxas_cambio.csv\nCâmbio: Euro")
    df = pd.read_csv("taxas_cambio.csv")
    print(df)
    logging.info(df)




if __name__ == '__main__':
    Main().executar()