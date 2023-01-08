from database import Database

db_manager = Database(
    db_host='127.0.0.1',
    db_name='nkitbot_db',
    db_password='15386',
    db_port='5432',
    db_user='root'
)


class UserService:
    @staticmethod
    async def init_user(
        group: str,
        user_id: int,
        key: str = None
    ) -> bool:
        if not group:
            raise AttributeError('group us required argument')
        if not user_id:
            raise AttributeError('user_id us required argument')
        if group in ['teacher', 'admin'] and not key:
            raise AttributeError('Key is required for teacher and admin')

        if group == 'teacher':
            return await db_manager.init_teacher(
                user_id,
                key
            )
        if group == 'admin':
            return await db_manager.init_admin()
        if group == 'student':
            return await db_manager.init_student()
