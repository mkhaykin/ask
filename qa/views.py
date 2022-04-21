from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, \
    login as django_login, \
    logout as django_logout
from django.forms.forms import NON_FIELD_ERRORS
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime, timedelta

from models import *
from forms import *


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def index(request):  # , *args, **kwargs):
    # paginator
    try:
        qs = Question.objects.new()
    except Question.DoesNotExist:
        raise Http404

    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    paginator = Paginator(qs, limit)

    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'index.html',
                  {"paginator": paginator,
                   "page": page})


def question(request, id):
    try:
        q = Question.objects.get(id=id)
        # a = Answer.objects.get(question=id)
        a = q.answer_set.all()
        print(a)
        if request.method == "POST":
            form = AnswerForm(request.POST)
            if form.is_valid():
                form._user = request.user
                form.save(q)
                form = AnswerForm(initial={'question': q.id})
        else:
            form = AnswerForm(initial={'question': q.id})
    except Question.DoesNotExist:
        raise Http404
    return render(request, 'question.html', {
        'id': id,
        'question': q,
        'answers': a,
        'form': form
    })


def ask(request):
    # HttpResponseRedirect('/ /question/...123.../')
    # return HttpResponse('ask')
    if request.method == "POST":
        form = AskForm(request.POST)
        form._user = request.user
        if form.is_valid():
            post = form.save()
            url = post.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask.html', {
        'form': form
    })


def popular(request):
    try:
        qs = Question.objects.popular()
    except Question.DoesNotExist:
        raise Http404

    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    paginator = Paginator(qs, limit)

    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'popular.html',
                  {"paginator": paginator,
                   "page": page})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            try:
                # u = User.objects.get(username=username)
                u = User.objects.filter(username=username)
            except User.DoesNotExist, e:
                u = None
            # if User.objects.filter(username=username).exists():
            if u:
                form.errors[NON_FIELD_ERRORS] = form.error_class(['account already exists.'])
            else:
                user = User.objects.create_user(username, email, password)
                user.save()
                # login!
                user = authenticate(username=username, password=password)
                django_login(request, user)
                # request.user.sessionid = request.COOKIES.get('sessionid', None)
                response = HttpResponseRedirect("/")
                response.set_cookie("sessionid",
                                    request.COOKIES.get('sessionid', None),
                                    httponly=True,
                                    expires=datetime.now() + timedelta(days=5))
                return response
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {
        'form': form
    })


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    # request.user.sessionid = request.COOKIES.get('sessionid', None)
                    response = HttpResponseRedirect("/")
                    response.set_cookie("sessionid",
                                        request.COOKIES.get('sessionid', None),
                                        httponly=True,
                                        expires=datetime.now() + timedelta(days=5))

                    # Redirect to a success page.
                    return response
                    # response = HttpResponseRedirect("/")
                    # response.set_cookie('sessionid', sessid,
                    #                 domain='.site.com', httponly=True,
                    #                 expires=datetime.now() + timedelta(days=5)
                    #                 )
                    # return response
                else:
                    # Return a 'disabled account' error message
                    form.errors[NON_FIELD_ERRORS] = form.error_class(['your account is disabled.'])
            else:
                # Return an 'invalid login' error message.
                form.errors[NON_FIELD_ERRORS] = form.error_class(['your login or password is invalid.'])
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form
    })


def logout(request):
    # FIXME ... only post request ;)
    django_logout(request)
    # TODO: clear user.sessionid ?
    return HttpResponseRedirect("/")
