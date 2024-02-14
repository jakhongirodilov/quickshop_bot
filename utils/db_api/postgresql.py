import datetime
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result
        
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())


# products_users table ----------------------------------------------------------------------------------
    # async def create_table_users(self):
    #     sql = """
    #     CREATE TABLE IF NOT EXISTS products_users (
    #     id SERIAL PRIMARY KEY,
    #     full_name VARCHAR(255) NOT NULL,
    #     username varchar(255) NULL,
    #     telegram_id BIGINT NOT NULL UNIQUE
    #     );
    #     """
    #     await self.execute(sql, execute=True)

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO products_users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM products_users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, telegram_id):
        sql = "SELECT * FROM products_users WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM products_users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE products_users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM products_users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE products_users", execute=True)

    
# products_products table -------------------------------------------------------------------------------
    # async def create_table_product(self):
    #     sql = """
    #         CREATE TABLE IF NOT EXISTS products_product (
    #             id SERIAL PRIMARY KEY,
    #             name VARCHAR(255) NOT NULL,
    #             description VARCHAR(255) NOT NULL,
    #             price NUMERIC(10, 2) NOT NULL,
    #             category_id INTEGER REFERENCES products_category(id),
    #             subcategory_id INTEGER REFERENCES products_subcategory(id),
    #             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #         );
    #     """
    #     await self.execute(sql, execute=True)

    async def add_product(self, name, description, price, category_id, subcategory_id):
        sql = """
            INSERT INTO products_product (name, description, price, category_id, subcategory_id, created_at) 
            VALUES ($1, $2, $3, $4, $5, CURRENT_TIMESTAMP) 
            RETURNING *
        """
        return await self.execute(sql, name, description, price, category_id, subcategory_id, fetchrow=True)

    async def select_all_products(self, category_id, subcategory_id):
        sql = f"SELECT * FROM products_product WHERE category_id = $1 and subcategory_id=$2"
        return await self.execute(sql, category_id, subcategory_id, fetch=True)
    
    async def select_product(self, product_id):
        sql = "SELECT * FROM products_product WHERE id = $1 "
        return await self.execute(sql, product_id, fetchrow=True)
    
    async def count_products(self, category_code):
        sql = "SELECT COUNT(*) FROM products_product WHERE products_product.category_id = $1"
        return await self.execute(sql, category_code, fetchval=True)

    async def delete_products(self):
        await self.execute("DELETE FROM products_product WHERE TRUE", execute=True)

    async def drop_product(self):
        await self.execute("DROP TABLE products_product", execute=True)


# Categories table -----------------------------------------------------------------------------
    # async def create_table_category(self):
    #     sql = """
    #         CREATE TABLE IF NOT EXISTS products_category (
    #             id SERIAL PRIMARY KEY,
    #             category_code VARCHAR(255) UNIQUE,
    #             category_name VARCHAR(255)
    #         );
    #     """
    #     await self.execute(sql, execute=True)

    async def add_category(self, category_code, category_name):
        sql = """
            INSERT INTO products_category (category_code, category_name) 
            VALUES ($1, $2) 
            RETURNING *
        """
        return await self.execute(sql, category_code, category_name, fetchrow=True)
    
    async def select_all_categories(self):
        sql = "SELECT * FROM products_category"
        return await self.execute(sql, fetch=True)
    
    async def count_categories(self):
        sql = "SELECT COUNT(*) FROM products_category"
        return await self.execute(sql, fetchval=True)

    async def delete_categories(self):
        await self.execute("DELETE FROM products_category WHERE TRUE", execute=True)

    async def drop_category(self):
        await self.execute("DROP TABLE products_category", execute=True)


# Subcategories table --------------------------------------------------------------------------
    # async def create_table_subcategory(self):
    #     sql = """
    #         CREATE TABLE IF NOT EXISTS products_subcategory (
    #             id SERIAL PRIMARY KEY,
    #             category_id INTEGER REFERENCES products_category(id),
    #             category_code VARCHAR(255) UNIQUE,
    #             category_name VARCHAR(255)
    #         );
    #     """
    #     await self.execute(sql, execute=True)

    async def add_subcategory(self, category_id, subcategory_code, subcategory_name):
        sql = """
            INSERT INTO products_subcategory (category_id, subcategory_code, subcategory_name) 
            VALUES ($1, $2, $3) 
            RETURNING *
        """
        return await self.execute(sql, category_id, subcategory_code, subcategory_name, fetchrow=True)
    
    async def select_all_subcategories(self, category):
        sql = "SELECT * FROM products_subcategory WHERE products_subcategory.category_id = $1"
        return await self.execute(sql, category, fetch=True)
    
    async def count_subcategories(self):
        sql = "SELECT COUNT(*) FROM products_subcategory"
        return await self.execute(sql, fetchval=True)

    async def delete_subcategories(self):
        await self.execute("DELETE FROM products_subcategory WHERE TRUE", execute=True)

    async def drop_subcategory(self):
        await self.execute("DROP TABLE products_subcategory", execute=True)


# products_carts table ----------------------------------------------------------------------------------
    # async def create_table_cart(self):
    #     sql = """
    #         CREATE TABLE IF NOT EXISTS products_cart (
    #             id SERIAL PRIMARY KEY,
    #             user_id INTEGER REFERENCES products_users(id),
    #             product_id INTEGER REFERENCES products_product(id),
    #             quantity INTEGER,
    #             added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #         );
    #     """
    #     await self.execute(sql, execute=True)

    async def add_to_cart(self, user_id, product_id, quantity):
        current_time = datetime.datetime.utcnow()
        sql = """
            INSERT INTO products_cart (user_id, product_id, quantity, added_at)
            VALUES ($1, $2, $3, $4)
            RETURNING *
        """
        return await self.execute(sql, user_id, product_id, quantity, current_time, fetchrow=True)
    
    async def increment_quantity(self, user_id, product_id):
        sql = """
            UPDATE products_cart 
            SET quantity = quantity + 1
            WHERE user_id = $1 and product_id = $2
        """
        return await self.execute(sql, user_id, product_id, execute=True)
    
    async def remove_cart_item(self, user_id, product_id):
        sql = """
            DELETE FROM products_cart 
            WHERE user_id = $1 AND product_id = $2
        """
        return await self.execute(sql, user_id, product_id, execute=True)
    
    async def get_cart_item(self, user_id, product_id):
        sql = "SELECT * FROM products_cart WHERE user_id=$1 AND product_id=$2"
        return await self.execute(sql, user_id, product_id, fetchrow=True)

    async def get_cart_items(self, user_id):
        sql = """
            SELECT * FROM products_cart WHERE user_id = $1
        """
        return await self.execute(sql, user_id, fetch=True)
    
    async def clear_cart_items(self, user_id):
        sql = """
            DELETE FROM products_cart
            WHERE user_id = $1
        """
        await self.execute(sql, user_id, execute=True)



# products_orders table ---------------------------------------------------------------------------------
        """
        user = models.ForeignKey(Users, on_delete=models.CASCADE)
        phone_number = models.CharField(max_length=50)
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        quantity = models.IntegerField()
        price = models.DecimalField(max_digits=10, decimal_places=2)
        total_price = models.DecimalField(max_digits=10, decimal_places=2)

        full_name = models.CharField(max_length=100)
        latitude = models.CharField(max_length=200)
        longitude = models.CharField(max_length=200)
        
        order_date = models.DateTimeField(auto_now_add=True)
        """
    async def add_order(self, user_id, phone_number, product_id, quantity, price, total_price, full_name, latitude, longitude):
        sql = """
            INSERT INTO "products_order" (user_id, phone_number, product_id, quantity, price, total_price, full_name, latitude, longitude, order_date) 
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, CURRENT_TIMESTAMP) 
            RETURNING *
        """
        return await self.execute(sql, user_id, phone_number, product_id, quantity, price, total_price, full_name, latitude, longitude, fetchrow=True)


    async def select_all_orders(self):
        sql = "SELECT * FROM products_order"
        return await self.execute(sql, fetch=True)

    async def select_order_by_id(self, order_id):
        sql = "SELECT * FROM products_order WHERE id = $1"
        return await self.execute(sql, order_id, fetchrow=True)

    async def select_orders_by_user_id(self, user_id):
        sql = "SELECT * FROM products_order WHERE user_id = $1"
        return await self.execute(sql, user_id, fetch=True)

    async def delete_order(self, order_id):
        sql = "DELETE FROM products_order WHERE id = $1"
        return await self.execute(sql, order_id, execute=True)
