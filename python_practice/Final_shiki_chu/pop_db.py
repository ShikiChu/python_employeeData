import mysql.connector
from configparser import ConfigParser


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


# create function for different tax calculation:

def calc_fed_tax(gross_income):
    if gross_income <= 50197:
        tax = gross_income * 0.15
        return tax
    elif 50197 < gross_income <= 100392:
        tax = 50197 * 0.15 + \
              (gross_income - 50197) * 0.205
        return tax
    elif 100392 < gross_income <= 155625:
        tax = 50197 * 0.15 + \
              50195 * 0.205 + \
              (gross_income - 50197 - 50195) * 0.26
        return tax
    elif 155625 < gross_income <= 221708:
        tax = 50197 * 0.15 + \
              50195 * 0.205 + \
              55233 * 0.26 + \
              (gross_income - 50197 - 50195 - 55233) * 0.29
        return tax
    else:
        tax = 50197 * 0.15 + \
              50195 * 0.205 + \
              55233 * 0.26 + \
              66083 * 0.29 + \
              (gross_income - 50197 - 50195 - 55233 - 66083) * 0.33
        return tax


def calc_on_tax(gross_income):
    if gross_income <= 46226:
        tax = gross_income * 0.0505
        return tax
    elif 46226 < gross_income <= 92454:
        tax = 46226 * 0.0505 + \
              (gross_income - 46226) * 0.0915
        return tax
    elif 92454 < gross_income <= 150000:
        tax = 46226 * 0.0505 + \
              92454 * 0.0915 + \
              (gross_income - 46226 - 92454) * 0.1116
        return tax
    elif 150000 < gross_income <= 220000:
        tax = 46226 * 0.0505 + \
              92454 * 0.0915 + \
              150000 * 0.1116 + \
              (gross_income - 46226 - 92454 - 150000) * 0.1216
        return tax
    else:
        tax = 46226 * 0.0505 + \
              92454 * 0.0915 + \
              150000 * 0.1116 + \
              220000 * 0.1216 + \
              (gross_income - 46226 - 92454 - 150000 - 220000) * 0.1316
        return tax


def calc_cpp(gross_income):
    if gross_income < 61400:
        ccp = gross_income * 0.057
        return ccp
    elif gross_income >= 61400:
        ccp = 61400 * 0.057
        return ccp


def calc_ei(gross_income):
    if gross_income < 60300:
        ei = gross_income * 0.0158
        return ei
    elif gross_income >= 60300:
        ei = 60300 * 0.0158
        return ei


# read data from the txt
def readAndPop():
    with open('employee_data.txt', 'r') as f:
        d = f.readlines()

        for line in d[1:]:
            record = line.split('\t')
            emId = record[0]
            firstName = record[1]
            lastName = record[2]
            email = record[3]
            password = record[4]
            grossIncome = record[5]

            # populate the data from txt to the employee table, without  fed_tax, on_tax,cpp,ei,net_income
            try:
                creds = readDBConfig()
                conn = mysql.connector.MySQLConnection(**creds)
                cursor = conn.cursor()

                query = """INSERT INTO employees
                (id, Fname, Lname, email, password, gross_income)
                VALUES (%s,%s,%s,%s,%s,%s)"""

                inputValue = (emId, firstName, lastName, email, password, grossIncome)

                cursor.execute(query, inputValue)
                conn.commit()

            except Exception as e:
                print(e)

            finally:
                cursor.close()
                conn.close()


# updating the  value on fed_tax,on_tax,cpp,ei
def update_employee_record(fedTax, onTax, cpp, ei, netIncome, id):
    try:
        creds = readDBConfig()
        conn = mysql.connector.MySQLConnection(**creds)
        cursor = conn.cursor()

        query = """UPDATE employees SET 
        fed_tax = %s, on_tax = %s, cpp = %s,  ei = %s, net_income = %s WHERE id = %s """

        inputValue = (fedTax, onTax, cpp, ei, netIncome, id)

        cursor.execute(query, inputValue)
        conn.commit()

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


# get the value from table and pass to function above
def getGrossIncome():
    try:
        creds = readDBConfig()
        conn = mysql.connector.MySQLConnection(**creds)
        cursor = conn.cursor()

        query = """SELECT id, gross_income FROM employees  """

        cursor.execute(query)
        result = cursor.fetchall()

        # append id and income from tuple to list
        returnList = []

        for row in result:
            returnList.append(row)

        # pass the income to the function
        for employee in returnList:
            id = employee[0]
            grossIncome = employee[1]

            fedTax = calc_fed_tax(grossIncome)
            onTax = calc_on_tax(grossIncome)
            cpp = calc_cpp(grossIncome)
            ei = calc_ei(grossIncome)
            netIncome = grossIncome - fedTax - onTax - cpp - ei

            update_employee_record(fedTax, onTax, cpp, ei, netIncome, id)

        cursor.close()
        conn.close()
        return returnList

    except Exception as e:
        print(e)


getGrossIncome()
