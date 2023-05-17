from database import Database

db_manager = Database(
    db_host='localhost',
    db_name='nkitbot_db',
    db_password='4336',
    db_port='5432',
    db_user='root'
)


class GetResult:
    @staticmethod
    async def gett_result():
        result = await db_manager.get_schedule()



class StudentService:
    @staticmethod
    async def init_student(
        groups: str,
        user_id: int,
    ) -> bool:
        await db_manager.init_student(groups, user_id)
    

    @staticmethod
    async def student_schedule(
        user_id: int
    ) -> bool:
        await db_manager.student_schedule(user_id)

    @staticmethod
    async def get_schedule(
        day: str,
    ) -> bool:
        await db_manager.get_schedule(day)


class TeacherService:
    @staticmethod
    async def init_teacher(
        teacher_id: int,
        code: str
    ) -> bool:
        await db_manager.init_teacher(teacher_id, code)
    
    @staticmethod
    async def check_code(
        code: str
    ) -> bool:
        return await db_manager.is_code_exists(code)
    
    @staticmethod
    async def finish_auth(
        teacher_id: int
    ) -> bool:
        await db_manager.auth_final(teacher_id)


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
        
    @staticmethod
    async def final_auth(
        admin_id: int
    ) -> bool:
        await db_manager.auth_ad_final(admin_id)


class Result:
    @staticmethod
    async def get_schedule(
        result
    ): print()