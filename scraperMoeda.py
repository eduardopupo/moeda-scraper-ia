import requests
import pandas as pd
import logging
import os
from datetime import date, datetime, timedelta
from sklearn.ensemble import IsolationForest
import api

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

        print("------------------\nIniciando Execução\n------------------")
        url = f"https://api.exchangeratesapi.io/latest?base=EUR&symbols=USD,GBP,JPY,BRL&access_key={api.api_key}" #"ocultei" pelo arquivo api.py
        try:
            response = requests.get(url)
            data = response.json()

            if "rates" in data:
                rates = data['rates']
                self.print_rates(rates)
                self.salvar_dados(rates)
                self.detectar_variacao(rates)
            else:
                logging.error("Resposta da API não contém as taxas de câmbio.")
                print("Erro: Dados de taxa não encontrados.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisição API: {e}")
            print(f"Erro na requisição API: {e}")

    def print_rates(self, rates):
        for currency, rate in rates.items():
            print(f"{currency}: {rate:.4f}")

    def salvar_dados(self, rates):
        hoje = datetime.today().strftime('%Y-%m-%d')
        arquivo_csv = f"taxas_cambio_{hoje}.csv"

        df = pd.DataFrame(rates.items(), columns=["Moeda", "Taxa"])
        df.to_csv(arquivo_csv, index=False)
        print(f"Dados salvos em {arquivo_csv}\nCâmbio: Euro")
        logging.info(f"Dados de câmbio para EUR: {rates}")
        
        print("\nDados de Câmbio Salvos:")
        print(df.to_string(index=False))

    def detectar_variacao(self, rates):
        try:
            df_antigo = pd.read_csv("taxas_cambio_historico.csv")
        except FileNotFoundError:
            df_antigo = pd.DataFrame(columns=["Moeda", "Taxa"])

        hoje = datetime.today().strftime('%Y-%m-%d')
        novo_df = pd.DataFrame(rates.items(), columns=["Moeda", "Taxa"])
        novo_df["Data"] = hoje
        df_antigo = pd.concat([df_antigo, novo_df])

        df_antigo.to_csv("taxas_cambio_historico.csv", index=False)

        modelo = IsolationForest(contamination=0.1)
        variacao = modelo.fit_predict(df_antigo[["Taxa"]])

        df_antigo["Variação"] = variacao
        anomalies = df_antigo[df_antigo["Variação"] == -1]

        if len(anomalies) > 0:
            logging.warning(f"Variações significativas detectadas nas taxas de câmbio:\n{anomalies}")
            print(f"Variações significativas detectadas:\n{anomalies}")
        else:
            logging.info("Nenhuma variação significativa detectada.")
            print("Nenhuma variação significativa detectada.")


if __name__ == '__main__':
    Main().executar()