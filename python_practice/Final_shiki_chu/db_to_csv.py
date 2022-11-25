import csv
from configparser import ConfigParser
import mysql.connector


def readDBConfig(filename='config.ini', section='mysql'):
    db = {}

    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]

    else:
        print("Error with config.ini file!")

    return db

# connect to database, and select the data
try:
    creds = readDBConfig()
    conn = mysql.connector.MySQLConnection(**creds)
    cursor = conn.cursor()

    query = """SELECT * FROM employees """

    cursor.execute(query)
    rows = cursor.fetchone()

    # create the column header for csv output
    colHeader = ['id','Fname','Lname','email','password','gross_income','fex_tax','on_tax','ccp','ei','net_income']

    # create csv
    with open('employees_db.csv', 'w') as employees_db:
        writer = csv.writer(employees_db)
        # write the column header
        writer.writerow(colHeader)
        # write the data
        writer.writerow(rows)
        writer.writerows(cursor.fetchall())

    cursor.close()
    conn.close()

except Exception as e:
    print(e)