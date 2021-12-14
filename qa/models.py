from __future__ import unicode_literals

from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    rating = models.IntegerField(default=0)
    autor = models.OneToOneField(User)  # , on_delete=models.DO_NOTHING()
    likes = models.ManyToManyField(User, related_name='question_like_user')  # , on_delete=models.DO_NOTHING()

    def __unicode__(self):
        return self.title

    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    question = models.ForeignKey(null=False, on_delete=models.CASCADE())
    autor = models.OneToOneField(User)  # , on_delete=models.DO_NOTHING()
