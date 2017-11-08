from django.shortcuts import render, HttpResponse

#home of the site
def home(request):
    return render(request, 'homepage/home.html')

def home2(request):
    return render(request, 'homepage/home-2.html')

def home3(request):
    return render(request, 'homepage/home-3.html')
