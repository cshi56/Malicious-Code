from django.db import models

# Create your models here.
class Submission(models.Model):
    name = models.CharField(max_length=200)
    run_date = models.DateTimeField('date submitted')

    def __str__(self):
        return self.name

    def sub_risk(self):
        for x in self.output_set:
            if output__risk is 'Bad':
                return 'Bad'

class Output(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    risk = models.CharField(max_length=200)
    reason = models.CharField(max_length=200)

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

    def __str__(self):
        return self.type
