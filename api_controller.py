import datetime

from flask import Blueprint
from flask import session, request, jsonify, redirect, render_template

import data_layer
from models import User, Event

main_controller = Blueprint('main', __name__)


@main_controller.route('/get_user/<username>')
def get_user(username):
    user = data_layer.get_user(username)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'name': user.name
    })


@main_controller.route('/list_events')
def list_events():
    events = data_layer.list_all_events()
    data = []
    for event in events:
        data.append({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'goal': event.goal,
            'start_date': event.start_date,
            'end_date': event.end_date,
            'creator': event.creator_id
        })
    return jsonify(data)


@main_controller.route('/get_event/<int:event_id>')
def get_event(event_id):
    event = data_layer.get_event(event_id)

    if not event:
        return jsonify({'error': 'Event not found'}), 404

    data = {
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'goal': event.goal,
        'start_date': event.start_date,
        'end_date': event.end_date,
        'creator': event.creator_id
    }

    return jsonify(data)


@main_controller.route('/get_event_donations/<int:event_id>')
def get_event_donations(event_id):
    donations = data_layer.get_event_donations(event_id)

    data = []
    for d in donations:
        data.append({
            'id': d.id,
            'user': d.user_id,
            'amount': d.amount,
            'date': d.donate_date
        })

    return jsonify(data)


@main_controller.route('/get_donation/<int:donation_id>')
def get_donation(donation_id):
    donation = data_layer.get_donation_detail(donation_id)

    if not donation:
        return jsonify({'error': 'Donation not found'}), 404

    data = {
        'id': donation.id,
        'user': donation.user_id,
        'event': donation.event_id,
        'amount': donation.amount,
        'date': donation.donate_date
    }

    return jsonify(data)


@main_controller.route('/become_volunteer', methods=['POST'])
def become_volunteer():
    username = request.form.get('username')

    if not username:
        return jsonify({'error': 'Username required'})

    if not data_layer.became_a_volunteer(username):
        return jsonify({'error': 'Failed to become volunteer'})

    return jsonify({'message': 'You are now a volunteer!'})


@main_controller.route('/add_event', methods=['POST'])
def add_event():
    title = request.form.get('title')
    description = request.form.get('description')
    goal = request.form.get('goal')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    creator_id = session.get('user_id')

    if not all([title, description, goal, start_date, end_date]):
        return jsonify({'error': 'All fields are required'})

    goal = float(goal)
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    # 创建事件对象
    event = Event(
        id=None,
        title=title,
        description=description,
        goal=goal,
        start_date=start_date,
        end_date=end_date,
        creator_id=creator_id)

    res = data_layer.add_an_event(event)

    if not res:
        return jsonify({'error': 'Failed to create event'})

    return jsonify({'message': 'Event created successfully!'})


@main_controller.route('/list_all_volunteers')
def list_all_volunteers():
    volunteers = data_layer.list_all_volunteers()

    data = []
    for v in volunteers:
        data.append({
            'id': v.id,
            'user_id': v.user_id,
            'join_date': v.join_date
        })

    return jsonify(data)