from flask import Flask, render_template
from .database import init_db    # För att koppla ihop appen med databasen
from flask_login import LoginManager   # Enkelt sätt att hantera inloggning
from .models.user import User           # Modellen för användare (behövs av Flask-Login)

def skapa_app():
    """
    Funktion som bygger och startar Flask-appen.

    Varför behövs detta?
    - Ger dig en tydlig plats där all konfiguration sker.
    - Gör det lätt att testa din kod (eller använda olika inställningar).
    """

    # Skapa själva Flask-applikationen
    app = Flask(__name__)

    # SÄTT UPP APPENS INSTÄLLNINGAR
    app.config['SECRET_KEY'] = '86cff1dfb45dcaec470c4b3dfcfe6ee6'   # Behöv för att sessions/inloggning ska vara säkert
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auctionsite.db'  # Pekar ut vilken databas som ska användas
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # Spara minne och processorkraft

    # KOPPLA APPEN TILL DATABASEN & SKAPA TABELLER
    init_db(app)

    # REGISTRERA MODULES (BLUEPRINTS)
    # Varje blueprint är en del av appen, t.ex. "bostäder" eller "admin".
    registrera_blueprints(app)

    # SKAPA DE VIKTIGA APP-ROUTES (t.ex. startsidan)
    create_routes(app)

    # SÄTT UPP INLOGGNING (Flask-Login)
    login_manager = LoginManager()
    login_manager.init_app(app)                     # Koppla till appen
    login_manager.login_view = 'auth_bp.login'      # Var ska man hamna om man inte är inloggad?

    @login_manager.user_loader
    def load_user(user_id):
        """
        Denna funktion frågar databasen efter en användare med det sparade ID:t.
        Flask-Login behöver denna funktion för att återkoppla sessions till rätt user.
        """
        return User.query.get(int(user_id))

    return app

def registrera_blueprints(app):
    """
    Kopplar ihop alla dina olika moduler (blueprints) med huvudappen,
    så att rutterna och funktionerna de innehåller blir tillgängliga.
    """
    # Imports
    from .myblueprints.auctions_bp.auctions_bp import auctions_bp
    from .myblueprints.auctionadmin_bp.auctionadmin_bp import auctionadmin_bp

    # Registration
    app.register_blueprint(auctions_bp, url_prefix='/auctions')
    app.register_blueprint(auctionadmin_bp, url_prefix='/auctionadmin')

def create_routes(app):
    """
    Definierar rutterna som gäller hela appen (inte bara en modul).
    T.ex. startsidan och en test-rutt.
    """

    @app.route("/hello")
    def hello_world():
        """Testar att allt fungerar."""
        return "<p>Hej Världen! Min första Flask-app!</p>"

    @app.route('/')
    def index():
        """Den första sidan man ser (startsidan)."""
        # 'home.html' ska ligga i mappen 'templates' i projektroten.
        return render_template('home.html', titel='Välkommen')

# HÄR STARTAS APPEN
app = skapa_app()

if __name__ == '__main__':
    # Kör appen (sätter igång den). Du ser nu debug-meddelanden och sidan laddas om automatiskt när du sparar kod.
    app.run(debug=True)