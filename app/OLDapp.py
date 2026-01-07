from flask import Flask, render_template, jsonify, request
import json

from myblueprints.auctions_bp.auctions_bp import auctions_bp
#from myblueprints.login_bp.login_bp import login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'af3fc57db372caf31143a78ce9036b955618517ac2855ef73e58df67ae11e51a'
#login_manager.init_app(app) #Register this app with the loginmanager that is in login_bp, see import above

# for formhandling, sessions, security, Flask uses this key
#to protect the contents of the user session against tampering.
#such ass cross-site request forgery (CSRF) attacks. A CSRF attack
#occurs when a malicious website sends
#requests to the application server on which the user is currently logged in.

app.register_blueprint(auctions_bp, url_prefix='/auctions')


# <!-- 
# <p class="text-center mb-0">
#     &copy;
#     <script>document.write(new Date().getFullYear())</script> Mäklarfirman Blge Estates AB.
#     <a href="{{url_for('auth_bp.login')}}">Admin Login</a>
# </p>
#  -->