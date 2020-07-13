from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from .models import Submission, Output, FileSubmissionForm, FileSubmission
from .forms import UploadFileForm
from .analysis.yaraTests import maldocsScan
import hashlib
from django.contrib import messages
import json


def index(request):
    return HttpResponse("Hello, world. You're at the test index.")

def results(request, submission_id):
    obj = FileSubmission.objects.get(id=submission_id)
    sha256_hash = obj.sha256_hash
    name = str(obj.file)
    yaraResult = json.loads(obj.yaraResult)
    if len(yaraResult) == 0:
        yaraOut = 'VERDICT: File is Safe'
    else:
        yaraOut = 'VERDICT: File is Dangerous'
    context = {'hash': sha256_hash, 'name': name, 'number': submission_id, 'yaraOut': yaraOut}
    return render(request, 'test/results.html', context)

def details(request, submission_id):
    submission = FileSubmission.objects.get(id=submission_id)
    results = json.loads(submission.yaraResult)
    context = {'results': results, 'number': submission_id}
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
    sha256_hash = hashlib.sha256()
    a_file = open(filename, "rb")
    content = a_file.read()
    sha256_hash.update(content)
    entry.sha256_hash = sha256_hash.hexdigest()
    entry.save()

    #running yaraTests
    print("Running Yara tests for " + filename)
    yaraMatches = maldocsScan(filename)
    print(yaraMatches)
    entry.yaraResult = json.dumps(yaraMatches)
    entry.save()


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
