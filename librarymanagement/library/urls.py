
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-book/', views.add_book, name='add_book'),
    path('view-books/', views.view_books, name='view_books'),
    path('edit-book/<int:id>/', views.edit_book, name='edit_book'),
    path('delete-book/<int:id>/', views.delete_book, name='delete_book'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-member/', views.add_member, name='add_member'),
    path('view-members/', views.view_members, name='view_members'),
    path('issue-book/', views.issue_book, name='issue_book'),
    path('return-book/', views.return_book, name='return_book'),
    path('view-issued-books/', views.view_issued_books, name='view_issued_books'),
    path('edit-member/<int:id>/', views.edit_member, name='edit_member'),
    path('delete-member/<int:id>/', views.delete_member, name='delete_member'),
    path('login/', views.custom_login, name='custom_login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_page, name='logout'),
]

