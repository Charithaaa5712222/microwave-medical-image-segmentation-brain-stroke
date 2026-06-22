from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('UserLogin.html', views.UserLogin, name="UserLogin"), 
	       path('Register.html', views.Register, name="Register"),
	       path('Signup', views.Signup, name="Signup"),
	       path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),
	       path('runOSTU.html', views.runOSTU, name="runOSTU"), 
	       path('runOSTUAction', views.runOSTUAction, name="runOSTUAction"),
	      path('runDBIM.html', views.runDBIM, name="runDBIM"), 
	       path('runDBIMAction', views.runDBIMAction, name="runDBIMAction"),
	           
]
