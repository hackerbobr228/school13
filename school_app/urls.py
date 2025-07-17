from django.urls import path
from . import views
from .views import generate_student_pdf

urlpatterns = [
    path('', views.home, name='home'),
    path('classes/', views.classes_view, name='classes'),
    path('class/<int:grade>-<str:section>/', views.class_detail, name='class_detail'),
    path('student/<str:student_id>/', views.student_detail, name='student_detail'),
    path('student/<str:student_id>/pdf/', generate_student_pdf, name='student_pdf'),
    path('nominations/', views.nominations_view, name='nominations'),
    path('nomination/<str:nomination_name>/', views.nomination_detail, name='nomination_detail'),
    path('api/class/<int:grade>-<str:section>/students/', views.api_class_students, name='api_class_students'),
]
