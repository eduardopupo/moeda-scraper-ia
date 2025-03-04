import requests
import pandas

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
            print(rates)
            
        else:
            print("Falha ao conectar na API")




if __name__ == '__main__':
    Main().executar()