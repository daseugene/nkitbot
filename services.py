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
        name: str,
        user_id: int,
    ) -> bool:
        await db_manager.init_student(name, user_id)


class TeacherService:
    pass
