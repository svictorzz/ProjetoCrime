import pymongo
from flask import Flask, jsonify, request, render_template
from flask_ngrok import run_with_ngrok

# Conexão com MongoDB Atlas
client = pymongo.MongoClient("mongodb+srv://scrumTeam:OsRV9Q3IUvdoGOZt@clusteres3.lj0e2.mongodb.net/?retryWrites=true&w=majority&appName=clusterES3")
db = client['seguranca_cidade'] 
locais_collection = db['locais']  

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inserir_dados', methods=['POST'])
def inserir_dados():
    locais_collection.insert_many([
        {"nome": "Centro", "bairro": "Centro", "regiao": "Central", "incidencia": {"roubo": 20, "furto": 10, "assalto": 5, "estelionato": 3, "sequestro": 1}},
        {"nome": "Zona Norte", "bairro": "Santana", "regiao": "Norte", "incidencia": {"roubo": 15, "assalto": 5, "furto": 7, "estelionato": 4, "homicidio": 2}},
        {"nome": "Zona Sul", "bairro": "Vila Mariana", "regiao": "Sul", "incidencia": {"roubo": 8, "furto": 12, "assalto": 3, "trafico": 2, "sequestro": 0}},
        {"nome": "Zona Leste", "bairro": "Mooca", "regiao": "Leste", "incidencia": {"roubo": 25, "furto": 20, "assalto": 10, "estelionato": 5, "homicidio": 1}},
        {"nome": "Zona Oeste", "bairro": "Pinheiros", "regiao": "Oeste", "incidencia": {"roubo": 18, "furto": 9, "assalto": 4, "trafico": 1, "sequestro": 2}},
        {"nome": "Jardins", "bairro": "Jardins", "regiao": "Central", "incidencia": {"roubo": 3, "furto": 1, "assalto": 2, "estelionato": 1, "homicidio": 0}},
        {"nome": "Itaim Bibi", "bairro": "Itaim", "regiao": "Central", "incidencia": {"roubo": 5, "furto": 4, "assalto": 3, "trafico": 0, "sequestro": 1}},
        {"nome": "Brás", "bairro": "Brás", "regiao": "Leste", "incidencia": {"roubo": 12, "furto": 15, "assalto": 8, "estelionato": 3, "homicidio": 0}},
        {"nome": "Liberdade", "bairro": "Liberdade", "regiao": "Central", "incidencia": {"roubo": 2, "furto": 6, "assalto": 1, "trafico": 4, "sequestro": 0}},
        {"nome": "Vila Madalena", "bairro": "Vila Madalena", "regiao": "Oeste", "incidencia": {"roubo": 7, "furto": 5, "assalto": 6, "estelionato": 2, "homicidio": 1}}
    ])
    return jsonify({"status": "dados inseridos"}), 200


@app.route('/pesquisar', methods=['GET'])
def pesquisar_crimes():
    tipo_crime = request.args.get('tipo')
    # Busca locais com base no tipo de crime
    resultados = locais_collection.find({"incidencia." + tipo_crime: {"$exists": True}}).sort("incidencia." + tipo_crime, -1)
    locais = [{"nome": local["nome"], "bairro": local["bairro"], "regiao": local["regiao"], "incidencia": local["incidencia"][tipo_crime]} for local in resultados]
    return jsonify(locais), 200

if __name__ == '__main__':
    app.run(debug=True)