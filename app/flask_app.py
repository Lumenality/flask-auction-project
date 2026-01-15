from flask import Flask, flash, redirect, render_template, url_for
# from .database import init_db   # <- remove if not using Flask-SQLAlchemy
from flask_login import LoginManager, current_user, login_required
from flask_bcrypt import Bcrypt

def skapa_app():
    """
    Funktion som bygger och startar Flask-appen.

    Varför behövs detta?
    - Ger dig en tydlig plats där all konfiguration sker.
    - Gör det lätt att testa din kod (eller använda olika inställningar).
    """

    # Skapa själva Flask-applikationen
    app = Flask(__name__)

    # Initialize Bcrypt for password hashing
    bcrypt = Bcrypt(app)

    # SÄTT UPP APPENS INSTÄLLNINGAR
    app.config['SECRET_KEY'] = '86cff1dfb45dcaec470c4b3dfcfe6ee6'   # Behöv för att sessions/inloggning ska vara säkert
    app.config['DB_URI'] = 'sqlite:///auctions_sqlalchemy.db'  # Databasens plats
    # REGISTRERA MODULES (BLUEPRINTS)
    # Varje blueprint är en del av appen, t.ex. "bostäder" eller "admin".
    registrera_blueprints(app)

    # SKAPA DE VIKTIGA APP-ROUTES (t.ex. startsidan)
    create_routes(app)

    # SÄTT UPP INLOGGNING (Flask-Login)
    login_manager = LoginManager()
    login_manager.init_app(app)                     # Koppla till appen
    login_manager.login_view = 'login_bp.login'      # Var ska man hamna om man inte är inloggad?

    # Initialize Bcrypt for password hashing
    bcrypt = Bcrypt(app)

    @login_manager.user_loader
    def load_user(user_id):
        """
        Denna funktion frågar databasen efter en användare med det sparade ID:t.
        Flask-Login behöver denna funktion för att återkoppla sessions till rätt user.
        """
        from .myblueprints.login_bp.login_repository import UserRepository
        user_repo = UserRepository()

        return user_repo.find_by_id(int(user_id))

    return app

def registrera_blueprints(app):
    """
    Kopplar ihop alla dina olika moduler (blueprints) med huvudappen,
    så att rutterna och funktionerna de innehåller blir tillgängliga.
    """
    # Imports
    from .myblueprints.vue_frontend_bp.vue_frontend_bp import vue_frontend_bp
    from .myblueprints.auctions_bp_sqlalchemy.auctions_bp_sqlalchemy import auctions_bp_sqlalchemy
    from .myblueprints.auctions_bp_sqlalchemy.auctions_bp_rest import auctions_bp_rest
    from .myblueprints.auctions_bp_sqlalchemy.users_bp_rest import users_bp_rest
    from .myblueprints.login_bp.login_bp import login_bp, login_manager # this app is registered with the loginmanager above
    from .myblueprints.search_bp.search_bp import search_bp
    

    # Registration
    app.register_blueprint(vue_frontend_bp)
    app.register_blueprint(auctions_bp_sqlalchemy, url_prefix='/admin')
    app.register_blueprint(auctions_bp_rest, url_prefix='/api/v1/auctions')
    app.register_blueprint(users_bp_rest, url_prefix='/api/v1/users')
    app.register_blueprint(login_bp, url_prefix='/user')
    app.register_blueprint(search_bp, url_prefix='/search')

def create_routes(app):
    """
    Definierar rutterna som gäller hela appen (inte bara en modul).
    T.ex. startsidan och en test-rutt.
    """
    @app.route('/')
    def index():
        """Den första sidan man ser (startsidan)."""
        return redirect(url_for('vue_frontend_bp.vue_frontend'))
    
    @app.route('/admin')
    @login_required
    def admin():
        """En enkel admin-sida."""
        if current_user.is_admin:
            return render_template('home_admin.html', titel='Admin-sida')
        else:
            flash("You must be logged in as admin to access this page.", "error")
            return redirect(url_for('login_bp.login'))


# HÄR STARTAS APPEN
app = skapa_app()

if __name__ == '__main__':
    # Kör appen (sätter igång den). Du ser nu debug-meddelanden och sidan laddas om automatiskt när du sparar kod.
    app.run(debug=True)