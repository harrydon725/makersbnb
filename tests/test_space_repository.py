from lib.space_repository import *
from lib.space import *
import pytest
def test_space_repo_all(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    spacerepo = SpaceRepository(db_connection)
    assert spacerepo.all() == [Space(1, 'Studio apartment', 100, '2024-05-20', '2025-05-20', 1), Space(2, '3 bedroom flat', 250, '2024-05-10', '2024-12-10', 2), Space(3, 'Penthouse', 500, '2024-05-25', '2026-05-25', 3), Space(4, 'Town house', 180, '2024-06-25', '2026-10-28', 3)]
def test_space_repo_find_by_id_valid(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    spacerepo = SpaceRepository(db_connection)
    assert spacerepo.find_by_id(1) == Space(1, 'Studio apartment', 100, '2024-05-20', '2025-05-20', 1)
def test_space_repo_find_by_id_invalid(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    spacerepo = SpaceRepository(db_connection)
    with pytest.raises(Exception) as e:
        spacerepo.find_by_id(5)
    error_message = str(e.value)
    assert error_message == "Space not found!"
def test_space_repo_create_space(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    spacerepo = SpaceRepository(db_connection)
    newspace = Space(None,'The White House', 200, '2024-12-12','2025-12-12',2)
    spacerepo.create(newspace)
    assert spacerepo.find_by_id(5) ==  Space(5,'The White House', 200, '2024-12-12','2025-12-12',2)
def test_is_available_true(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    spacerepo = SpaceRepository(db_connection)
    assert spacerepo.is_available(1,'2002-12-20') ==True
def test_is_available_false(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    spacerepo = SpaceRepository(db_connection)
    assert spacerepo.is_available(1,'2024-06-10') == False


def test_in_window_valid_1result(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    spacerepo = SpaceRepository(db_connection)
    date = datetime.strptime(str("2026-10-27"), '%Y-%m-%d').date()
    assert spacerepo.in_window(date) == [Space(4,'Town house',180,'2024-06-25', '2026-10-28', 3)]

def test_in_window_valid_multiple_results(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    spacerepo = SpaceRepository(db_connection)
    date = datetime.strptime(str("2025-05-19"), '%Y-%m-%d').date()
    assert spacerepo.in_window(date) == [Space(1,'Studio apartment',100,'2024-05-20', '2025-05-20', 1), Space(3, 'Penthouse',500,'2024-05-25', '2026-05-25',3), Space(4, "Town house",180, '2024-06-25', '2026-10-28',3 )]


def test_in_window_invalid(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    spacerepo = SpaceRepository(db_connection)
    date =  datetime.strptime(str("3000-05-19"), '%Y-%m-%d').date()
    assert spacerepo.in_window(date) == [f"There was no available Spaces for 3000-05-19"]
    pass
















