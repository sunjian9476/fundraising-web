class User:
    def __init__(self, id, username, password, email, name, join_date):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.join_date = join_date


class Event:
    def __init__(self, id, title, description, goal, start_date, end_date, creator_id):
        self.id = id
        self.title = title
        self.description = description
        self.goal = goal
        self.start_date = start_date
        self.end_date = end_date
        self.creator_id = creator_id


class Donation:
    def __init__(self, id, user_id, event_id, amount, donate_date):
        self.id = id
        self.user_id = user_id
        self.event_id = event_id
        self.amount = amount
        self.donate_date = donate_date


class Volunteer:
    def __init__(self, id, user_id, join_date):
        self.id = id
        self.user_id = user_id
        self.join_date = join_date
