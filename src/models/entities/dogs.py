class Dog:
    """
    A class to represent a dog.
    """

    def __init__(self, dogid: str, dogname: str, breed: str, age: int, userid: str, imageurl: str):
        self.dogid = dogid
        self.dogname = dogname
        self.breed = breed
        self.age = age
        self.userid = userid
        self.imageurl = imageurl