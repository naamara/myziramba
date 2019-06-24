from django.shortcuts import render


def about(request):
	# Function for calling the about us page 
	
	return render(request, "about.html", {})
