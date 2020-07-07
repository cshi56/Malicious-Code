from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from .models import Submission, Output, FileSubmissionForm, FileSubmission
from .forms import UploadFileForm
from .analysis.yaraTests import yaraScan
from django.contrib import messages


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
    form = FileSubmissionForm()
    return render(request, 'test/home.html', {'form': form})

def save_form(request):
    form = FileSubmissionForm(request.POST, request.FILES)
    entry = form.save()
    yaraMatches = yaraScan(str(entry.file))
    for match in yaraMatches:
        print(match)
    return redirect('/test/' + str(entry.id) + '/results')

def send_email(request, submission_id):
    send_mail(
    'Potential MALWARE Alert from a Duke User',
    'The Malicious Code Analysis tool at http://127.0.0.1:8000/test/home has flagged a test by a user who suspects malware. Log into the admin view at http://127.0.0.1:8000/admin to view the details.',
    'FROM_USER@duke.edu',
    ['TO_USER@duke.edu'],
    fail_silently=False,
    )
    messages.success(request, 'OIT has been notified and will take a look. Thanks!', fail_silently=True)
    strin = "/test/"+ submission_id.__str__() + "/results"
    return HttpResponseRedirect(strin)
