from django.shortcuts import render_to_response

def index(request):
    return render_to_response('signupStrict.html')

def homepage(request):
	return render_to_response('homepageStrict.html')
	
def profile(request):
	return render_to_response('profileStrict.html')