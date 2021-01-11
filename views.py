from flask import request, jsonify
from app import app, db
from app.models import Friend
from datetime import datetime



@app.route('/api/friends', methods=['GET'])
def index():
    friends = Friend.query.all()
    output = []

    for friend in friends:
        friend_data = {}
        friend_data['id'] = friend.id
        friend_data['name'] = friend.name
        friend_data['last_name'] = friend.last_name
        friend_data['phone'] = friend.phone
        friend_data['sex'] = friend.sex
        friend_data['birth_day'] = friend.birth_day
        friend_data['friend_rank'] = friend.friend_rank
        friend_data['hobby'] = friend.hobby
        output.append(friend_data)

    return jsonify({'friends': output})



@app.route('/api/friends', methods=['POST'])
def create():
    data = request.json

    year = int(data['birth_day'][:4])
    month = int(data['birth_day'][5:7])
    day = int(data['birth_day'][8:10])
    birth_day = datetime(year, month, day)

    new_friend = Friend(name=data['name'],
                    last_name=data['last_name'],
                    phone=data['phone'],
                    sex=data['sex'],
                    birth_day=birth_day,
                    friend_rank=data['friend_rank'],
                    hobby=data['hobby'])
    db.session.add(new_friend)
    db.session.commit()
    return jsonify({'message': 'New friend created'})


@app.route("/api/friends/<int:friend_id>", methods=['GET'])
def friend(friend_id):
    friend = Friend.query.filter_by(id=friend_id).first()

    if not friend:
        return jsonify({'message': 'Friend not found'})

    friend_data = {}
    friend_data['id'] = friend.id
    friend_data['name'] = friend.name
    friend_data['last_name'] = friend.last_name
    friend_data['phone'] = friend.phone
    friend_data['sex'] = friend.sex
    friend_data['birth_day'] = friend.birth_day
    friend_data['friend_rank'] = friend.friend_rank
    friend_data['hobby'] = friend.hobby

    return jsonify({'friend': friend_data})


@app.route("/api/friends/<int:friend_id>", methods=['PUT'])
def update_friend(friend_id):
    data = request.json
    friend = Friend.query.filter_by(id=friend_id).first()

    if not friend:
        return jsonify({'message': 'Friend not found'})

    year = int(data['birth_day'][:4])
    month = int(data['birth_day'][5:7])
    day = int(data['birth_day'][8:10])
    birth_day = datetime(year, month, day)

    friend.name = data['name']
    friend.last_name = data['last_name']
    friend.phone = data['phone']
    friend.sex = data['sex']
    friend.birth_day = birth_day
    friend.friend_rank = data['friend_rank']
    friend.hobby = data['hobby']
    db.session.commit()

    return jsonify({'message': 'The friend has been updated'})


@app.route("/api/friends/<int:friend_id>", methods=['DELETE'])
def delete_friend(friend_id):
    friend = Friend.query.filter_by(id=friend_id).first()

    if not friend:
        return jsonify({'message': 'Friend was not found'})

    db.session.delete(friend)
    db.session.commit()
    return jsonify({'message': 'The friend has been deleted'})
