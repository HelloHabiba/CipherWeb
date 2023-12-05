# subapp/urls.py
from django.urls import path

from spaces import views

urlpatterns = [
    path("download_key/<str:key_type>", views.download_key, name="download_key"),
    path("download_file/<int:file_id>", views.download_file, name="download_file"),
    path("decrypt_file/<int:file_id>", views.decrypt_file, name="decrypt_file"),
    path("delete_file/<int:file_id>", views.delete_file, name="delete_file"),
    path('handle_file_upload', views.handle_file_upload, name='handle_file_upload'),
    path("file_list/", views.file_list, name="file_list"),
    path("home", views.home_page, name="home"),
]
