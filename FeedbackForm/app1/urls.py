from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view()),
    path("formmaker", views.FormMake.as_view()),
    path("testformmaker", views.add),
    path("formtokenview", views.formtokenview),
    path("emailtokenview", views.emailtokenview),
    path('formcheck',views.formcheck),
    path('formpreview',views.formpreview),
    path('showmail',views.showmail),
    path('feedbackform/<slug:uidb64>/<slug:token>/',views.feedbackform,name="feedbackform")

]
