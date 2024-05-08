from lib.booking_repository import *
from lib.booking import *
import pytest

def test_booking_repo_all(db_connection):
    db_connection.seed('seeds/temp_seed.sql')
    bookrepo = BookingRepository(db_connection)
    assert bookrepo.all() == [ Booking(1,'2024-05-06',2,1) , Booking(2,'2024-05-07',1,2)]

def test_booking_repo_find_by_id_valid(db_connection):
    db_connection.seed('seeds/temp_seed.sql')
    bookrepo = BookingRepository(db_connection)
    assert bookrepo.find_by_id(1) == Booking(1,'2024-05-06',2,1)

def test_booking_repo_find_by_id_invalid(db_connection):
    db_connection.seed('seeds/temp_seed.sql')
    bookrepo = BookingRepository(db_connection)
    with pytest.raises(Exception) as e:
        bookrepo.find_by_id(3)
    error_message = str(e.value) 
    assert error_message == "Booking not found!"

def test_booking_repo_find_by_spaceid_valid(db_connection):
    db_connection.seed('seeds/temp_seed.sql')
    bookrepo = BookingRepository(db_connection)
    assert bookrepo.find_by_spaceid(1) == [Booking(2,'2024-05-07',1,2)]

def test_booking_repo_find_by_spaceid_invalid(db_connection):
    db_connection.seed('seeds/temp_seed.sql')
    bookrepo = BookingRepository(db_connection)
    assert bookrepo.find_by_spaceid(4) == []
    
