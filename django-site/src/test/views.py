from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from .models import Submission, Output, FileSubmissionForm, FileSubmission
from .forms import UploadFileForm
from .analysis.yaraTests import yaraScan
import hashlib
from django.contrib import messages


def index(request):
    return HttpResponse("Hello, world. You're at the test index.")

def results(request, submission_id):
    obj = FileSubmission.objects.get(id=submission_id)
    md5_hash = obj.md5_hash
    name = str(obj.file)
    context = {'hash': md5_hash, 'name': name}
    return render(request, 'test/results.html', context)

def details(request, submission_id):
    submission_results_list = Output.objects.filter(submission__id=submission_id)
    context = {'latest_question_list': submission_results_list, 'number': submission_id}
    return render(request, 'test/details.html', context)

def home(request):
    form = FileSubmissionForm()
    return render(request, 'test/home.html', {'form': form})

def save_form(request):
    #file is saved
    form = FileSubmissionForm(request.POST, request.FILES)
    entry = form.save()
    filename = str(entry.file)

    #hashing file
    md5_hash = hashlib.md5()
    a_file = open(filename, "rb")
    content = a_file.read()
    md5_hash.update(content)
    entry.md5_hash = md5_hash.hexdigest()
    entry.save()

    #running yaraTests
    yaraMatches = yaraScan(filename)
    for match in yaraMatches:
        print(match)

    #redirects to results page
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
