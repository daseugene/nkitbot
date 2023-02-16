from asyncpg.connection import Connection
import asyncpg
from aiogram.dispatcher import Dispatcher

# from mainbotfile import student_authorized


class Database:
    def __init__(
        self,
        db_user: str,
        db_password: str,
        db_host: str,
        db_port: int,
        db_name: str
    ):
        self.DB_USER = db_user
        self.DB_PASSWORD = db_password
        self.DB_HOST = db_host
        self.DB_PORT = db_port
        self.DB_NAME = db_name

    async def _get_connection(self) -> Connection:
        return await asyncpg.create_pool(
            password=self.DB_PASSWORD,
            user=self.DB_USER,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
            max_inactive_connection_lifetime=600
        )

    async def first_time_init(self):
        # 'postgresql://root:15386@127.0.0.1:5432/nkitbot_db'
        conn = await self._get_connection()
        await self._firt_init_user(conn)
        await self._firt_init_teacher(conn)
        await conn.close()

    async def _firt_init_user(self, conn):
        query = """CREATE TABLE IF NOT EXISTS students (
            user_id char(15),
            group_student char(5)

        );"""
        await conn.execute(query=query)

    async def _firt_init_teacher(self, conn):
        query = """CREATE TABLE IF NOT EXISTS teachers (
            user_id char(15),
            code text
        );"""
        await conn.execute(query=query)

    async def init_teacher(self, auth_key, teacher_id) -> bool:
        ...
    

    async def is_code_exists(self, code):
        query = f"SELECT EXISTS(SELECT * FROM teachers WHERE code = '{code}')" 
        conn = await self._get_connection()
        response = await conn.fetch(query)
        return response[0].get("exists")
            

           
        

    async def init_student(self, groups, user_id) -> bool:
        query = ("INSERT INTO students (user_id, group_student)"
                 f" VALUES ('{user_id}', '{groups}' );")
        conn = await self._get_connection()
        await conn.execute(query)
        await conn.close()


    async def init_admin(self) -> bool:
        pass

    async def get_users_list(self) -> list:
        conn = await self._get_connection()
        result = await conn.fetch('SELECT * FROM teachers;')
        await conn.close()
        return result
