# lib/testing/test_many_to_many.py

import pytest
from lib.models import Book, Author, Contract

@pytest.fixture(autouse=True)
def reset_classes():
    """Reset class variables before each test"""
    Book.all_books = []
    Author.all_authors = []
    Contract.all_contracts = []

def test_book_init():
    """Test Book class initializes with title"""
    book = Book("Title")
    assert book.title == "Title"

def test_author_init():
    """Test Author class initializes with name"""
    author = Author("Name")
    assert author.name == "Name"

def test_contract_init():
    """Test Contract class initializes with author, book, date, royalties"""
    author = Author("Name")
    book = Book("Title")
    contract = Contract(author, book, "2023-10-01", 1000)
    assert contract.author == author
    assert contract.book == book
    assert contract.date == "2023-10-01"
    assert contract.royalties == 1000

def test_contract_validates_author():
    """Test Contract class validates author of type Author"""
    book = Book("Title")
    try:
        Contract("Not an author", book, "2023-10-01", 1000)
    except Exception as e:
        assert str(e) == "author must be an instance of Author"

def test_contract_validates_book():
    """Test Contract class validates book of type Book"""
    author = Author("Name")
    try:
        Contract(author, "Not a book", "2023-10-01", 1000)
    except Exception as e:
        assert str(e) == "book must be an instance of Book"

def test_contract_validates_date():
    """Test Contract class validates date of type str"""
    author = Author("Name")
    book = Book("Title")
    try:
        Contract(author, book, 12345, 1000)
    except Exception as e:
        assert str(e) == "date must be a string"

def test_contract_validates_royalties():
    """Test Contract class validates royalties of type int"""
    author = Author("Name")
    book = Book("Title")
    try:
        Contract(author, book, "2023-10-01", "Not an int")
    except Exception as e:
        assert str(e) == "royalties must be an integer"

def test_author_has_contracts():
    """Test Author class has method contracts() that returns a list of its contracts"""
    author = Author("Name")
    book = Book("Title")
    contract = Contract(author, book, "2023-10-01", 1000)
    assert author.contracts() == [contract]

def test_author_has_books():
    """Test Author class has method books() that returns a list of its books"""
    author = Author("Name")
    book = Book("Title")
    Contract(author, book, "2023-10-01", 1000)
    assert author.books() == [book]

def test_book_has_contracts():
    """Test Book class has method contracts() that returns a list of its contracts"""
    author = Author("Name")
    book = Book("Title")
    contract = Contract(author, book, "2023-10-01", 1000)
    assert book.contracts() == [contract]

def test_book_has_authors():
    """Test Book class has method authors() that returns a list of its authors"""
    author = Author("Name")
    book = Book("Title")
    Contract(author, book, "2023-10-01", 1000)
    assert book.authors() == [author]

def test_author_can_sign_contract():
    """Test Author class has method sign_contract() that creates a contract for an author and book"""
    author = Author("Name")
    book = Book("Title")
    contract = author.sign_contract(book, "2023-10-01", 1000)
    assert isinstance(contract, Contract)
    assert contract.author == author
    assert contract.book == book
    assert contract.date == "2023-10-01"
    assert contract.royalties == 1000

def test_author_has_total_royalties():
    """Test Author class has method total_royalties that gets the sum of all its related contracts' royalties"""
    author = Author("Name")
    book1 = Book("Title 1")
    book2 = Book("Title 2")
    Contract(author, book1, "2023-10-01", 1000)
    Contract(author, book2, "2023-10-01", 2000)
    assert author.total_royalties() == 3000

def test_contract_contracts_by_date():
    """Test Contract class has method contracts_by_date() that sorts all contracts by date"""
    author1 = Author("Name 1")
    author2 = Author("Name 2")
    book1 = Book("Title 1")
    book2 = Book("Title 2")
    contract1 = Contract(author1, book1, "2023-10-01", 1000)
    contract2 = Contract(author2, book2, "2023-09-01", 2000)
    contract3 = Contract(author1, book2, "2023-09-01", 1500)
    assert Contract.contracts_by_date("2023-09-01") == [contract2, contract3]
    assert Contract.contracts_by_date("2023-10-01") == [contract1]