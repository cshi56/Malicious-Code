from django.urls import path

from . import views

urlpatterns = [
    # hello world
    path('', views.index, name='index'),
    # see results
    path('<int:submission_id>/results/', views.results, name='results'),
    # see details
    path('<int:submission_id>/details/', views.details, name='details'),

    path('home', views.home, name='home'),
]