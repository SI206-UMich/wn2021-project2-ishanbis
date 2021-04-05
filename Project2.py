from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest

def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    #test cases for this function don't match what is on the actual website when url is searched
    t = []
    f = open(filename)
    soup = BeautifulSoup(f, "html.parser")
    f.close()

    div = soup.find("div", class_="mainContentContainer")
    books = div.find_all("tr")

    for book in books:
        a1 = book.find("a", class_="bookTitle")
        title = a1.find("span").text

        a2 = book.find("a", class_="authorName")
        author = a2.find("span").text

        t.append((title, author))
    
    return t

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"  
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    lst = []

    div = soup.find("div", class_="mainContentFloat")
    table = div.find("table")
    trs = table.find_all("tr")

    for tr in trs:
        td = tr.find_all("td")[0]
        href = td.find("a")["href"]
        lst.append("https://www.goodreads.com" + href)

    return lst[:10]

def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    #can't understand problem
    #get link prolem? getting index out of range problem
    r = requests.get(book_url)

    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.find("h1", id="bookTitle").text.strip()
    author = soup.find("a", class_="authorName").text.strip()
    pages_string = soup.find("span", itemprop="numberOfPages").text.strip()
    pages_list = re.findall(r"\d{1,}", pages_string)
    pages = int(pages_list[0])

    """
    div1 = soup.find("div", class_="leftContainer")
    div2 = div1.find("div", class_="last col")
    title_before = div2.find("h1").text
    title = title_before.strip()

    author_before = div2.find("a", class_="authorName").find("span").text
    author = author_before.strip()

    details = div2.find("div", class_="uitext darkGreyText")
    div3 = details.find("div", class_="row")
    pages_string = div3.find_all("span")[1].text.strip()
    """


    t = (title, author, pages)
    
    return t

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    f = open(filepath)
    soup = BeautifulSoup(f, "html.parser")
    f.close()

    lst = []

    div1 = soup.find("div", class_="mainContent")
    categories = div1.find_all("div", class_="category clearFix")

    for category in categories:
        genre = category.find("a").find("h4").text.strip()
        title = category.find("div", class_="category__winnerImageContainer").find("img")["alt"]
        href = category.find("a")["href"]
        lst.append((genre, title, href))
    
    return lst 

def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    #opening file name problem
    #opening it wrong in test too??
    
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), "w") as f:
        obj = csv.writer(f, delimiter=",")
        obj.writerow(["Book Title", "Author Name"])
        for row in data:
            obj.writerow(row)

def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filepath), 'r') as f:    
        data = f.read()
    
    #f = open(filepath)
    soup = BeautifulSoup(data, "html.parser")
    #f.close()

    #url = "https://www.goodreads.com/book/show/42975172-the-testaments?ac=1&from_search=true&qid=gmLO3ySp28&rank=1"
    #resp = requests.get(url)
    #soup = BeautifulSoup(resp.content, 'html.parser')

    div = soup.find("div", class_="readable stacked")
    br = div.find("span", id="freeText4791443123668479528").text



    regex = r"\b[A-Z]\w.\w+(?:\s[A-Z]\w+)+"
    #lst = br.split(".")[1:]
    #print(lst)
    ec = []

    temp = re.findall(regex, br)
    for item in temp:
        ec.append(item)
    
    return ec

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        lst = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(lst), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(lst), list)
        # check that each item in the list is a tuple
        count = 0
        for item in lst:
            if type(item) != tuple:
                count += 1
        self.assertEqual(count, 0)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(lst[0][0], "Harry Potter and the Deathly Hallows (Harry Potter, #7)")
        self.assertEqual(lst[0][1], "J.K. Rowling")
        # check that the last title is correct (open search_results.htm and find it)
        #change it
        self.assertEqual(lst[-1][0], "Harry Potter: The Prequel (Harry Potter, #0.5)")
        self.assertEqual(lst[-1][1], "J.K. Rowling")

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        count = 0
        for url in TestCases.search_urls:
            if type(url) != str:
                count += 1
        self.assertEqual(count, 0)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        count2 = 0
        for url in TestCases.search_urls:
            if "https://www.goodreads.com/book/show/" in url == False:
                count2 += 1
        self.assertEqual(count2, 0)

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for item in TestCases.search_urls:
            summaries.append(get_book_summary(item))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)

        count = 0
        for item in summaries:
            # check that each item in the list is a tuple
            if type(item) != tuple:
                count += 1
            # check that each tuple has 3 elements
            if len(item) != 3:
                count += 1 
            # check that the first two elements in the tuple are string
            if type(item[0]) != str and type(item[1]) != str:
                count += 1
            # check that the third element in the tuple, i.e. pages is an int
            if type(item[2]) != int:
                count += 1
            # check that the first book in the search has 337 pages
        if summaries[0][2] != 337:
            count += 1
        
        self.assertEqual(count, 0)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        lst = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(lst), 20)
        
        count = 0
        for item in lst:
            # assert each item in the list of best books is a tuple
            if type(item) != tuple:
                count += 1
            # check that each tuple has a length of 3
            if len(item) != 3:
                count += 1
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(lst[0][0], "Fiction")
        self.assertEqual(lst[0][1], "The Midnight Library")
        self.assertEqual(lst[0][2], "https://www.goodreads.com/choiceawards/best-fiction-books-2020")
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(lst[-1][0], "Picture Books")
        self.assertEqual(lst[-1][1], "Antiracist Baby")
        self.assertEqual(lst[-1][2], "https://www.goodreads.com/choiceawards/best-picture-books-2020")

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        lst = get_titles_from_search_results("search_results.htm")
        # call write csv on the variable you saved and 'test.csv'
        write_csv(lst, "test.csv")
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        f = open("test.csv", "r")
        csv_reader = csv.reader(f)
        csv_lines = []
        for i in csv_reader:
            csv_lines.append(i)
        f.close()
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0], ["Book Title" , "Author Name"])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], ["Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling"])
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'Julian Harrison (Introduction)'
        self.assertEqual(csv_lines[-1], ["Harry Potter: The Prequel (Harry Potter, #0.5)", "J.K. Rowling"])


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



