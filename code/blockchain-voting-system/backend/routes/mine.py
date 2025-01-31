from .__init__ import block_chain
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

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

    return jsonify({
        'msg':'New block mined!',
        'block':new_block.as_dict()
    }), 201
