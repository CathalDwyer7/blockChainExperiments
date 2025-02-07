from .__init__ import block_chain
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from typing import Optional
from extensions import db

mine_routes = Blueprint('mine', __name__)

@mine_routes.route('/info', methods=['GET'])
@jwt_required()
def get_mine_info():
    last_block = block_chain.last_block
    last_proof = last_block.proof
    return jsonify({'last_proof': last_proof, 'difficulty': block_chain.POW_DIFFICULTY}), 200


@mine_routes.route('/mine-block', methods=['POST'])
@jwt_required()
def mine_block():
    data = request.get_json()

    if 'proof' not in data:
        return jsonify({'error': 'Proof is required'}, 400)

    new_proof = data['proof']
    last_proof = block_chain.last_block.proof

    if not block_chain.is_valid_pow(last_proof, new_proof):
        return jsonify({'error': 'Proof is not valid'}, 400)


    previous_hash = block_chain.hash(block_chain.last_block)
    new_block = block_chain.new_block(new_proof, previous_hash)

    current_user = get_jwt_identity()
    user_id = int(current_user['id'])
    user_obj: Optional[User] = User.query.get(user_id)

    if not user_obj:
        return jsonify({'error': 'user id not valid'}), 400

    user_obj.coins += 1
    db.session.commit()

    return jsonify({
        'msg':'New block mined!',
        'block':new_block.as_dict()
    }), 201


@mine_routes.route('/get_coins', methods=['GET'])
@jwt_required()
def get_coins():
    current_user = get_jwt_identity()
    user_id = int(current_user['id'])
    user_obj: Optional[User] = User.query.get(user_id)

    if not user_id or not user_obj:
        return jsonify({'error': 'user id not valid'}), 400

    return jsonify({"coins":user_obj.coins}), 200


