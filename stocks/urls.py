from django.urls import path

from . import views

urlpatterns = [
    path("", views.homeView, name = "home"),
    path("getting-started/", views.select_stock_ticker, name = 'form'),
    path('details/<str:ticker>/', views.stock_details, name = 'stock_details'),
    path('analyze/<str:ticker>/', views.analyze_stock, name = 'analyze_stock'),
    path("gainers-losers/", views.top_stock_gainer_loser, name = 'top_stock_gainer_loser'),
    path("news/", views.get_news, name = 'get_news'),
]