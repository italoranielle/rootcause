# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 12:56:09 2020

@author: italo Ranielle
@mail: italoranielle@gmail.com
"""

from django.urls import path ,re_path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    #path('analysis/<int:team>',views.AnalysisList.as_view(),name='analysis_list'),
    path('analysis/',views.AnalysisList.as_view(),name='analysis_list'),
    path('analysis/new/',views.AnalysisCreateView.as_view(),name='analysis_new'),
    path('analysis/detail/<int:pk>',views.AnalysisDetailView.as_view(),name='analysis_detail'),
    path('analysis/edit/<int:pk>',views.AnalysisUpdate.as_view(),name='analysis_edit'),
    path('analysis/delete/<int:pk>',views.AnalysisDeleteView.as_view(),name='analysis_delete'),

    path('5w2h/new/<int:analysis>', views.W5h2CreateView.as_view(), name = 'w5h2_new'),
    path('5w2h/detail/<int:pk>', views.W5h2DetailView.as_view(), name = 'w5h2_detail'),
    path('5w2h/edit/<int:pk>', views.W5h2EditView.as_view(), name = 'w5h2_edit'),

    path('ishikawa/view/<int:analysis>', views.ishikawaView, name = 'ishikawa_view'),
    path('ishikawa/itens/<int:analysis>', views.IshikawaItems.as_view(), name = 'ishikawa_itens'),
    path('ishikawa/new/<int:analysis>', views.IshikawaNew.as_view(), name = 'ishikawa_new'),
    path('ishikawa/generatewhays/<int:analysis>',views.ishikawaGenereteWhays, name = 'ishikawa_generate_pqs5'),

    path('whays/list/<int:analysis>',views.WhaysListView.as_view(), name = 'pqs5_list'),
    path('whays/table/<int:analysis>',views.WhaysTableView.as_view(), name = 'pqs5_table'),
    path('whays/new/<int:analysis>',views.whaysNew.as_view(), name = 'pqs5_new'),
    path('whays/edit/<int:pk>',views.whaysEditView.as_view(), name = 'pqs5_edit'),
    path('whays/delete/<int:pk>',views.whaysDeleteView.as_view(), name = 'pqs5_delete'),

    path('action/kamban/<int:analysis>',views.Kamban, name='kamban'),
    path('action/list/<int:analysis>',views.ActionListView.as_view(), name='action_list'),
    path('action/task/new/<int:analysis>',views.ActionNew.as_view(),name='action_new'),
    path('action/task/edit/<int:pk>',views.ActionEditView.as_view(),name='action_edit'),
    path('action/task/delete/<int:pk>',views.ActionDeleteView.as_view(),name='action_delete'),

    path('api/tasks/<int:analysis>',views.apiActions, name='api_tasks'),
    path('api/tasks/changeBucket/',views.apiActionChangeBucket, name='api_changeBucket'),
    
    path('shift/list/<int:team>', views.ShiftList.as_view(), name = 'shift_list'),
    path('shift/new/', views.ShiftCreate.as_view(), name = 'shift_new'),
    path('shift/delete/<int:pk>', views.ShiftDelete.as_view(), name = 'shift_delete'),
    
    path('area/list/<int:team>', views.AreaList.as_view(), name = 'area_list'),
    path('area/new/', views.CreateArea.as_view(), name = 'area_new'),
    path('area/delete/<int:pk>', views.AreaDelete.as_view(), name = 'area_delete'),
    
    path('aqf/ishikawa_edit/<int:pk>', views.IshikawaEditView.as_view(), name = 'ishikawa_edit'),
]