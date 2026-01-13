from flask import Blueprint, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import requests #to make request to google book api
from markupsafe import escape

search_bp = Blueprint('search_bp', __name__, template_folder='templates')
#create the class for the form
class SearchForm(FlaskForm):
    search_term = StringField('Book Search')

@search_bp.route('/', methods=['GET', 'POST'])
def search_items():
    ''' Fetch books from Google Books API based on user query'''
    form = SearchForm()
    search_query = "Mona Lisa" #default search query
    api_url = "https://www.googleapis.com/books/v1/volumes" #Google Books API endpoint

    if request.method == 'POST':
        search_query = form.search_term.data
    
    params = {
        'q': search_query
    }
    response = requests.get(api_url, params=params)
    data_json = response.json()
    bookItems=data_json.get('items', [])
    return render_template('search_test.html', books=bookItems, query=search_query, form=form)

@search_bp.route('/book/<book_id>', methods=['GET'])
def item_details(book_id):
    ''' Fetch detailed information about a specific book using its ID '''
    api_url = f"https://www.googleapis.com/books/v1/volumes"
    
    # Prevent Cross-Site Scripting (XSS) by sanitizing potentially
    # unsafe user input in web applications. In this case, we use escape(id)
    # to ensure that any special characters in the book_id are properly encoded.
    book_id = escape(book_id)
    api_url = f"{api_url}/{book_id}"

    response = requests.get(api_url)

    data_json_dict = response.json()
    return render_template('book_details.html', book=data_json_dict)