from lib.booking import *
def test_bookingeq():
    booking1 = Booking(1,'2024-08-23',1,1)
    booking2 = Booking(1,'2024-08-23',1,1)
    assert booking1 == booking2

def test_bookingeq_noteq():
    booking1 = Booking(1,'2024-08-23',1,1)
    booking2 = Booking(1,'2014-08-23',1,1)
    assert booking1 != booking2

def test_booking_repr():
    booking1 = Booking(1,'2023-08-23',2,2)
    assert str(booking1) == "Booking(1, 2023-08-23, 2, 2)"
