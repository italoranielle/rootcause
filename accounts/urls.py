# -*- coding: utf-8 -*-



from django.urls import path
from . import views



urlpatterns = [
    
     path('signup/', views.SignUpView.as_view(), name = 'signup'),
     path('loginWin/', views.win_login, name = 'loginwin'),
     path('callback/', views.callback, name = 'callback'),
     path('profile/', views.UserView, name = 'user_profile'),
     path('update/', views.Update, name = 'user_update'),
     path('reset/', views.PasswordReset, name = 'reset_pw'),
     path('list/', views.Userlist, name = 'list_user'),
     path('userupdate/<int:pk>', views.UpdateAdmin.as_view(), name = 'user_update_adm'),
     
     path('team/myteams',views.TeamView, name='myteams'),
     path('team/new',views.CreateTeam.as_view(), name='new_team'),
     path('team/function/new',views.CreateFunction.as_view(), name='new_function'),
     path('team/function/delete/<int:pk>',views.FunctionDelete.as_view(), name='delete_function'),
     path('team/function/update/<int:pk>',views.UpdateFunction.as_view(), name='update_function'),
     path('team/menber/new',views.addMember, name='add_member'),
     path('team/menber/remove/<int:pk>',views.RemoveMember.as_view(), name='remove_member'),
     path('team/menber/update/<int:pk>',views.UpdateMember.as_view(), name='update_member'),

]
