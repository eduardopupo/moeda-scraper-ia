from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

CSV_FILE = "taxas_cambio_historico.csv"

@app.route('/cotacoes', methods=['GET'])
def get_cotacoes():
    if not os.path.exists(CSV_FILE):
        return jsonify({"error": "Arquivo de dados não encontrado."}), 404
    
    df = pd.read_csv(CSV_FILE)
    dados = df.to_dict(orient='records')
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True)
