from django.db import models

# Create your models here.

class Question(models.Model):
    question = models.CharField("Survey Question", max_length=256)
    integer_question = models.IntegerField('Set to 1 if True', default = 0)
    question_index = models.IntegerField('Orders the Questions', default=-1)

    def __unicode__(self):
        return self.question

    class Meta:
        ordering = ["question_index"]
        unique_together = [["question", "question_index"]]

class Answer(models.Model):
    quesiton = models.ForeignKey(Question)
    votes = models.IntegerField(default=0)
    answer_text = models.CharField('Answer text',default='', max_length=256)




