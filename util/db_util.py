import pyodbc # type: ignore

class DBConnection:
    def __init__(self):
        self.conn=pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost,1433;'
            'DATABASE=appdb ;'
            'UID=sa;'
            'PWD=examlyMssql@123;'
        )
        self.cursor=self.conn.cursor()
        self.initialize_schema()

    def initialize_schema(self):
        create_table_query='''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Patients' AND xtype='U')
        CREATE TABLE Patients(
            patient_id INT IDENTITY(1,1) PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            gender VARCHAR(10),
            symptoms VARCHAR(255),
            contact VARCHAR(100)
        )
        '''
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def get_cursor(self):
        return self.cursor
    
    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()