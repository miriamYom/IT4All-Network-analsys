import pymysql

# Create a connection object

dbServerName = "sql6.freesqldatabase.com"
dbUser = "sql6635076"
dbPassword = "IVFgIa9ywj"
dbName = "sql6635076"
charSet = "utf8mb4"
cursorType = pymysql.cursors.DictCursor

connectionObject = pymysql.connect(
    host=dbServerName,
    user=dbUser,
    password=dbPassword,
    db=dbName,
    charset=charSet,
    cursorclass=cursorType
)

try:
    # Create a cursor object
    cursorObject = connectionObject.cursor()

    # SQL query string
    sqlQuery1 = '''CREATE TABLE Device_temp(
    ID INT NOT NULL AUTO_INCREMENT,
    NetworkID INT NOT NULL,
    IP VARCHAR(100),
    Mac VARCHAR(100),
    Name VARCHAR(20) DEFAULT "Device",
    Vendor VARCHAR(20),
    Info NVARCHAR(100) NULL,
    CONSTRAINT PK_Device_temp PRIMARY KEY (ID)
);'''

    # Execute the INSERT statement
    cursorObject.execute(sqlQuery1)

    # Commit the transaction to make the changes permanent
    connectionObject.commit()

# except Exception as e:
#     print("Exception occurred: {}".format(e))

finally:
    connectionObject.close()
