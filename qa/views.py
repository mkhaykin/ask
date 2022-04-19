from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        a = Answer.objects.all()
        if request.method == "POST":
            form = AnswerForm(request.POST)
            if form.is_valid():
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
