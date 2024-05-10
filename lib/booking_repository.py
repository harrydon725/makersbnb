from lib.booking import *
class BookingRepository:
    def __init__(self, connection):
        self.connection = connection

    def find_by_spaceid(self, spaceid):
        booking_list = []
        rows = self.connection.execute('SELECT * FROM bookings WHERE spaceid = %s',[spaceid])
        if rows:
            for row in rows:
                existing_booking = Booking(row['id'],row['booking_date'], row['userid'],row['spaceid'])
                booking_list.append(existing_booking)
            return booking_list
        else:
            return booking_list
        
    def create(self, booking):
        self.connection.execute('INSERT INTO bookings (booking_date, userid, spaceid) Values(%s, %s, %s)',[str(booking.booking_date), booking.userid,  booking.spaceid])
        
    def find_by_id(self, id):
        rows = self.connection.execute('SELECT * FROM bookings WHERE id = %s',[id])
        if rows:
            row = rows[0]
            return Booking(row['id'], row['booking_date'], row['userid'],row['spaceid'])
        else:
            raise Exception("Booking not found!")

    def all(self):
        rows = self.connection.execute('SELECT * FROM bookings')
        booking_list = []
        for row in rows:
            current_booking = Booking(row['id'], str(row['booking_date']),row['userid'],row['spaceid'])
            booking_list.append(current_booking)
        return booking_list

    def find_all_bookings_user(self, userid):
        rows = self.connection.execute('SELECT * FROM users JOIN bookings ON users.id = bookings.userid WHERE bookings.userid = %s',[userid])
        user_bookings = []
        if rows:
            for row in rows:
                existing_booking = Booking(row['id'],row['booking_date'], row['userid'],row['spaceid'])
                user_bookings.append(existing_booking)
            return user_bookings
        else:
            return user_bookings

    def find_all_bookings_owner(self, ownerid):
        rows = self.connection.execute('SELECT * FROM bookings JOIN spaces ON spaces.id = bookings.spaceid WHERE spaces.ownerid = %s', [ownerid])
        owner_bookings = []
        if rows:
            for row in rows:
                existing_booking = Booking(row['id'],row['booking_date'], row['userid'],row['spaceid'])
                owner_bookings.append(existing_booking)
            return owner_bookings
        else:
            return owner_bookings


