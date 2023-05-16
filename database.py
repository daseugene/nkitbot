from asyncpg.connection import Connection
import asyncpg


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


# ---- TEACHER ----
    async def _firt_init_teacher(self, conn):
        query = """CREATE TABLE IF NOT EXISTS teachers (
            user_id char(15),
            code text
        );"""
        await conn.execute(query=query)


    async def init_teacher(self, teacher_id, code) -> bool:
        query = f"UPDATE teachers SET user_id = '{teacher_id}' WHERE code = '{code}'"
        conn = await self._get_connection()
        await conn.execute(query)
        await conn.close()


    async def is_code_exists(self, code):
        query = f"SELECT EXISTS(SELECT * FROM teachers WHERE code = '{code}')" 
        conn = await self._get_connection()
        response = await conn.fetch(query)
        return response[0].get("exists")
    
    async def auth_final(self, teacher_id):
        query = f"UPDATE teachers SET code = ' ' WHERE user_id = '{teacher_id}'"
        conn = await self._get_connection()
        await conn.execute(query)
        await conn.close()



# --- STUDENT ---
    async def _firt_init_user(self, conn):
            query = """CREATE TABLE IF NOT EXISTS students (
                user_id char(15),
                group_student char(5)

            );"""
            await conn.execute(query=query)



    async def init_student(self, groups, user_id) -> bool:
        query = ("INSERT INTO students (user_id, group_student)"
                 f" VALUES ('{user_id}', '{groups}' );")
        conn = await self._get_connection()
        await conn.execute(query)
        await conn.close()


    async def student_schedule(self, user_id) -> bool:
        query = f"SELECT groups FROM students WHERE user_id = '{user_id}'"
        conn = await self._get_connection()
        response = await conn.fetch(query)
        await conn.close()
        print(response[0].get())
        

# --- ADMIN ---
    async def _first_init_admin(self, conn):
        query = """CREATE TABLE IF NOT EXISTS admins (
            user_id char(15),
            code text
        );"""
        await conn.execute(query=query)

    async def init_admin(self, code, admin_id) -> bool:
        query = f"UPDATE teachers SET user_id = '{admin_id}' WHERE code = '{code}'"
        conn = await self._get_connection()
        await conn.execute(query)
        await conn.close()

    async def is_admin_code_exists(self, code) -> bool:
        query = f"SELECT EXISTS(SELECT * FROM admins WHERE code = '{code}')"
        conn = await self._get_connection()
        response = await conn.fetch(query)
        return response[0].get("exists")
    
    async def auth_ad_final(self, admin_id):
        query = f"UPDATE teachers SET code = ' ' WHERE user_id = '{admin_id}'"
        conn = await self._get_connection()
        await conn.execute(query)
        await conn.close() 

# --- SERVICE --- 
    async def get_users_list(self) -> list:
        conn = await self._get_connection()
        result = await conn.fetch('SELECT * ')
        await conn.close()
        return result


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
        await self._first_init_admin(conn)
        await conn.close()
