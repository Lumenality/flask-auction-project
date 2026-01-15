from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from ..login_bp.login_repository import UserRepository

users_bp_rest = Blueprint('users_bp_rest', __name__, template_folder='templates', static_folder='static')
users_repo = UserRepository()

@users_bp_rest.route('/', methods=['GET'])
def get_all_users():
    """Hämtar alla användare och returnerar dem som JSON."""
    users = users_repo.get_all()
    users_list = []
    for user in users:
        if not user.is_admin:
            users_list.append(
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                })
    if not users_list:
        return jsonify({'error': 'Inga användare hittades'}), 404
    return jsonify(users_list), 200

@users_bp_rest.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Hämtar en specifik användare."""
    user = users_repo.find_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'Användare inte hittad'}), 404
    
    if user.is_admin:
        return jsonify({'error': 'Åtkomst nekad'}), 403
    
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }
    return jsonify(user_data), 200