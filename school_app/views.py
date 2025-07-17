from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import SchoolClass, Student, Nomination, StudentNomination, SchoolSettings
from django.template.loader import get_template
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def generate_student_pdf(request, student_id):
    student = get_object_or_404(Student, student_id=student_id, is_active=True)
    nominations = StudentNomination.objects.filter(student=student).order_by('-date_awarded')

    # Создаем HTTP-ответ для PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.full_name}.pdf"'

    # Создаем PDF в памяти (BytesIO)
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Регистрируем и используем шрифт с поддержкой кириллицы
    font_path = '/root/school13/static/fonts/DejaVuSans.ttf'  # Путь на сервере
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
    p.setFont("DejaVuSans", 12)

    # Пишем текст в PDF
    p.drawString(100, 750, f"Имя: {student.full_name}")
    p.drawString(100, 730, f"Возраст: {student.age}")
    p.drawString(100, 710, f"Дата рождения: {student.birth_date.strftime('%d.%m.%Y')}")
    p.drawString(100, 690, f"Класс: {student.school_class}")

    y_position = 670  # Начальная позиция для списка номинаций
    p.drawString(100, y_position, "Статистика по номинациям:")

    # Считаем количество каждой номинации для ученика
    from collections import Counter
    nomination_counts = Counter([n.nomination.title_ru for n in nominations])
    for title, count in nomination_counts.items():
        y_position -= 20
        p.drawString(120, y_position, f"{title}: {count}")

    y_position -= 30
    p.drawString(100, y_position, "Список номинаций:")

    # Пишем номинации подробно
    for nomination in nominations:
        y_position -= 20
        p.drawString(120, y_position, f"{nomination.nomination.title_ru} — {nomination.date_awarded.strftime('%d.%m.%Y')}")

    # Закрываем и сохраняем PDF в буфер
    p.showPage()
    p.save()

    # Переносим содержимое буфера в ответ
    buffer.seek(0)
    response.write(buffer.getvalue())
    
    return response

def get_school_settings():
    settings, created = SchoolSettings.objects.get_or_create(
        defaults={
            'school_name_ru': 'Школа №13',
            'school_name_uz': '13-maktab',
            'total_students': 5000,
            'total_achievements': 12500,
            'phone': '+998 XX XXX XX XX',
            'telegram': 'https://t.me/maktabimizhayoti',
        }
    )
    return settings

def home(request):
    settings = get_school_settings()
    classes = SchoolClass.objects.all()
    nominations = Nomination.objects.filter(is_active=True)
    
    # Calculate real statistics from database
    total_students = Student.objects.filter(is_active=True).count()
    
    # Update settings with real numbers
    if settings.total_students != total_students:
        settings.total_students = total_students
        settings.save()
    
    
    context = {
        'settings': settings,
        'total_classes': classes.count(),
        'total_nominations': nominations.count(),
        'total_students': total_students,
        'classes': classes,
        'nominations': nominations,
    }
    return render(request, 'school_app/home.html', context)

def classes_view(request):
    classes = SchoolClass.objects.all().order_by('grade', 'section')
    classes_by_grade = {}
    
    for school_class in classes:
        if school_class.grade not in classes_by_grade:
            classes_by_grade[school_class.grade] = []
        classes_by_grade[school_class.grade].append(school_class)
    
    context = {
        'classes_by_grade': classes_by_grade,
        'settings': get_school_settings(),
    }
    return render(request, 'school_app/classes.html', context)

def class_detail(request, grade, section):
    school_class = get_object_or_404(SchoolClass, grade=grade, section=section)
    students = Student.objects.filter(school_class=school_class, is_active=True).order_by('last_name', 'first_name')
    
    # Pagination
    paginator = Paginator(students, 12)  # Show 12 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'school_class': school_class,
        'students': page_obj,
        'settings': get_school_settings(),
    }
    return render(request, 'school_app/class_detail.html', context)

def student_detail(request, student_id):
    student = get_object_or_404(Student, student_id=student_id, is_active=True)
    nominations = StudentNomination.objects.filter(student=student).order_by('-date_awarded')

    # Подсчитываем количество номинаций и дату последней номинации для каждой номинации
    nomination_stats = {}
    for nomination in Nomination.objects.all():
        student_nominations = nominations.filter(nomination=nomination)
        nomination_stats[nomination] = {
            'count': student_nominations.count(),
            'last_nomination_date': student_nominations.first().date_awarded if student_nominations else None
        }

    context = {
        'student': student,
        'nomination_stats': nomination_stats,  # Теперь для каждой номинации статистика
        'nominations': nominations,
        'settings': get_school_settings(),
    }
    return render(request, 'school_app/student_detail.html', context)


def nominations_view(request):
    nominations = Nomination.objects.filter(is_active=True).order_by('name')
    
    context = {
        'nominations': nominations,
        'settings': get_school_settings(),
    }
    return render(request, 'school_app/nominations.html', context)

def nomination_detail(request, nomination_name):
    nomination = get_object_or_404(Nomination, name=nomination_name, is_active=True)
    recipients = StudentNomination.objects.filter(nomination=nomination).order_by('-date_awarded')
    
    # Pagination
    paginator = Paginator(recipients, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'nomination': nomination,
        'recipients': page_obj,
        'settings': get_school_settings(),
    }
    return render(request, 'school_app/nomination_detail.html', context)




def api_class_students(request, grade, section):
    """API endpoint for getting class students"""
    school_class = get_object_or_404(SchoolClass, grade=grade, section=section)
    students = Student.objects.filter(school_class=school_class, is_active=True)
    
    students_data = []
    for student in students:
        students_data.append({
            'id': student.student_id,
            'name': student.full_name,
            'photo': student.photo.url if student.photo else None,
            'age': student.age,
            'achievements': student.achievements,
        })
    
    return JsonResponse({
        'class': f"{grade}-{section}",
        'students': students_data,
        'count': len(students_data)
    })
