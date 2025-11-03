import pytest
from books_collector import BooksCollector


# --- фикстура для инициализации объекта класса ---
@pytest.fixture
def collector():
    return BooksCollector()