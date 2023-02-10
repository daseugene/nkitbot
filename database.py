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
            group_no varchar(30)
        );"""
        await conn.execute(query=query)

    async def _firt_init_teacher(self, conn):
        query = """CREATE TABLE IF NOT EXISTS teachers (
            user_id char(15),
            name char(30),
            auth_code char(10)
        );"""
        await conn.execute(query=query)

    async def init_teacher(
        self,
        user_id: int,
        key: str
    ) -> bool:
        '''
        INSERT INTO teachers (auth_code)
        VALUES ('key')
        ''',  # user_id(int): teacher_id, key(str): auth_code

      #  async def check_auth_teacher(conn, table, field, value, key):
       #     query = f"SELECT auth_code FROM teachers WHERE auth_code = 'key', key"
        #
        #   row = await conn.fetchrow(query)

    # """Проверяем и авторизуем учителя

     #   Args:
     #       user_id (int): Telegram ID пользователя
      #      key (str): Ключ-пароль

     #   Returns:
      #      bool: True если пароль верный

     #   Тут мы должны взять ключ, который передал юзер,
     #   после чего мы ищем в базе данных запись с этим ключом
   #     если запись найдена - вписываем в нее user_id
     #   и обязательно удаляем из неё ключ.
    #    """
    # pass

    async def init_student(
        self,
        group_no: str,
        user_id: int
    ) -> bool:
        query = ("INSERT INTO students (user_id, group_no)"
                 f" VALUES ('{user_id}', '{group_no}' )")
        conn = await self._get_connection()
        await conn.execute(query)
        await conn.close()

    async def init_admin(self) -> bool:
        pass

    async def get_users_list(self) -> list:
        conn = await self._get_connection()
        result = await conn.fetch('SELECT * FROM "teachers";')
        await conn.close()
        return result
