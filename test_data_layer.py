import datetime

import pytest
from data_layer import *


@pytest.fixture(autouse=True)
def clean():
    clean_all()


@pytest.fixture
def sample_user():
    return User(1, 'test', 'password', 'test@example.com', 'Test User', datetime.datetime.now())


def test_valid_credentials(sample_user):
    register_user(sample_user)
    assert is_valid_credentials('test', 'password')


def test_invalid_username():
    assert not is_valid_credentials('invaliduser', 'password')


def test_invalid_password():
    assert not is_valid_credentials('test', 'wrongpassword')


def test_invalid_username_and_password():
    assert not is_valid_credentials('invaliduser', 'wrongpassword')


def test_register_user(sample_user):
    register_user(sample_user)
    target = get_user('test')
    assert target.username == sample_user.username
    assert target.password == sample_user.password
    assert target.name == sample_user.name
    assert target.email == sample_user.email


def test_add_event(sample_user):
    register_user(sample_user)
    sample_user = list_all_users()[0]
    event = Event(1, 'Test Event', 'Test', 100, datetime.date(2023, 1, 1), datetime.date(2023, 1, 2), sample_user.id)
    add_an_event(event)

    fetched = list_all_events()[0]
    assert fetched.title == 'Test Event'
    assert fetched.description == 'Test'
    assert fetched.goal == 100
    assert fetched.start_date == datetime.date(2023, 1, 1)
    assert fetched.end_date == datetime.date(2023, 1, 2)
    assert fetched.creator_id == sample_user.id


def test_donate_event(sample_user):
    # Register user
    register_user(sample_user)
    sample_user = list_all_users()[0]

    # Add event
    event = Event(1, 'Test Event', 'Test', 100, datetime.date(2023, 1, 1), datetime.date(2023, 1, 2), sample_user.id)
    add_an_event(event)
    event = list_all_events()[0]

    # Donate to event
    donate_an_event(event.id, sample_user.id, 50)

    donations = get_event_donations(event.id)
    assert len(donations) == 1
    assert donations[0][0].amount == 50
