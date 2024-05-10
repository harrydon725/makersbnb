from datetime import datetime
class Booking:
    def __init__(self,id, booking_date, userid, spaceid):
        self.id = id
        self.userid = userid
        self.spaceid = spaceid
        self.booking_date = datetime.strptime(str(booking_date), '%Y-%m-%d').date() #In the format yyyy-mm-dd

    def __eq__(self,other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Booking({self.id}, {str(self.booking_date)}, {self.userid}, {self.userid})"
        
        
        
        
        
        
        
