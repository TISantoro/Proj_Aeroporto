from app.database.db import SessionLocal
from app.models.user import User


def clear_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            db.delete(user)
        db.commit()
        print(f"{len(users)} usuários removidos do banco.")
    finally:
        db.close()


if __name__ == "__main__":
    clear_users()
