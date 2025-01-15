from src.database.database_connection import DatabaseConnection
from src.models.entities.dogs import Dog
from typing import List, Optional

class DogModel:
    """
    A model class to interact with the dogs' data in the database.
    It provides methods to save, retrieve, and update dog records.
    """

    @classmethod
    def save_dog(cls, dog: Dog) -> bool:
        try:
            connection = DatabaseConnection.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO dogs (dogid, dogname, breed, age, userid, imageurl) VALUES (?, ?, ?, ?, ?, ?)",
                    (dog.dogid, dog.dogname, dog.breed, dog.age, dog.userid, dog.imageurl)
                )
                connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_dog_by_user(cls, userid: str) -> List[Dog]:
        try:
            connection = DatabaseConnection.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM dogs WHERE userid = ?", (userid,)
                )
                rows = cursor.fetchall()
                dogs = []
                for row in rows:
                    dog = Dog(row[0], row[1], row[2], row[3], row[4], row[5])
                    dogs.append(dog)
                return dogs
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_dog_by_id(cls, dogid: str) -> Optional[Dog]:
        try:
            connection = DatabaseConnection.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM dogs WHERE dogid = ?", (dogid,)
                )
                row = cursor.fetchone()
                if row:
                    return Dog(row[0], row[1], row[2], row[3], row[4], row[5])
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def get_dogs_by_user_id(userid: str) -> List[Dog]:
        try:
            connection = DatabaseConnection.get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT dogid, dogname, breed, age, imageurl FROM dogs WHERE userid = ?", (userid,))
                rows = cursor.fetchall()
                dogs = []
                if rows:
                    for row in rows:
                        dogs.append(Dog(row[0], row[1], row[2], row[3], userid, row[4]))
                return dogs
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def update_dog(dog: Dog) -> None:
        try:
            connection = DatabaseConnection.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE dogs SET dogname = ?, breed = ?, age = ?, imageurl = ? WHERE dogid = ?",
                    (dog.dogname, dog.breed, dog.age, dog.imageurl, dog.dogid)
                )
                connection.commit()
        except Exception as ex:
            connection.rollback()
            raise Exception(ex)