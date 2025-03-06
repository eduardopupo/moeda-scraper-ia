from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

CSV_FILE = "taxas_cambio_historico.csv"

@app.route('/')
def index():
    if not os.path.exists(CSV_FILE):
        return "Arquivo de dados não encontrado.", 404

    df = pd.read_csv(CSV_FILE)
    
    # Gerar gráfico interativo com Plotly
    fig = px.line(
        df,
        x="Data",
        y="Taxa",
        color="Moeda",
        title="Evolução das Taxas de Câmbio"
    )
    
    # Converta o gráfico para HTML
    graph_html = fig.to_html(full_html=False)
    
    return render_template('dashboard.html', graph_html=graph_html)

@app.route('/cotacoes', methods=['GET'])
def get_cotacoes():
    if not os.path.exists(CSV_FILE):
        return jsonify({"error": "Arquivo de dados não encontrado."}), 404
    
    df = pd.read_csv(CSV_FILE)
    dados = df.to_dict(orient='records')
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True)