from django.urls import path
from . import views

urlpatterns = [
    #path('user',views.test),
    #path('user/<int:id>',views.test_details) 
    #for class base api url
    path('user/',views.testclass.as_view()),
    path('user/<int:id>',views.testclassdetails.as_view()),


    #generic api urls
    path('generic/',views.testgeneric.as_view()),
    path('generic/<int:id>/',views.testgeneric.as_view())

]