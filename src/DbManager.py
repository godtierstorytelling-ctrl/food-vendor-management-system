import csv
import sqlite3
import os
from sqlite3 import Error
from os import path
from Users import Admin, Customer


class DbManager:

    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(":memory:")

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def create_menu_table(self, data_file):
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMARY KEY,
                category TEXT,
                item_name TEXT,
                description TEXT,
                price REAL,
                prep_time INTEGER,
                available INTEGER
            )
        """)

        with open(data_file, "r") as file:
            next(file)

            for row in file:
                fields = row.rstrip("\n").split("\t")

                category = fields[0]
                item_name = fields[1]
                description = fields[2]
                price = float(fields[3])
                prep_time = int(fields[4])
                available = int(fields[5])

                menu_item = (
                    category,
                    item_name,
                    description,
                    price,
                    prep_time,
                    available
                )

                self.insert_menu(menu_item)

        self.conn.commit()

    def insert_menu(self, menu):
        sql = """
            INSERT INTO menu (
                category,
                item_name,
                description,
                price,
                prep_time,
                available
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, menu)
        self.conn.commit()

    def create_user_table(self, data_file):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                user_name TEXT,
                account_type TEXT,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                phone_number TEXT,
                password TEXT,
                employee_id TEXT,
                credit_card_number TEXT,
                credit_card_exp_date TEXT,
                billing_address TEXT,
                reward_points INTEGER,
                order_history INTEGER
            )
        """)

        with open(data_file, "r") as file:
            next(file)

            for row in file:
                fields = row.rstrip("\n").split("\t")

                user_name = fields[0]
                account_type = fields[1]
                first_name = fields[2]
                last_name = fields[3]
                email = fields[4]
                phone_number = fields[5]
                password = fields[6]
                employee_id = fields[7]
                credit_card_number = fields[8]
                credit_card_exp_date = fields[9]
                billing_address = fields[10]

                reward_points = int(fields[11]) if fields[11] else None
                order_history = int(fields[12]) if fields[12] else None

                user = (
                    user_name,
                    account_type,
                    first_name,
                    last_name,
                    email,
                    phone_number,
                    password,
                    employee_id,
                    credit_card_number,
                    credit_card_exp_date,
                    billing_address,
                    reward_points,
                    order_history
                )

                self.insert_user(user)

        self.conn.commit()

    def insert_user(self, user):
        sql = """
            INSERT INTO user (
                user_name,
                account_type,
                first_name,
                last_name,
                email,
                phone_number,
                password,
                employee_id,
                credit_card_number,
                credit_card_exp_date,
                billing_address,
                reward_points,
                order_history
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, user)
        self.conn.commit()

    def update_customer_rewards(self, name, value):
        sql = """
            UPDATE user
            SET reward_points = ?
            WHERE user_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (value, name))
        self.conn.commit()

    def update_customer_history(self, name, value):
        sql = """
            UPDATE user
            SET order_history = ?
            WHERE user_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (value, name))
        self.conn.commit()

    def is_user_exist(self, user_name):
        sql = """
        SELECT *
        FROM user
        WHERE user_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (user_name,))

        user = cursor.fetchone()

        return user is not None

    def delete_user(self, user_name):
        sql = """
            DELETE FROM user
            WHERE user_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (user_name,))
        self.conn.commit()

    def display_daily_menu(self, category):
        sql = """
            SELECT item_name, price, description
            FROM menu
            WHERE category = ?
            AND available = 1
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (category,))

        items = cursor.fetchall()

        print(f"{category}:")

        for item_name, price, description in items:
            print(f"    {item_name}    (${price:.2f})")
            print(f"       {description}")

    def set_food_price(self, name, price):
        sql = """
            UPDATE menu
            SET price = ?
            WHERE item_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (price, name))
        self.conn.commit()

    def set_food_category(self, name, category):
        sql = """
            UPDATE menu
            SET category = ?
            WHERE item_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (category, name))
        self.conn.commit()

    def set_food_description(self, name, description):
        sql = """
            UPDATE menu
            SET description = ?
            WHERE item_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (description, name))
        self.conn.commit()

    def set_food_availability(self, name, availability):
        sql = """
            UPDATE menu
            SET available = ?
            WHERE item_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (availability, name))
        self.conn.commit()

    def set_food_name(self, old_name, new_name):
        sql = """
            UPDATE menu
            SET item_name = ?
            WHERE item_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (new_name, old_name))
        self.conn.commit()

    def get_food_price(self, name):
        sql = """
            SELECT price
            FROM menu
            WHERE item_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (name,))

        result = cursor.fetchone()

        if result is not None:
            return float(result[0])

        return -1.0

    def get_food_time(self, name):
        sql = """
            SELECT prep_time
            FROM menu
            WHERE item_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (name,))

        result = cursor.fetchone()

        if result is not None:
            return result[0]

        return -1

    def is_food_exist(self, name):
        sql = """
            SELECT item_name
            FROM menu
            WHERE item_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (name,))

        result = cursor.fetchone()

        return result is not None

    def is_food_available(self, name):
        sql = """
            SELECT available
            FROM menu
            WHERE item_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (name,))

        result = cursor.fetchone()

        if result is not None:
            return result[0] == 1

        return False

    def update_admin(self, user):
        sql = """
            UPDATE user
            SET phone_number = ?,
                email = ?
            WHERE user_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(
            sql,
            (
                user.phone_num,
                user.email,
                user.user_name
            )
        )
        self.conn.commit()

    def get_admin(self, user_name):
        sql = """
            SELECT user_name,
                   account_type,
                   first_name,
                   last_name,
                   email,
                   phone_number,
                   password,
                   employee_id
            FROM user
            WHERE user_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (user_name,))

        user = cursor.fetchone()

        if user is None:
            return Admin(
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                ""
            )

        return Admin(
            user[0],
            user[1],
            user[2],
            user[3],
            user[4],
            user[5],
            user[6],
            user[7]
        )

    def update_customer(self, user):
        sql = """
            UPDATE user
            SET credit_card_number = ?,
                credit_card_exp_date = ?,
                billing_address = ?,
                phone_number = ?,
                email = ?
            WHERE user_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(
            sql,
            (
                user.card_num,
                user.card_date,
                user.address,
                user.phone_num,
                user.email,
                user.user_name
            )
        )
        self.conn.commit()


    def get_customer(self, user_name):
        sql = """
            SELECT user_name,
                   account_type,
                   first_name,
                   last_name,
                   email,
                   phone_number,
                   password,
                   credit_card_number,
                   credit_card_exp_date,
                   billing_address,
                   reward_points,
                   order_history
            FROM user
            WHERE user_name = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, (user_name,))

        user = cursor.fetchone()

        if user is None:
            return Customer(
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                ""
            )

        return Customer(
            user[0],
            user[1],
            user[2],
            user[3],
            user[4],
            user[5],
            user[6],
            user[7],
            user[8],
            user[9],
            user[10],
            user[11]
        )
