# dbrepositories/bostad_repository.py
"""
🏠 BOSTAD REPOSITORY - Ansvarar för ALL databasåtkomst för bostäder.

DETTA ÄR ETT DESIGNMÖNSTER (Repository Pattern / Data Access Layer):
Syftet är att isolera logiken för hur man pratar med databasen (t.ex. SQL-frågor)
från resten av applikationen (t.ex. webbroutning, användargränssnitt).

SINGLE RESPONSIBILITY (Enkelt ansvar): Denna fil har ENDAST ansvar för:
- Hämta data från databasen (READ/Hämta)
- Lägga till ny data (CREATE/Skapa)
- Uppdatera befintlig data (UPDATE/Uppdatera)
- Ta bort data (DELETE/Radera)

Viktigt: Denna fil känner INTE till routing, HTML, eller JSON!
Den är ENDAST fokuserad på att prata med databasen (CRUD-operationerna).
"""

# Importera Auction-modellen (klassen som representerar tabellen 'auction' i databasen)
from ..models.auction import Auction
# Importera databasobjektet (ofta en instans av SQLAlchemy) för att hantera sessioner
from ..database import db


class AuctionRepository:
    """
    Repository-klass för Auction.
    Innehåller alla databasoperationer (CRUD = Create, Read, Update, Delete).
    Denna klass fungerar som en 'butler' som sköter kommunikationen med databasen
    åt resten av applikationen.
    """

    def hamta_alla(self):
        """
        Hämtar ALLA bostäder från databasen.
        Använder SQLAlchemy:s query-system för att göra en 'SELECT * FROM bostad'.

        Returns:
            list: En lista med alla Auction-objekt. Varje objekt motsvarar en rad i tabellen.
        """
        # Auction.query är basfrågan, .all() exekverar frågan och returnerar resultaten som en lista.
        return Auction.query.all()

    def hamta_en(self, auction_id):
        """
        Hämtar EN specifik auktion baserat på dess primärnyckel (ID).

        Args:
            auction_id (int): ID för auktionen (Primärnyckel i databasen)

        Returns:
            Auction: Auction-objektet om det hittas, eller None om ID:t inte existerar.
        """
        # .get(id) är en snabb metod för att hämta en rad baserat på dess Primärnyckel.
        return Auction.query.get(auction_id)

    def hamta_eller_404(self, auction_id):
        """
        Hämtar EN auktion eller utlöser ett 404-fel (Not Found).
        Denna metod är användbar i webbapplikationer där du vill att servern ska
        krascha snyggt med ett 404 om resursen inte finns.

        Args:
            auction_id (int): ID för auktionen

        Returns:
            Bostad: Bostad-objektet (Garanterat att existera)

        Raises:
            404: Om bostaden inte hittas, utlöses ett Flask/webb-fel.
        """
        # .get_or_404(id) är en Flask-SQLAlchemy-funktion som automatiserar felhanteringen.
        return Auction.query.get_or_404(auction_id)

    def skapa_ny(self, data):
        """
        Skapar en NY auktion i databasen (INSERT-operation).
        Args:
            data (dict): En Python Dictionary som innehåller fälten (adress, stad, pris, etc.)
                         som ska sparas i den nya auktionen.

        Returns:
            Auction: Den nya Auction-instansen som skapades och sparades.
        """
        # Skapa en ny instans av Auction-modellen baserat på datan i dictionaryn.
        new_auction = Auction(
            description=data['description'],
            starting_bid=data['starting_bid'],
            auction_duration=data['auction_duration'],
            image_url=data.get('image_url')
            # Använder .get() med standardvärde för att hantera frivilliga fält (för att undvika KeyError)

        )

        # 1. Lägg till i session: Förbereder objektet för att sparas i databasen
        #    ('Staging' i en temporär buffert).
        db.session.add(new_auction)
        # 2. Spara/Committa: Utför den faktiska INSERT-frågan till databasen
        #    och gör ändringen permanent.
        db.session.commit()

        return new_auction

    def uppdatera(self, auction_id, data):
        """
        Uppdaterar en BEFINTLIG auction (UPDATE-operation).

        Args:
            auction_id (int): ID för auktionen att uppdatera
            data (dict): Ny data att skriva över den gamla med.

        Returns:
            Auction: Den uppdaterade auktionen, eller None om den inte fanns (och därmed inte uppdaterades).
        """
        # Först: Hämta det befintliga objektet från databasen.
        auction = Auction.query.get(auction_id)

        if auction:
            # Objektet hittades: Uppdatera fälten på Python-objektet.
            auction.description = data['description']
            auction.starting_bid = data['starting_bid']
            auction.auction_duration = data['auction_duration']
            auction.image_url = data.get('image_url', auction.image_url)
            # Använder .get() för att hantera frivilliga fält (behåller gamla värdet om inget nytt anges)

            # Spara ändringarna: Berättar för databasen att ändringarna på objektet ska sparas (UPDATE-fråga).
            # I SQLAlchemy lägger man inte till igen (.add) vid uppdatering, utan committar direkt.
            db.session.commit()

        return auction

    def radera(self, auction_id):
        """
        Raderar en auktion från databasen (DELETE-operation). 
        Args:
            auction_id (int): ID för auktionen att radera

        Returns:
            bool: True om radering lyckades, False om auktionen inte fanns att radera.
        """
        # Först: Hämta objektet för att säkerställa att det finns.
        auction = Auction.query.get(auction_id)

        if auction:
            # Markera objektet för radering i databassessionen.
            db.session.delete(auction)
            # Utför den faktiska DELETE-frågan till databasen.
            db.session.commit()
            return True

        return False

# Skapa EN instans av repository som kan användas överallt
# Detta objekt är nu redo att importeras och användas i andra delar av koden,
# t.ex. i dina rutter (views).
auction_repo = AuctionRepository()