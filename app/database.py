from flask_sqlalchemy import SQLAlchemy

# Skapa en SQLAlchemy-instans.
# Detta objekt 'db' är gränssnittet mellan din kod och databasen.
# Alla modell-klasser som t.ex. Maklare, Bostad, User kommer använda 'db' för att definiera sina tabeller.
db = SQLAlchemy()

def init_db(app):
    """
    Förbereder och startar databasen i din Flask-applikation.

    Varför behövs detta?
    1. Flask och SQLAlchemy måste kopplas ihop så att rätt inställningar används (t.ex. adress till databasen).
    2. Tabellerna för alla dina modeller måste skapas (om de inte redan finns).
    3. Du kan välja att direkt fylla tabellerna med startdata när du kör appen första gången.

    Args:
        app: Din Flask-applikation (det objekt du skapar med app = Flask(__name__)).
    """

    # Kopplar ihop databas-objektet (db) med Flask-applikationen.
    # Gör att 'db' kan läsa t.ex. databas-URL från Flask-config.
    db.init_app(app)

    # Skapar ett app-context. Det är som att "aktivera" Flask-världen,
    # vilket krävs när man ska ändra saker i databasen (ex. skapa tabeller).
    with app.app_context():
        # --- Modell-import ---
        # Viktigt! SQLAlchemy måste veta vilka modeller som finns innan tabeller kan skapas.
        # Genom att importera modellklasserna, registreras de hos SQLAlchemy.
        from .models.auction import Auction           # Auktion-tabellen

        # --- Tabellskapande ---
        # db.create_all(): Skapar tabeller i databasen utifrån de modeller som är importerade.
        # Om tabeller redan finns, händer inget (det är säkert att köra).
        db.create_all()

        # --- Startdata / Seeding ---
        # Här importeras funktioner som lägger till startdata i databasen, ex. några mäklare och bostäder.
        # OBS! Startdata är valfritt, men bra för att kunna börja testa appen med något innehåll.
        from .models.auction import create_start_auctions

        # Kör startdata-funktionerna så de fyller på med initial data.
        create_start_auctions()

        # Nu är databasen klar att användas med Flask och alla tabeller är upprättade & fyllda med startdata.