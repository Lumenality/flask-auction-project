from flask import Blueprint, jsonify, request
import json
import os

auctions_rest_bp = Blueprint('auctions_rest_bp', __name__)# use this variable in flask_app.py, look how import and register this blueprint
#templates is in the main template folder

# Get the directory of the current script
BLUEPRINT_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the path to the auctions.json file
AUCTIONS_FILE = os.path.join(BLUEPRINT_DIR, 'auctions.json')

#------------- get all auctions --------------
@auctions_rest_bp.route('/', methods=['GET'])#https://localhost:5000/api/v1/auctions/
def getauctions_jsonlist():
    """
    Hämtar alla auktioner i databasen och returnerar dem som en JSON-lista.
    """
    fileObject = open(AUCTIONS_FILE, "r") # Öppna filen i läsläge
    jsonContent = fileObject.read() # Läs in hela filens innehåll
    # json string till lista
    auctions = json.loads(jsonContent) #Gör om JSON-strängen till en Python-lista
    fileObject.close() # Stäng filen


    return jsonify(auctions), 200 # Returnerar JSON-listan med HTTP-statuskod 200 (OK)

#------------- get auction by id --------------
@auctions_rest_bp.route('/<int:auction_id>', methods=['GET'])#https://localhost:5000/api/v1/auctions/1
def getauction_byid(auction_id):
    """
    Hämtar en specifik auktion baserat på dess ID och returnerar den som JSON.
    """
    fileObject = open(AUCTIONS_FILE, "r") # Öppna filen i läsläge
    jsonContent = fileObject.read() # Läs in hela filens innehåll
    auctions = json.loads(jsonContent) #Gör om JSON-strängen till en Python-lista
    fileObject.close() # Stäng filen

    # Leta efter auktionen med det angivna ID:t
    for auction in auctions:
        if auction['id'] == auction_id:
            return jsonify(auction), 200 # Returnerar auktionen som JSON med HTTP-statuskod 200 (OK)

    # Om auktionen inte hittas, returnera ett felmeddelande
    return jsonify({'error': 'Auktion inte hittad'}), 404 # HTTP-statuskod 404 (Not Found)