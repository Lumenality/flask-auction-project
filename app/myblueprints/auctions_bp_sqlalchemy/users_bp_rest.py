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

@users_bp_rest.route('/<int:user_id>/likes_dislikes', methods=['GET'])
@login_required
def get_user_likes_dislikes(user_id: int):
    """Hämtar alla likes och dislikes för en användare."""
    if current_user.id != user_id:
        return jsonify({'error': 'Åtkomst nekad'}), 403
    user_likes_dislikes = users_repo.get_all_likes_dislikes_for_user(user_id)
    
    user_likes_dislikes_list = []
    for entry in user_likes_dislikes:
        user_likes_dislikes_list.append(
            {
                'auction_id': entry.auction_id,
                'has_liked': entry.liked,
                'has_disliked': entry.disliked
            })
        
    return jsonify(user_likes_dislikes_list), 200

@users_bp_rest.route('/<int:user_id>/likes_dislikes/<int:auction_id>', methods=['GET'])
@login_required
def get_like_dislike(user_id: int, auction_id: int):
    """Hämtar likes och dislikes för en användare på en specifik auktion."""
    if current_user.id != user_id:
        return jsonify({'error': 'Åtkomst nekad'}), 403
    user_like_dislike = users_repo.get_user_like_dislike_for_auction(user_id, auction_id)
    
    if not user_like_dislike:
        return jsonify({'has_liked': False, 'has_disliked': False}), 200
    
    data = {
        'has_liked': user_like_dislike.liked,
        'has_disliked': user_like_dislike.disliked
    }

    return jsonify(data), 200