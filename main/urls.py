from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
	url(r'^results/$', views.results, name = 'information'),
    url(r'^begin/$', views.begin, name = 'monitoring'),
    # url(r'^(?P<order_id>[0-9]+)/$', views.order, name='order'),
    # url(r'^login/$', views.login, name = 'login'),
    # url(r'^logout/$', views.logout, name = 'logout'),
    # url(r'^loginned/$', views.logginned, name = 'loginok'),
    # url(r'^order/(?P<edit_order_id>[0-9]+)/$', views.edit, name='edit'),
    # url(r'^editprofile/(?P<edit_profile_id>[0-9]+)/$', views.editprofile,name='editprofile'),
    # url(r'^profile/(?P<views_profile_id>[0-9]+)/$', views.profile,name='profile')
]