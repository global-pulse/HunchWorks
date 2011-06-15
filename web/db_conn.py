import MySQLdb

#This is for connecting to a MAMP database
db= MySQLdb.connect('localhost','root','root','hunchWorks', 8889,
					'/Applications/MAMP/tmp/mysql/mysql.sock')
cursor = db.cursor()
cursor.execute("SELECT * from Users where userId = 1")
results = cursor.fetchall()
for row in results:
	location = row[0]
	email = row[1]
	firstName = row[2]
	lastName = row[3]