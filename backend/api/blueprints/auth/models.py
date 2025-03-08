from api.extensions import db
from sqlalchemy import exists
from sqlalchemy.orm import Mapped, mapped_column
from bcrypt import checkpw, hashpw, gensalt

# User Model
class User(db.Model):
    __tablename__ = 'users'

    # Fields
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)
    
    @property
    def password(self):
        raise AttributeError("password cannot be read directly")
    
    @password.setter
    def password(self, raw_password):
        self.password_hash = hashpw(raw_password.encode("utf-8"), gensalt()).decode("utf-8")

    def check_password(self, raw_password):
        return checkpw(raw_password.encode("utf-8"), self.password_hash.encode("utf-8"))

    @classmethod
    def is_username_taken(cls, username):
        return db.session.query(exists().where(cls.username == username)).scalar()

    @classmethod
    def is_email_taken(cls, email):
        return db.session.query(exists().where(cls.email == email)).scalar()

    @classmethod
    def is_user_admin(cls, user_id):
        user = cls.query.get(user_id)
        return user.is_admin if user else False