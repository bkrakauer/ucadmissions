from django.conf.urls import url

from ucadmissions import views

#do we need to add an entry for index, rather than just home?

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^results$', views.results, name='results'),
]