from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from .models import Submission, Output, FileSubmissionForm, FileSubmission
from .forms import UploadFileForm
from .analysis.yaraTests import maldocsScan, emlScan
import hashlib
from django.contrib import messages
import json
import magic
from .analysis.virusTotalTest import VTScan


def index(request):
    return redirect('/test/home')

def results(request, submission_id):
    obj = FileSubmission.objects.get(id=submission_id)
    dangerous = False
    vtdetections = obj.VTDetections
    sha256_hash = obj.sha256_hash
    name = str(obj.file)
    yaraResult = json.loads(obj.yaraResult)
    if len(yaraResult) == 0 and vtdetections == 0:
        yaraOut = 'VERDICT: FILE IS SAFE'
    elif vtdetections > 0:
        dangerous = True
        yaraOut = 'VERDICT: FILE IS DANGEROUS'
    elif vtdetections == -1:
        yaraOut = 'File is taking longer than expected to analyze. Please come back to this page or upload the same file again in a few minutes to see results.'
    else:
        yaraOut = 'VERDICT: Inconclusive'
    context = {'hash': sha256_hash, 'name': name, 'number': submission_id, 'yaraOut': yaraOut, 'dangerous': dangerous}
    return render(request, 'test/results.html', context)

def details(request, submission_id):
    submission = FileSubmission.objects.get(id=submission_id)
    results = json.loads(submission.yaraResult)
    count = submission.VTDetections
    context = {'results': results, 'number': submission_id, 'VTCount': count, 'vtlink': submission.VTUrl}
    return render(request, 'test/details.html', context)

def home(request):
    form = FileSubmissionForm()
    return render(request, 'test/home.html', {'form': form})

def save_form(request):
    #file is saved
    form = FileSubmissionForm(request.POST, request.FILES)
    entry = form.save()
    return render(request, 'test/loading.html', {'submission_id': entry.id})

def loading(request, submission_id):
    entry = FileSubmission.objects.get(id=submission_id)
    filename = str(entry.file)

    #hashing file
    hash = hashlib.sha256()
    a_file = open(filename, "rb")
    content = a_file.read()
    hash.update(content)
    entry.sha256_hash = hash.hexdigest()

    #checking if file has already been scanned
    if FileSubmission.objects.filter(sha256_hash=hash.hexdigest()).exists():
        print("Found to exist")
        entry.delete()
        entry = FileSubmission.objects.get(sha256_hash=hash.hexdigest())
        VTOut = VTScan('', hash.hexdigest())
        entry.VTUrl = VTOut[1]
        entry.VTDetections = VTOut[0]
        entry.save()
        return redirect('/test/' + str(entry.id) + '/results')

    #determining file type
    filetype = 'unknown'
    officeExtensions = ['.docx', '.doc', '.docm', '.dot', '.dotm', '.dotx', '.docb', '.xls', '.xlt', '.xlm',
                        '.xlsx', '.xlsm', '.xltx', '.xltm', '.xlsb', '.xla', '.xlam', '.xll', '.xlw',
                        '.ppt', '.pot', '.pps', '.pptx', '.pptm', '.potx', '.potm', '.ppam', '.ppsx',
                        '.ppsm', '.sldx', '.sldm']
    if any(x in filename for x in officeExtensions):
        magicType = magic.from_file(filename)
        if 'Microsoft' not in magicType:
            filetype = 'disguised'
        else:
            filetype = 'msdoc'
    if '.eml' in filename:
        filetype = 'eml'
    if '.pdf' in filename:
        magicType = magic.from_file(filename)
        if 'PDF' not in magicType:
            filetype = 'disguised'
        else:
            filetype = 'pdf'

    #running yaraTests
    print("Running Yara tests for " + filename)
    if filetype is 'msdoc' or filetype is 'pdf':
        yaraMatches = maldocsScan(filename)
    if filetype is 'eml':
        yaraMatches = emlScan(filename)
    if filetype is 'unknown':
        yaraMatches = ['Unsupported filetype. Yara scans are only available for eml, pdf, or Microsoft Office files.']
    if filetype is 'disguised':
        yaraMatches = ['Disguised filetype']
    print(yaraMatches)
    entry.yaraResult = json.dumps(yaraMatches)
    entry.save()

    #running virus total tests
    print("Running VirusTotal Tests")
    VTOut = VTScan(filename, entry.sha256_hash)
    entry.VTUrl = VTOut[1]
    entry.VTDetections = VTOut[0]
    entry.save()
    print("Detections: " + str(VTOut[0]))

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
