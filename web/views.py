from django.shortcuts import render_to_response

def index(request):
    return render_to_response('signupStrict.html')

def homepage(request):
	return render_to_response('homepageStrict.html')
	
def profile(request):
	return render_to_response('profileStrict.html')
	
def importFacebook(request):
	return render_to_response('importFacebook.html')

def importLinkedIn(request):
	return render_to_response('importLinkedIn.html')

def importTeamWorks(request):
	return render_to_response('importTeamWorks.html')