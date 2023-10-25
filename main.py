import psycopg2

# Напишем функцию, создающую БД
def create_db(conn):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS customers(
        client_id INTEGER UNIQUE PRIMARY KEY,
        first_name VARCHAR(20),
        last_name VARCHAR(40),
        email VARCHAR(60));""")
    cur.execute("""CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES customers(client_id),
        phone VARCHAR(12));""")
    conn.commit()
    conn.close()

# Создаем функцию, позволяющую добавлять нового клиента
def add_client(conn, client_id, first_name, last_name, email, phones=None):
    cur = conn.cursor()
    cur.execute("""INSERT INTO customers(client_id, first_name, last_name, email) VALUES (%s, %s, %s, %s);""",
                (client_id, first_name, last_name, email))
    conn.commit()
    cur.execute("""SELECT * FROM phones;""")
    print(cur.fetchall())
    conn.close()

# Создаем функцию, позволяющую добавить телефон для существующего клиента
def add_phone(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute("""UPDATE phones SET phone=%s WHERE client_id=%s;""", (phone, client_id))
    conn.commit()
    conn.close()

#  Создаем функцию, позволяющую изменить данные о клиенте
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    cur = conn.cursor()
    if first_name:
        conn.execute("UPDATE customers SET first_name=%s WHERE id=%s", (first_name, client_id))
    if last_name:
        conn.execute("UPDATE customers SET last_name=%s WHERE id=%s", (last_name, client_id))
    if email:
        conn.execute("UPDATE customers SET email=%s WHERE id=%s", (email, client_id))
    print(cur.fetchall)
    conn.close()

# Создаем функцию, позволяющую удалить телефон для существующего клиента
def delete_phone(conn, client_id):
    cur = conn.cursor()
    cur.execute("""UPDATE phones SET phone=%s WHERE client_id=%s;""", ('Null', client_id))
    cur.execute("""SELECT * FROM phones;""")
    print(cur.fetchall())
    conn.close()

# Создаем функцию, позволяющую удалить существующего клиента
def delete_client(conn, client_id):
    cur = conn.cursor()
    cur.execute("""DELETE FROM phones WHERE client_id=%s;""",
                (client_id,))
    cur.execute("""SELECT * FROM phones;""")
    print(cur.fetchall())
    cur = conn.cursor()
    cur.execute("""DELETE FROM customers WHERE client_id=%s;""",
                (client_id,))
    cur.execute("""SELECT * FROM customers;""")
    print(cur.fetchall())
    conn.close()

# Создаем функцию, позволяющую найти клиента по его данным: имени, фамилии, email или телефону
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur = conn.cursor()
    cur.execute("""
    SELECT first_name, last_name FROM customers c JOIN phones p ON c.client_id = p.client_id 
    WHERE (first_name=%(first_name)s OR %(first_name)s IS NULL)
    AND (last_name=%(last_name)s OR %(last_name)s IS NULL)
    AND (email=%(email)s OR %(email)s IS NULL)
    AND (phone=%(phone)s OR %(phone)s IS NULL);""",
    {"first_name": first_name, "last_name": last_name, "email": email, "phone": phone})
    print(cur.fetchall())
    conn.close()

if __name__ == "__main__":
    with psycopg2.connect(database="DBClients", user=input("Введите имя пользователя: "),
                        password=input("Введите пароль для подключения: ")) as conn:
        create_db(conn)
        add_client(conn, 1, 'Иван', 'ИВАНОВ', 'ivanov@e-mail.com', '+71111111111')
        add_client(conn, 2, 'Пётр', 'Петров', 'petrov@e-mail.com', '+72222222222')
        add_client(conn, 3, 'Сергей', 'Сидоров', 'sidorov@e-mail.com')

        add_client(conn, 4, 'Илья', 'Пупкин', 'pupkin@e-mail.com', '+74444444444')

        add_phone(conn, 3, '+73333333333')

        change_client(conn, 2, email='petr@e-mail.com')

        delete_phone(conn, 1)
        delete_client(conn, 4)

        find_client(conn, first_name='Сергей')
        find_client(conn, phone='+72222222222')