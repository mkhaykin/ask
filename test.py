from qa.models import Question, Answer

from django.contrib.auth.models import User
from django.db.models import Max
from django.utils import timezone

import time

res = Question.objects.all().aggregate(Max('rating'))
max_rating = res['rating__max'] or 0
user, _ = User.objects.get_or_create(
    username='x',
    defaults={'password': 'y', 'last_login': timezone.now()})

for i in range(2):
    question = Question.objects.create(
        title='question ' + str(i),
        text='text ' + str(i),
        author=user,
        rating=max_rating + i
    )
