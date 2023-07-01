from django.urls import path
from . import views

urlpatterns = [
    path('client', views.ClientView.as_view({'post': 'create'})),
    path('client/<int:pk>', views.ClientView.as_view({'get': 'retrieve',
                                                      'put': 'update',
                                                      'delete': 'destroy'})),
    path('dispatch', views.DispatchView.as_view({'post': 'create'})),
    path('dispatch/<int:pk>', views.DispatchView.as_view({'get': 'retrieve',
                                                          'put': 'update',
                                                          'delete': 'destroy'
                                                          })),
    path('dispatch/<int:pk>/stats/', views.DispatchStatsView.as_view(), name='dispatch-stats'),
    path('message/<int:dispatch_id>', views.MessageView.as_view()),

]
