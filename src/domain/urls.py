from django.urls import path
from domain.views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
]
