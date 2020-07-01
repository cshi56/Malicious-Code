from django.contrib import admin
from .models import Submission, FileSubmission

# Register your models here.
# Password is maliciouscode
# Username is admin
admin.site.register(Submission)
admin.site.register(FileSubmission)
