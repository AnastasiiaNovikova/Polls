from django.db import models
from django.contrib.auth.models import User


class Person(User):
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Poll(models.Model):
    poll_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    poll_user_count = models.IntegerField(default=0)
    user = models.ManyToManyField(Person, blank=True)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.poll_name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question_user_count = models.IntegerField(default=0)
    user = models.ForeignKey(Person, related_name='question_user', null=True, blank=True)

    def __str__(self):
        return self.question_text

    def save(self, *args, **kwargs):
        all_choices = Choice.objects.filter(question_id=self.pk)
        if all_choices.count() >= 2:
            super(Question, self).save(*args, **kwargs)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    choice_user_count = models.IntegerField(default=0)
    rate = models.FloatField(default=0)
    user = models.ForeignKey(Person, related_name='user', null=True, blank=True)

    def __str__(self):
        return self.choice_text

    def save(self, *args, **kwargs):
        super(Choice, self).save(*args, **kwargs)
        question = self.question
        all_choices = Choice.objects.filter(question_id=question.id)
        if self == all_choices.last():
            rate = 100
            for choice in all_choices:
                if choice != self:
                    rate -= choice.rate
            self.rate = rate
        else:
            try:
                self.rate = self.choice_user_count / question.question_user_count * 100
            except ZeroDivisionError:
                self.rate = 0
        super(Choice, self).save(*args, **kwargs)

