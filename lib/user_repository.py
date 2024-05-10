from lib.user import *

class UserRepository:
    def __init__(self, connection):
        self.connection = connection
        self.users = []

    def find_by_id(self,id):
        rows = self.connection.execute('SELECT * FROM users WHERE id = %s',[id])
        if rows:
            row = rows[0]
            return User(row['id'], row['email_address'],row['password'])
        else:
            raise Exception("User not found!")


    def create(self, user):
        rows = self.connection.execute('INSERT INTO users (email_address, password) Values(%s, %s) RETURNING id',[user.email, user.password])
        row = rows[0]
        user.id = row['id']
        return user


    def all(self):
        rows = self.connection.execute('SELECT * FROM users')
        user_list = []
        for row in rows:
            current_user = User(row['id'],row['email_address'],row['password'])
            user_list.append(current_user)
        return user_list

    def find_bookings_with_name(self,userid):
        rows = self.connection.execute(f"SELECT * FROM bookings WHERE userID = {userid}")
        listbookings = []
        print(rows)
        for row in rows:
            outputstring = ""
            spaces = self.connection.execute(f"SELECT title FROM spaces WHERE id = {row['spaceid']}")
            print(spaces)
            name = spaces[0]['title']
            outputstring = f"{name} {str(row['booking_date'])}"
            print(outputstring)
            listbookings.append(outputstring)
        return listbookings

