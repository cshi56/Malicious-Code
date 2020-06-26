from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs):
    my_context = {}
    return render(request, 'home.html', my_context)