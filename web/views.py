from django.shortcuts import render_to_response
import MySQLdb

db= MySQLdb.connect('localhost','root','root','hunchWorks', 8889, '/Applications/MAMP/tmp/mysql/mysql.sock')
cursor = db.cursor()
cursor.execute("SELECT * from Users where userId = 1")
results = cursor.fetchall()
for row in results:
	location = row[0]
	email = row[1]
	firstName = row[2]
	lastName = row[3]

def index(request):
    return render_to_response('signupStrict.html')

def homepage(request):
	return render_to_response('homepageStrict.html', { 'firstName': firstName, 'location': location })
	
def profile(request):
	return render_to_response('profileStrict.html')
	
def importFacebook(request):
	return render_to_response('importFacebook.html')

def importLinkedIn(request):
	return render_to_response('importLinkedIn.html')

def importTeamWorks(request):
	return render_to_response('importTeamWorks.html')