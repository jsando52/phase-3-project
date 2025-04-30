import json
from decimal import Decimal
import datetime

# used to determine whether which function to call based on the filter and sort order selected
def searchQuery(search_Json, conn):
    # Extract JSON information
    filter = search_Json.get("Filter")
    sorting = search_Json.get("Sort")
    search = search_Json.get("Query")
    # Determine filter choice
    match filter:
        case "Sort By Title":
            return sortByTitle(search, sorting, conn)
        case "Sort By Retailer":
            return sortByRetailer(search, sorting, conn)
        case "Sort By Price":
            return sortByPrice(search, sorting, conn)

# sorts by title, can be in either ASC or DESC order
def sortByTitle(query, sort, conn):
    sort = "ASC" if sort.upper() == "ASC" else "DESC"
    sql = f'''
        SELECT title, author, genre
        FROM book
        WHERE title LIKE %s
        Order by title {sort}
        '''
    cursor = conn.cursor()
    cursor.execute(sql, (f'%{query}%',))
    return SQLToJSON(cursor)

# sorts by retailer title, order doesn't really matter but it's there nonetheless
def sortByRetailer(query, sort, conn):
    sort = "ASC" if sort.upper() == "ASC" else "DESC"
    sql = f'''
        SELECT name, title, author, genre, price
        FROM book, retailer, price
        WHERE book.book_id = price.book_id
        AND retailer.retailer_id = price.retailer_id
        AND name LIKE %s
        Order by name {sort}
        '''
    cursor = conn.cursor()
    cursor.execute(sql, (f'%{query}%',))
    return SQLToJSON(cursor)

# sorts book info by price, in either ASC or DESC order
def sortByPrice(query, sort, conn):
    sort = "ASC" if sort.upper() == "ASC" else "DESC"
    sql = f'''
        SELECT price, name, title, author, genre
        FROM book, retailer, price
        WHERE book.book_id = price.book_id
        AND retailer.retailer_id = price.retailer_id
        AND title LIKE %s
        Order by price {sort}
        '''
    cursor = conn.cursor()
    cursor.execute(sql, (f'%{query}%',))
    return SQLToJSON(cursor)

# when clicking on a book, expands the book's information from the database in one area
def expandBookData(book_name, conn):
    print(book_name)
    sql = f'''
        SELECT price, name, availability, title, author, isbn, pub_date, genre, rating, review_text, review_date
        FROM book
        JOIN price ON book.book_id = price.book_id
        JOIN retailer ON retailer.retailer_id = price.retailer_id
        JOIN reviews ON book.book_id = reviews.book_id
        AND title = %s
        ORDER BY price ASC
    '''
    cursor = conn.cursor()
    cursor.execute(sql, (book_name,))
    return SQLToJSON(cursor)


# convert SQL Query results into JSON, making sure decimals are up to 2 decmial points
def SQLToJSON(cursor):  
    columns = [column[0] for column in cursor.description]
    data = []

    for row in cursor.fetchall():
        row_dict = {}
        for col, val in zip(columns, row):
            if isinstance(val, Decimal):
                row_dict[col] = f"{val:.2f}"
            elif isinstance(val, (datetime.date, datetime.datetime)):
                val = val.isoformat()
            else:
                row_dict[col] = val
        data.append(row_dict)

    json_data = json.dumps(data, indent=4)
    return json_data
