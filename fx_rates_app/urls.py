from django.urls import path
from fx_rates_app import views
from .views import (CashListView, SharesListView, FxListView, CashDetailView,
                    CashUpdateView, CashDeleteView, SharesDetailView,
                    SharesUpdateView, SharesDeleteView,update_shares_list)  # why do I need this if I have already imported view above?

app_name = 'fx_rates_app'


urlpatterns = [
    path('fx_list/',FxListView.as_view(), name='fx'),
    path('shares/',views.Shares,name='shares'),
    path('cash_list/',CashListView.as_view(), name='cash_list'),
    path('shares_list/',SharesListView.as_view(), name='shares_list'),
    path('createcash/',views.CashCreateView.as_view(),name='create_cash'),
    path('createshares/',views.SharesCreateView.as_view(),name='create_shares'),
    path('cash_list/<int:pk>',views.CashDetailView.as_view(),name='detail'),
    path('update/<int:pk>/', views.CashUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.CashDeleteView.as_view(), name='delete'),
    path('shares_list/<int:pk>', views.SharesDetailView.as_view(), name='stock_detail'),
    path('update_stock/<int:pk>/', views.SharesUpdateView.as_view(), name='stock_update'),
    path('delete_stock/<int:pk>/', views.SharesDeleteView.as_view(), name='stock_delete'),
    path('update/',FxListView.update, name='update'),
    path('update_shares_list/', update_shares_list, name='update_shares_list'),
    # path('update_shares/',SharesListView.update2, name='update2'),

    # path('',views.CView.as_view()),
]
