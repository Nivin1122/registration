from django.urls import path
from app1 import views
urlpatterns = [



path('login/',views.LoginPage,name='login'),
path('home/',views.HomePage,name='home'),
path('',views.signupPage,name='signup'),
path('logout/',views.LogoutPage,name='logout'),
# //////////////////////
path('adminlogin/',views.loginAdmin, name='admlogin'),
path('adminpage/',views.userData,name='adminpage'),
path('add/',views.addEmp,name='add'),
path('edit',views.editEmp, name = 'edit'),
path('update/<str:id>', views.updatEmp, name='update'),
path('delete/<str:id>', views.delEmp, name='delete'),
path('admlogout/',views.signOut,name='admlogout'),
]