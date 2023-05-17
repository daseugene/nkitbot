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
    

    @staticmethod
    async def student_schedule(
        user_id: int
    ) -> bool:
        await db_manager.student_schedule(user_id)

    @staticmethod
    async def get_schedule(
        day: str,
    ) -> str:
        result = await db_manager.get_schedule(day)
        return result


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

    @staticmethod
    async def create_attention(
        user_id: int,
        attention: str,
    ) -> bool:
        return await db_manager.create_attention(user_id, attention)
    
    @staticmethod
    async def send_attention_to_all(
    ) -> list:
        user_ids_list = await db_manager.get_all_user_list()
        return user_ids_list
    
    @staticmethod
    async def get_last_attention(
    ) -> str:
        message = await db_manager.get_last_attention()
        return message
    
    @staticmethod
    async def delete_old_attention(
    ) -> bool:
        await db_manager.delete_old_attention()

class Result:
    @staticmethod
    async def get_schedule(
        result
    ): print()
