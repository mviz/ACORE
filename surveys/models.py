from django.db import models

# Create your models here.

class SurveyQuestion(models.Model):
    question = models.CharField("Survey Question", max_length=256)
    integer_question = models.IntegerField('0 if yes, else no', default = 0)
    question_index = models.IntegerField('For order', default=-1)

    def __unicode__(self):
        return self.question

    class Meta:
        ordering = ["question_index"]
        unique_together = [["question", "question_index"]]

class SurveyAnswer(models.Model):
    quesiton = models.ForeignKey(SurveyQuestion)
    votes = models.IntegerField(default=0)
    answer_text = models.CharField('Answer text',default='', max_length=256)




