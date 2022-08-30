from sqlalchemy.orm import sessionmaker

from repository.model.user import User, ENGINE


class SessionContext:
    def __init__(self):
        print('init')
        session_maker = sessionmaker(bind=ENGINE, expire_on_commit=False)
        self.session = session_maker()

    def __enter__(self):
        print('enter')
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')
        self.session.flush()
        self.session.commit()
        self.session.close()


class UserRepository:
    def __init__(self):
        pass

    def get(self, user_id: int):
        with SessionContext() as session:
            user = session.query(User).get(user_id)
        return {
            'id': user.id,
            'name': user.name,
            'age': user.age
        }
