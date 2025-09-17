from .connect import get_connect


def is_register(chat_id):
    conn = get_connect()
    dbc = conn.cursor()
    try:
        dbc.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
        return dbc.fetchone()
    except Exception as e:
        print("Xato:", e)
        return None
    finally:
        conn.close()


def save_user(chat_id, fullname, phone, lat, long, username=None):
    conn = get_connect()
    dbc = conn.cursor()
    try:
        dbc.execute("""
            INSERT INTO users (chat_id, fullname, username, phone, lat, long)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (chat_id, fullname, username, phone, lat, long))
        conn.commit()
        return "Success"
    except Exception as e:
        print("Xato:", e)
        return None
    finally:
        conn.close()


def get_foods():
    conn = get_connect()
    dbc = conn.cursor()
    dbc.execute("SELECT * FROM food")
    foods = dbc.fetchall()
    conn.close()
    return foods


def get_food(id):
    conn = get_connect()
    dbc = conn.cursor()
    dbc.execute("SELECT * FROM food WHERE id = ?", (id,))
    food = dbc.fetchone()
    conn.close()
    return food


def save_order(food_id, user_id, quantity, price):
    conn = get_connect()
    dbc = conn.cursor()
    dbc.execute("""
        INSERT INTO orders (food_id, user_id, quantity, price, status)
        VALUES (?, ?, ?, ?, ?)
    """, (food_id, user_id, quantity, price, "new"))
    conn.commit()
    conn.close()


def is_admin(chat_id):
    conn = get_connect()
    dbc = conn.cursor()
    try:
        dbc.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
        return dbc.fetchone()
    except Exception as e:
        print("Xato:", e)
        return None
    finally:
        conn.close()


def is_new_foods():
    conn = get_connect()
    dbc = conn.cursor()
    try:
        dbc.execute("""
            SELECT 
                o.id AS order_id,
                f.name AS food_name,
                u.chat_id AS user_id,
                o.quantity,
                o.price,
                (o.quantity * o.price) AS total_price,
                o.status
            FROM orders o
            JOIN food f ON o.food_id = f.id
            JOIN users u ON o.user_id = u.id
            WHERE o.status = 'new';
        """)
        return dbc.fetchall()
    except Exception as e:
        print("Xato:", e)
        return None
    finally:
        conn.close()


def is_progress_foods():
    conn = get_connect()
    dbc = conn.cursor()
    try:
        dbc.execute("""
            SELECT 
                o.id AS order_id,
                f.name AS food_name,
                u.chat_id AS user_id,
                o.quantity,
                o.price,
                (o.quantity * o.price) AS total_price,
                o.status
            FROM orders o
            JOIN food f ON o.food_id = f.id
            JOIN users u ON o.user_id = u.id
            WHERE o.status = 'in_progress';
        """)
        return dbc.fetchall()
    except Exception as e:
        print("Xato:", e)
        return None
    finally:
        conn.close()


def update_order(order_id):
    conn = get_connect()
    dbc = conn.cursor()
    try:
        dbc.execute("UPDATE orders SET status = 'cancel' WHERE id = ?", (order_id,))
        conn.commit()
        return True
    except Exception as e:
        print("Xato:", e)
        return None
    finally:
        conn.close()


def add_food(data: dict):
    conn = get_connect()
    dbc = conn.cursor()
    try:
        dbc.execute("""
            INSERT INTO food (name, description, image, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, (data["name"], data["desc"], data["image"], data["price"], data["quantity"]))
        conn.commit()
        return True
    except Exception as e:
        print("Xato:", e)
        return None
    finally:
        conn.close()