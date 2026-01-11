from flask import Blueprint, jsonify, render_template, request
import json
import os

auctions_rest_bp = Blueprint('auctions_rest_bp', __name__,template_folder='templates', static_folder='static')# use this variable in flask_app.py, look how import and register this blueprint
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

#------------- add auction to json file --------------
@auctions_rest_bp.route('/', methods=['POST'])#https://localhost:5000/api/v1/auctions/
def add_auction():
    # Läs in från JSON-filen till en lista
    fileObject = open(AUCTIONS_FILE, "r")
    auctions = json.load(fileObject)
    print(auctions)
    fileObject.close()

    # läser in om det kommer från HTML formulär
    if(request.form):
        data = request.form

    # läs in om det kommer som json
    content_type = request.headers.get('Content-Type')
    if(content_type == 'application/json'):
        data = request.json

    # check if id already exists
    for auction in auctions:
        if auction['id'] == data['id']:
            return jsonify({'error': 'Auktion med detta ID finns redan'}), 400 # HTTP status code 400 means bad request
        
    # skapa en dict med person data
    new_auction = {
        'id': data['id'],
        'description': data['description'],
        'starting_bid': data['starting_bid'],
        'duration': data['duration'],
        'image_url': data['image_url']
    }
    #appenda dict till listan
    auctions.append(new_auction)
    print(auctions)
    # gör om listan till json sträng, med indentering 2
    jsonString = json.dumps(auctions, indent=2)
    jsonFile = open(AUCTIONS_FILE, "w")
    # skriv json strängen till fil
    jsonFile.write(jsonString)
    jsonFile.close()
    # skapar en dict som skickas tillbaka som json sträng
    return jsonify(new_auction), 201 # HTTP status code 201 means created

@auctions_rest_bp.route('/<int:auction_id>', methods=['DELETE'])#https://localhost:5000/api/v1/auctions/1
def delete_auction(auction_id):
    #läs in från JSON-filen till en lista
    fileObject = open(AUCTIONS_FILE, "r")
    jsonContent = fileObject.read()
    fileObject.close()
    auctions = json.loads(jsonContent)
    # loopa auctions listan och ta bort den med rätt id
    index=0
    deleted_auction = {}
    for auction in auctions:
        if auction['id'] == auction_id:
            deleted_auction = auction
            del auctions[index]
            break
        index += 1
    # skriv tillbaka till filen
    jsonString = json.dumps(auctions, indent=2)
    jsonFile = open(AUCTIONS_FILE, "w")
    jsonFile.write(jsonString)
    jsonFile.close()
    return jsonify(deleted_auction), 200 # HTTP status code 200 means OK

@auctions_rest_bp.route('/<int:auction_id>', methods=['PUT'])#https://localhost:5000/api/v1/auctions/1
def update_auction(auction_id):
    #läs in från JSON-filen till en lista
    fileObject = open(AUCTIONS_FILE, "r")
    jsonContent = fileObject.read()
    fileObject.close()
    #gör om JSON-strängen till en lista med dicts i
    auctions = json.loads(jsonContent)
    # loopa igenom lista för att finna den som skall uppdateras
    auction_updated = {}
    for auction in auctions:
        if auction['id'] == auction_id:
            #kom ihåg postman att ta raw och skicka som det description json {"description": "Mona Lisa"}
            #läser in det skickade id datat och byter ut det för den funna auktionen
            content_type = request.headers.get('Content-Type')
            if (content_type == 'application/json'):
                auction["description"]=request.json["description"]
                auction["starting_bid"]=request.json["starting_bid"]
                auction["duration"]=request.json["duration"]
                auction["image_url"]=request.json["image_url"]
            #om det postas som formulär
            if (request.form):
                # läser in det från formuläret skickade namn datat, byter ut det för den funna personen
                auction["description"]=request.form.get("description")
                auction["starting_bid"]=request.form.get("starting_bid")
                auction["duration"]=request.form.get("duration")
                auction["image_url"]=request.form.get("image_url")
            auction_updated = auction
            break

    # gör om lista till jsonsträng
    jsonString = json.dumps(auctions, indent=2)
    # skriv json strängen till fil
    jsonFile = open(AUCTIONS_FILE, "w")
    #skriv tillbaka till fil
    jsonFile.write(jsonString)
    jsonFile.close()
    return jsonify(auction_updated), 200 # HTTP status code 200 means OK

#------------- återställ json med ursprungsdata --------------
@auctions_rest_bp.route('/reset', methods=['POST'])#https://localhost:5000/api/v1/auctions/reset
def reset_auctions_json():
    original_auctions = [
        {
            "id": 1,
            "description": "Skriet",
            "starting_bid": 5,
            "duration": 7,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/The_Scream.jpg/256px-The_Scream.jpg?20160501101333"
        },
        {
            "id": 2,
            "description": "Mona Lisa",
            "starting_bid": 10,
            "duration": 7,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Mona_Lisa.jpg/256px-Mona_Lisa.jpg?20100608143407"
        }
    ]
    jsonString = json.dumps(original_auctions, indent=2)
    jsonFile = open(AUCTIONS_FILE, "w")
    jsonFile.write(jsonString)
    jsonFile.close()
    return jsonify({'message': 'Auktionsdata återställd'}), 200 # HTTP status code 200 means OK

@auctions_rest_bp.route('/vueauctions', methods=['GET'])
def showvue():
    """Visar sidan som använder Vue.js för att hämta och visa auktioner."""
    # 'vue_auctions.html' ska ligga i mappen 'templates' i projektroten.
    return render_template('auctions_vue.html', titel='Auktioner med Vue.js')