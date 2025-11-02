import pytest
from books_collector import BooksCollector


# --- фикстура для инициализации объекта класса ---
@pytest.fixture
def collector():
    return BooksCollector()


# --- 1. Тест: добавление новой книги ---
@pytest.mark.parametrize("book_name", ["Книга A", "Очень длинное название книги до 40 символов"])
def test_add_new_book_adds_book_correctly(collector, book_name):
    collector.add_new_book(book_name)
    assert book_name in collector.get_books_genre()
    assert collector.get_book_genre(book_name) == ""


# --- 2. Тест: некорректные имена книг (пустое, слишком длинное) ---
@pytest.mark.parametrize("book_name", ["", "А" * 41])
def test_add_new_book_invalid_name_not_added(collector, book_name):
    collector.add_new_book(book_name)
    assert book_name not in collector.get_books_genre()


# --- 3. Тест: установка жанра существующей книге ---
def test_set_book_genre_sets_valid_genre(collector):
    collector.add_new_book("Книга B")
    collector.set_book_genre("Книга B", "Фантастика")
    assert collector.get_book_genre("Книга B") == "Фантастика"


# --- 4. Тест: установка жанра несуществующей книге ---
def test_set_book_genre_nonexistent_book_does_nothing(collector):
    collector.set_book_genre("Неизвестная книга", "Фантастика")
    assert "Неизвестная книга" not in collector.get_books_genre()


# --- 5. Тест: получение списка книг с конкретным жанром ---
def test_get_books_with_specific_genre_returns_correct_list(collector):
    collector.add_new_book("Книга C1")
    collector.add_new_book("Книга C2")
    collector.set_book_genre("Книга C1", "Фантастика")
    collector.set_book_genre("Книга C2", "Фантастика")
    result = collector.get_books_with_specific_genre("Фантастика")
    assert set(result) == {"Книга C1", "Книга C2"}


# --- 6. Тест: получение детских книг (исключая жанры с возрастным рейтингом) ---
def test_get_books_for_children_excludes_age_rated_genres(collector):
    collector.add_new_book("Книга D1")
    collector.add_new_book("Книга D2")
    collector.set_book_genre("Книга D1", "Фантастика")  # подходит детям
    collector.set_book_genre("Книга D2", "Ужасы")       # возрастной рейтинг
    result = collector.get_books_for_children()
    assert "Книга D1" in result
    assert "Книга D2" not in result


# --- 7. Тест: добавление книги в избранное ---
def test_add_book_in_favorites_adds_correctly(collector):
    collector.add_new_book("Книга E")
    collector.add_book_in_favorites("Книга E")
    assert "Книга E" in collector.get_list_of_favorites_books()


# --- 8. Тест: нельзя добавить в избранное одну и ту же книгу дважды ---
def test_add_book_in_favorites_twice_does_not_duplicate(collector):
    collector.add_new_book("Книга F")
    collector.add_book_in_favorites("Книга F")
    collector.add_book_in_favorites("Книга F")
    favorites = collector.get_list_of_favorites_books()
    assert favorites.count("Книга F") == 1


# --- 9. Тест: удаление книги из избранного ---
def test_delete_book_from_favorites_removes_book(collector):
    collector.add_new_book("Книга G")
    collector.add_book_in_favorites("Книга G")
    collector.delete_book_from_favorites("Книга G")
    assert "Книга G" not in collector.get_list_of_favorites_books()


# --- 10. Тест: метод get_books_genre возвращает словарь с книгами и жанрами ---
def test_get_books_genre_returns_full_dict(collector):
    collector.add_new_book("Книга H")
    collector.set_book_genre("Книга H", "Комедии")
    result = collector.get_books_genre()
    assert result == {"Книга H": "Комедии"}