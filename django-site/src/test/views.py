from django.shortcuts import render
from django.http import HttpResponse
from .models import Submission, Output
from .forms import UploadFileForm


def index(request):
    return HttpResponse("Hello, world. You're at the test index.")

def results(request, submission_id):
    number = submission_id
    submission_results_list = Output.objects.filter(submission__id=submission_id)
    context = {'latest_question_list': submission_results_list, 'number': submission_id}
    return render(request, 'test/results.html', context)

def details(request, submission_id):
    submission_results_list = Output.objects.filter(submission__id=submission_id)
    context = {'latest_question_list': submission_results_list, 'number': submission_id}
    return render(request, 'test/details.html', context)

def home(request):
    form = UploadFileForm()
    return render(request, 'test/home.html', {'form': form})
