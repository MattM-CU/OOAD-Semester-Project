# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi

import sqlite3 as dbInterface


# CREDIT: Dave Wescott (structure of executeQuery/NonQuery)
class Database(object):

    def __init__(self, dbName):

        # A connection to the database
        self.dbConnection = dbInterface.connect(dbName)

        # A cursor from the database connection
        self.cursor = self.dbConnection.cursor()

    def createDatabase(self):

        # TODO - sql string for each table
        sql = ""
        self.executeNonQuery(sql, variables=[])

    def executeNonQuery(self, sql, variables):
        """Private method.  If a database connection and cursor are available,
           execute the requested SQL statement.

           Input:  SQL statement <str>
                   SQL variables [value <str>/<int>/<float>]
           Output: None
        """
        #  If the database connection and cursor are valid
        if self.dbConnection is not None and self.cursor is not None:
            #  Try executing SQL
            try:
                self.cursor.execute(sql, variables)
                self.dbConnection.commit()
            # If any errors occur, return the no info dictionary
            except Exception as error:
                raise DatabaseError("Failed to execute SQL statement.  " + str(error))

    def executeQuery(self, sql, variables):
        """Private method.  If a database connection and cursor are available,
           execute the requested SQL query statement.

           Input:  SQL query statement <str>
                   SQL variables [value <str>/<int>/<float>]
           Output: rows of data [ { column <str> : value <str> }]
        """

        #  A dictionary; column index => column name (0 => Column_Name_0)
        columnNames = {}

        #  The results of the SQL query.  A 1D list of dictionaries.  The keys in
        #  the dictionaries are the column names and the value is the column value.
        resultsList = []

        if self.dbConnection is not None and self.cursor is not None:
            #  Try executing SQL
            try:
                self.cursor.execute(sql, variables)
            # If any errors occur, return the no info dictionary
            except Exception as error:
                raise DatabaseError("Failed to execute SQL statement.  " + str(error))

            # Get the first row from the query
            row = self.cursor.fetchone()

            #  Get the column names and arrange them into a dictionary
            for index, column in enumerate(self.cursor.description):
                columnNames[index] = column[0]#.lower()


            #  While there are more rows from the query
            while row is not None:
                #  A dictionary of values from the row.  The key is the column name and the value
                #  is the data from the row/column.
                values = {}

                #  Go through each value in the row
                for index, value in enumerate(row):
                    #  Add the value into the dictionary with the correct column name
                    values[columnNames[index]] = str(value)

                # Add the dictionary to the results list
                resultsList.append(values)

                #  Get the next row
                row = self.cursor.fetchone()

        return resultsList

    def closeDatabase(self):
        """Close the database connection."""
        #  If the cursor is valid, close it
        if (self.cursor is not None):
            self.cursor.close()

        # If the DB connection is valid, close it
        if (self.dbConnection is not None):
            self.dbConnection.close()

    def wipeDatabase(self):
        # TODO - change be more abstract: iterate over all tables and drop each
        pass


class DatabaseError(Exception):
    pass


