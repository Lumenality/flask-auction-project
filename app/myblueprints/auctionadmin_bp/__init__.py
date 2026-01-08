# myblueprints/bostader/__init__.py
"""
🏘️ AUKTIONS BLUEPRINT - Initialiseringsfil (Instruktioner för att starta den publika modulen)

SYFTE: Att definiera den publika delen av applikationen, som visar listor och detaljer
över tillgängliga auktioner för besökare.

SINGLE RESPONSIBILITY: Denna fil har ENDAST ansvar för:
1. Definiera auktions-blueprintet (Blueprint-objektet).
2. Importera nödvändiga resurser (auction_repo).
3. Importera routes (URL-hanterarna) som tillhör auktions-delen.

VIKTIGT OM IMPORTORDNING:
1. Blueprint-objektet (auctions_bp) måste skapas FÖRST.
2. Repository (auction_repo) måste importeras.
3. Routes-filen (auctions_routes) importeras SIST, eftersom den använder både auctions_bp och auction_repo.
"""
# Importera Blueprint-klassen från Flask
from flask import Blueprint

# ============================================================
# 1. SKAPA BLUEPRINTET
# ============================================================
auctionadmin_bp = Blueprint(
    'auctionadmin_bp',                       # Internt namn/identifierare. Används för url_for('auctionadmin_bp.hamta_lista').
    __name__,                         # Python-modulens namn. Säger var Flask ska leta efter resurser.
    template_folder='templates',      # Säger till Flask var HTML-mallarna för detta blueprint ligger.
    # OBS: Detta blueprint registreras ofta utan url_prefix i huvudappen för att vara startsidan.
)


# ============================================================
# 2. IMPORTERA REPOSITORY (Databaslagret)
# ============================================================
# Importerar den enda instansen av auction_repository. 
# Detta är nödvändigt för att routarna ska kunna hämta auktionsdata.
# ----sqlalchemy based repository----
from ...dbrepositories.auction_repository import auction_repo 

# ----sqlite based repository----
#from dbrepositories.sqlite_auction_repository import auction_repo


# ============================================================
# 3. IMPORTERA ROUTES (URL:er och logik)
# ============================================================
# Denna import MÅSTE vara sist!
# Filen 'bostader_routes.py' importerar och använder de objekt som definieras ovan.
#from . import bostader_routes