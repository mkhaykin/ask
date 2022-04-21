from django import forms
from django.contrib.auth.models import User

from models import Answer, Question


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    # def __init__(self, *args, **kwargs):
    #     super(AskForm, self).__init__(*args, **kwargs)

    # def clean_message(self):
    #     message = self.cleaned_data['message']
    #     if not is_ethic(message):
    #         raise forms.ValidationError(u'error message', code=12)
    #     return message + \
    #     "\nThank you for your attention."

    # not used
    # def get_url(self):
    #     return ""

    def save(self):
        # answer = Question(**self.cleaned_data)
        ask = Question()
        cd = self.cleaned_data
        ask.title = cd['title']
        ask.text = cd['text']
        ask.author = self._user     # User.objects.get(pk=1)

        ask.save()
        return ask


class AnswerForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    # TODO: drop later
    question = forms.IntegerField()

    def save(self, question):
        answer = Answer()
        cd = self.cleaned_data

        answer.question = question
        answer.title = cd['title']
        answer.text = cd['text']
        answer.author = self._user  # User.objects.get(pk=1)
        print(self._user, '/', answer.author)

        answer.save()
        return answer


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
