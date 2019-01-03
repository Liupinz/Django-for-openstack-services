from django.conf.urls import url
from OM import views

urlpatterns = [
    url(r'^login$', views.login),
    url(r'^login_check$', views.login_check),
    url(r'^openstacks$', views.openstackStatus),
    url(r'^list_status$', views.list_status),
    url(r'^cloudip$', views.cloudip),
    url(r'^clouddashboard$', views.clouddashboard),
    url(r'^contact$', views.contact),
    url(r'^contact_handle$', views.contact_handle),

]