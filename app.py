from flask import Flask, render_template, request, redirect, session

from login_controller import auth
from api_controller import main_controller
import data_layer
import datetime

from models import Event

app = Flask(__name__)

# Set the secret key for signing the session cookie
app.secret_key = 'secret_key_haha'


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/contactus')
def contactus_page():
    return render_template('contactus.html')


@app.route('/donate')
def donate_page():
    events = data_layer.list_all_events()
    leaders = data_layer.list_all_leaders()
    return render_template('donate.html', events=events, leaders=leaders)


@app.route('/donate/by_creator_id/<int:creator_id>')
def donate_page_by_creator_id(creator_id):
    events = data_layer.list_events_by_creator_id(creator_id)
    leaders = data_layer.list_all_leaders()
    return render_template('donate.html', events=events, leaders=leaders)


@app.post('/donate_add')
def donate_add_page():
    title = request.form.get('title')
    description = request.form.get('description')
    goal = request.form.get('goal')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    creator_id = session.get('user_id')

    goal = float(goal)
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    event = Event(
        id=None,
        title=title,
        description=description,
        goal=goal,
        start_date=start_date,
        end_date=end_date,
        creator_id=creator_id)

    res = data_layer.add_an_event(event)
    return redirect('/donate')


@app.post('/donate')
def donate_page_search():
    keyword = request.form.get('keyword')

    events = data_layer.search_events(keyword)
    leaders = data_layer.list_all_leaders()
    return render_template('donate.html', events=events, leaders=leaders)


@app.route('/donate/<int:event_id>')
def donate_detail(event_id):
    event = data_layer.get_event(event_id)
    donations = data_layer.get_event_donations(event_id)

    total_donated = sum(d[0].amount for d in donations)

    return render_template('record.html', event=event,
                           donations=donations,
                           amount_raised=total_donated)


@app.post('/donate/<int:event_id>')
def donate_now(event_id):
    amount = request.form.get('amount')
    amount = float(amount)
    user_id = session.get('user_id')

    data_layer.donate_an_event(event_id, user_id, amount)
    event = data_layer.get_event(event_id)
    donations = data_layer.get_event_donations(event_id)

    total_donated = sum(d[0].amount for d in donations)

    return render_template('record.html', event=event,
                           donations=donations,
                           amount_raised=total_donated)


@app.route('/volunteer')
def volunteer_page():
    user_id = session.get('user_id')
    is_volunteer = False
    if user_id:
        is_volunteer = data_layer.check_is_volunteer(user_id)
    volunteers = data_layer.list_all_volunteers()
    return render_template('volunteer.html', is_volunteer=is_volunteer, volunteers=volunteers)


@app.post('/volunteer')
def volunteer_became_page():
    user_id = session.get('user_id')
    if user_id:
        data_layer.became_a_volunteer(user_id)
    volunteers = data_layer.list_all_volunteers()
    return render_template('volunteer.html', is_volunteer=True, volunteers=volunteers)


@app.route('/aboutus')
def aboutus_page():
    return render_template('aboutus.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/logout')
def logout_page():
    del session['user_id']
    return redirect('/login')


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(main_controller, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=5555)
