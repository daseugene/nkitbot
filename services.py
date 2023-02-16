from database import Database

db_manager = Database(
    db_host='localhost',
    db_name='nkitbot_db',
    db_password='4336',
    db_port='5432',
    db_user='root'
)


class StudentService:
    @staticmethod
    async def init_student(
        groups: str,
        user_id: int,
    ) -> bool:
        await db_manager.init_student(groups, user_id)


class TeacherService:
    @staticmethod
    async def init_teacher(
        teacher_id: int,
        code: str,
    ) -> bool:
        await db_manager.init_teacher(teacher_id, code)
    
    @staticmethod
    async def check_code(
        code: str
    ) -> bool:
        return await db_manager.is_code_exists(code)


class AdminService:
    @staticmethod
    async def init_admin(
        admin_id: int,
        code:str
    ) -> bool:
        await db_manager.init_admin(admin_id, code)
    
    @staticmethod
    async def check_admin_code(
        code: str
    ) -> bool:
        return await db_manager.is_admin_code_exists(code)
        