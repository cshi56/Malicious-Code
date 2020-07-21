from django.shortcuts import redirect

# Create your views here.
def home_view(request, *args, **kwargs):
    my_context = {}
    return redirect('/test/home')