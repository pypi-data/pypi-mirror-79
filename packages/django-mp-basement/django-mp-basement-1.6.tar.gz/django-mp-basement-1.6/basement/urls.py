
from django.urls import path

from basement import views


urlpatterns = [

    path('db/download/', views.download_db, name='download-db')

]
