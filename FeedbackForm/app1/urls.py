from django.urls import path
from . import views

urlpatterns = [
    path("", views.mylogin, name='login'),
    path('logout', views.mylogout, name='logout'),
    path('clear_tempdata', views.clear_tempdata, name='clear_tempdata'),
    path('cancel', views.cancel, name='cancel'),
    path('stats', views.stats, name='stats'),
    path('formdata', views.formdata, name='formdata'),
    path("home", views.Home.as_view()),
    path("formmaker", views.FormMake.as_view()),
    path("formclone", views.formclone),
    path("testformmaker", views.add),
    path("formtokenview", views.formtokenview),
    path("emailtokenview", views.emailtokenview),
    path('formcheck', views.formcheck),
    path('formpreview', views.formpreview),
    path('showmail', views.showmail),
    path('feedbackform/<slug:uidb64>/<slug:token>/', views.feedbackform, name="feedbackform"),
    path('del_fields/<int:pk>/', views.del_fields, name='del_fields')
]
