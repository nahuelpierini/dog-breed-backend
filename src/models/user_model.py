from src.models.entities.user import User
from src.database.database_connection import DatabaseConnection

class UserModel:
    """
    This class provides methods to interact with the users in the database.
    It includes functionalities for user login, registration, retrieval by ID, 
    and updating user information.
    """

    @classmethod
    def login(cls, user: User) -> User | None:
        try:
            connection = DatabaseConnection.get_connection()
            print("Connection successfully")

            with connection.cursor() as cursor:
                cursor.execute("SELECT userid, email, upassword, firstname, lastname, birthdate, country FROM users WHERE email = ?", (user.email,))
                row = cursor.fetchone()
                if row is not None:
                    hashed_password = row[2]
                    if User.check_password(hashed_password, user.upassword):
                        user = User(row[0], row[1], hashed_password, row[3], row[4], row[5], row[6])
                        return user
                return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(cls, userid: str) -> User | None:
        try:
            connection = DatabaseConnection.get_connection()
            print("Connection successfully")

            with connection.cursor() as cursor:
                cursor.execute("SELECT userid, email, firstname, lastname, birthdate, country FROM users WHERE userid = ?", (userid,))
                row = cursor.fetchone()
                if row is not None:
                    logged_user = User(row[0], row[1], None, row[2], row[3], row[4], row[5])
                    return logged_user
                return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register(cls, user: User) -> bool:
        try:
            connection = DatabaseConnection.get_connection()
            print("Connection successfully")

            # Check if email is already registered
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = ?", (user.email,))
                row = cursor.fetchone()
                if row is not None:
                    raise Exception("Email already registered")

                # If not, insert the new user
                hashed_password = User.generate_password(user.upassword)
                cursor.execute(
                    "INSERT INTO users (userid, email, upassword, firstname, lastname, birthdate, country) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (user.userid, user.email, hashed_password, user.firstname, user.lastname, user.birthdate, user.country)
                )
                connection.commit()
                return True
        except Exception as ex:
            raise Exception(str(ex))

    @classmethod
    def update_user(cls, user: User) -> bool:
        try:
            connection = DatabaseConnection.get_connection()
            print("Connection successfully")

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE users 
                    SET firstname = ?, lastname = ?, birthdate = ?, country = ?
                    WHERE userid = ?
                """, (user.firstname, user.lastname, user.birthdate, user.country, user.userid))
                
                connection.commit()
                return True
        except Exception as ex:
            raise Exception(ex)