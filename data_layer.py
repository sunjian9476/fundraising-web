from typing import List, Dict, Tuple
import pymysql
from config import create_connection
from models import User, Event, Donation, Volunteer


def is_valid_credentials(username, password) -> bool:
    conn = create_connection()
    try:
        cur = conn.cursor()
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cur.execute(query, (username, password))
        r = cur.fetchone() is not None
    except:
        return False
    finally:
        conn.close()
    return r


def get_user(username) -> User:
    conn = create_connection()
    try:
        cur = conn.cursor()
        query = "SELECT * FROM users WHERE username=%s"
        cur.execute(query, (username,))
        row = cur.fetchone()
        if row:
            return User(*row)
    finally:
        conn.close()


def get_user_by_id(user_id) -> User:
    conn = create_connection()

    try:
        cur = conn.cursor()
        query = "SELECT * FROM users WHERE id = %s"
        cur.execute(query, (user_id,))
        row = cur.fetchone()

        if row:
            return User(*row)

    finally:
        conn.close()


def list_all_events() -> List[Event]:
    conn = create_connection()
    try:
        cur = conn.cursor()
        query = "SELECT * FROM events"
        cur.execute(query)
        rows = cur.fetchall()
        return [Event(*row) for row in rows]
    finally:
        conn.close()


def get_event(event_id) -> Event:
    conn = create_connection()
    try:
        cur = conn.cursor()
        query = "SELECT * FROM events WHERE id=%s"
        cur.execute(query, (event_id,))
        row = cur.fetchone()
        if row:
            return Event(*row)
    finally:
        conn.close()


def get_event_donations(event_id) -> List[Tuple[Donation, User]]:
    conn = create_connection()
    try:
        cur = conn.cursor()
        query = "SELECT * FROM donations WHERE event_id=%s ORDER BY donate_date DESC"
        cur.execute(query, (event_id,))
        rows = cur.fetchall()
        donations = [Donation(*row) for row in rows]
        return [(donation, get_user_by_id(donation.user_id)) for donation in donations]
    finally:
        conn.close()


def get_donation_detail(donation_id) -> Donation:
    conn = create_connection()
    try:
        cur = conn.cursor()
        query = "SELECT * FROM donations WHERE id=%s"
        cur.execute(query, (donation_id,))
        row = cur.fetchone()
        if row:
            return Donation(*row)
    finally:
        conn.close()


def register_user(user: User):
    conn = create_connection()
    try:
        cur = conn.cursor()
        query = "INSERT INTO users (username, password, email, name) VALUES (%s, %s, %s, %s)"
        values = (user.username, user.password, user.email, user.name)
        cur.execute(query, values)
        conn.commit()
        return True
    except:
        # username/email already exists
        return False
    finally:
        conn.close()


def became_a_volunteer(user_id) -> bool:
    conn = create_connection()
    try:
        cur = conn.cursor()
        query = "INSERT INTO volunteers (user_id) VALUES (%s)"
        cur.execute(query, (user_id,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def add_an_event(event: Event) -> bool:
    conn = create_connection()
    try:
        cur = conn.cursor()
        query = "INSERT INTO events (title, description, goal, start_date, end_date, creator_id) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (event.title, event.description, event.goal, event.start_date, event.end_date, event.creator_id)
        cur.execute(query, values)
        conn.commit()
        return True
    except pymysql.Error as e:
        return False
    finally:
        conn.close()


def list_all_volunteers() -> List[Volunteer]:
    conn = create_connection()

    result = []

    try:
        cur = conn.cursor()

        # Get volunteer user ids and join dates
        query = """SELECT v.user_id, v.join_date
               FROM volunteers v"""

        cur.execute(query)

        rows = cur.fetchall()

        # Convert to tuple of Volunteer and datetime
        for row in rows:
            result.append((get_user_by_id(row[0]), row[1]))

    finally:
        conn.close()

    return result


def list_all_leaders() -> List[User]:
    conn = create_connection()

    try:
        cur = conn.cursor()

        query = """SELECT DISTINCT u.*  
               FROM users u
               INNER JOIN events e ON u.id = e.creator_id"""

        cur.execute(query)

        rows = cur.fetchall()
        leaders = []

        for row in rows:
            user = User(*row)
            leaders.append(user)

        return leaders

    finally:
        conn.close()


def search_events(keyword) -> List[Event]:
    conn = create_connection()

    try:
        cur = conn.cursor()

        # Use LIKE to search title and description
        query = """SELECT * FROM events 
               WHERE title LIKE %s OR description LIKE %s"""

        # Add wildcard % to keyword
        keyword = "%{}%".format(keyword)
        cur.execute(query, (keyword, keyword))

        rows = cur.fetchall()

        events = []
        for row in rows:
            event = Event(*row)
            events.append(event)

        return events

    finally:
        conn.close()


def list_events_by_creator_id(creator_id) -> List[Event]:
    conn = create_connection()

    try:
        cur = conn.cursor()

        query = """SELECT * FROM events 
               WHERE creator_id = %s"""

        cur.execute(query, (creator_id,))

        rows = cur.fetchall()
        events = []

        for row in rows:
            event = Event(*row)
            events.append(event)

        return events

    finally:
        conn.close()


def donate_an_event(event_id, user_id, amount):
    conn = create_connection()

    try:
        cur = conn.cursor()

        # Insert donation
        query = """INSERT INTO donations 
               (event_id, user_id, amount)  
               VALUES (%s, %s, %s)"""
        cur.execute(query, (event_id, user_id, amount))

        conn.commit()
        return True
    except:
        return False

    finally:
        conn.close()


def check_is_volunteer(user_id):
    conn = create_connection()

    try:
        cur = conn.cursor()
        query = "SELECT * FROM volunteers WHERE user_id = %s"
        cur.execute(query, (user_id,))
        row = cur.fetchone()

        if row:
            return True

    finally:
        conn.close()

    return False


def clean_all():
    conn = create_connection()
    try:
        cur = conn.cursor()

        cur.execute("DELETE FROM volunteers")
        cur.execute("DELETE FROM donations")
        cur.execute("DELETE FROM events")
        cur.execute("DELETE FROM users")

        conn.commit()
    finally:
        conn.close()


def list_all_users() -> List[User]:
    conn = create_connection()

    users = []

    try:
        cur = conn.cursor()
        query = "SELECT * FROM users"
        cur.execute(query)

        rows = cur.fetchall()
        for row in rows:
            user = User(*row)
            users.append(user)

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        conn.close()

    return users
