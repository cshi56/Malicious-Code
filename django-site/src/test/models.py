from django.db import models
from django.forms import ModelForm


class Submission(models.Model):
    name = models.CharField(max_length=200)
    run_date = models.DateTimeField('date submitted')

    def __str__(self):
        return self.name

    def sub_risk(self):
        for x in self.output_set:
            if output__risk is 'Bad':
                return 'Bad'

class FileSubmission(models.Model):
    #this is the model where file submissions are stored
    name = models.CharField(max_length=200)
    run_date = models.DateTimeField('date submitted', auto_now_add=True)
    file = models.FileField(upload_to='uploads/')
    md5_hash = models.CharField(max_length=32, default=None, blank=True, null=True)
    yaraResult = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name

class Output(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    risk = models.CharField(max_length=200)
    reason = models.CharField(max_length=200)

    def __str__(self):
        return self.type

class FileSubmissionForm(ModelForm):
    class Meta:
        model = FileSubmission
        fields = ['file', 'name']

class OutputForm(ModelForm):
    class Meta:
        model = Output
        fields = ['submission', 'type', 'risk', 'reason']

#COMMENTED OUT BELOW IS ENUMERATED IMPLEMENTATION OF RISK FIELD
    #class Risk(models.TextChoices):
    #    BAD = 'Bad'
    #    CLEAR = 'Clear'
    #    SUSPICIOUS = 'Suspicious'
#
#    risk = models.CharField(
#        max_length=15,
#        choices=Risk.choices,
#        default=Risk.CLEAR,
#    )
