import json
from decimal import Decimal

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

def sortByPrice(sort, conn):
    sort = "ASC" if sort.upper() == "ASC" else "DESC"
    sql = f'''
        SELECT price, name, title, author, genre
        FROM book, retailer, price
        WHERE book.book_id = price.book_id
        AND retailer.retailer_id = price.retailer_id
        Order by price {sort}
        '''
    cursor = conn.cursor()
    cursor.execute(sql)
    return SQLToJSON(cursor)

from decimal import Decimal

def SQLToJSON(cursor):  # Convert SQL Query results into JSON
    columns = [column[0] for column in cursor.description]
    data = []

    for row in cursor.fetchall():
        row_dict = {}
        for col, val in zip(columns, row):
            if isinstance(val, Decimal):
                row_dict[col] = float(val)
            else:
                row_dict[col] = val
        data.append(row_dict)

    json_data = json.dumps(data, indent=4)
    return json_data
