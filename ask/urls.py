"""ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView

from qa.views import index, question, popular, ask, signup, login, logout
from qa.views import test


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    # url(r'^(?P<slug>[\w-]+)/$', page, name='index'),    # for http://127.0.0.1:8000/2/
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^signup/', signup, name='signup'),
    url(r'^question/([0-9]+)/', question, name='question'),
    url(r'^ask/', ask, name='ask'),
    url(r'^popular/', popular, name='popular'),
    url(r'^new/', test, name='new'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
]
