from django.db import models
from django.urls import reverse
from PIL import Image
import os
import uuid 

class SchoolClass(models.Model):
    GRADE_CHOICES = [
        (1, '1 класс'),
        (2, '2 класс'),
        (3, '3 класс'),
        (4, '4 класс'),
        (5, '5 класс'),
        (6, '6 класс'),
        (7, '7 класс'),
        (8, '8 класс'),
        (9, '9 класс'),
        (10, '10 класс'),
        (11, '11 класс'),
    ]
    
    SECTION_CHOICES = [
    ('А', 'А'),
    ('Б', 'Б'),
    ('В', 'В'),
    ('Г', 'Г'),
    ('Д', 'Д'),
    ('Е', 'Е'),
    ('Ж', 'Ж'),
    ('З', 'З'),
    ('И', 'И'),
    ('К', 'К'),
    ('Л', 'Л'),
    ('М', 'М'),
    ('Н', 'Н'),
]
    
    grade = models.IntegerField(choices=GRADE_CHOICES, verbose_name="Класс")
    section = models.CharField(max_length=1, choices=SECTION_CHOICES, verbose_name="Секция")
    class_teacher = models.CharField(max_length=100, verbose_name="Классный руководитель")
    description = models.TextField(blank=True, verbose_name="Описание класса")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"
        unique_together = ['grade', 'section']
        ordering = ['grade', 'section']
    
    def __str__(self):
        return f"{self.grade}-{self.section}"
    
    def get_absolute_url(self):
        return reverse('class_detail', kwargs={'grade': self.grade, 'section': self.section})
    
    @property
    def student_count(self):
        return self.students.count()

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Отчество")
    photo = models.ImageField(upload_to='students/', blank=True, null=True, verbose_name="Фото")
    birth_date = models.DateField(verbose_name="Дата рождения")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='students', verbose_name="Класс")
    student_id = models.CharField(max_length=20, unique=True, editable=False, blank=True, verbose_name="ID ученика")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    address = models.TextField(blank=True, verbose_name="Адрес")
    parent_name = models.CharField(max_length=100, blank=True, verbose_name="ФИО родителя")
    parent_phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон родителя")
    achievements = models.TextField(blank=True, verbose_name="Достижения")
    hobbies = models.TextField(blank=True, verbose_name="Увлечения")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.school_class})"
    
    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"
    
    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = str(uuid.uuid4())[:8]  # короткий, уникальный ID

        super().save(*args, **kwargs)

    # Обработка фото, только если оно есть и уже сохранено
        if self.photo:
            photo_path = self.photo.path
            if os.path.exists(photo_path):  # чтобы не падало, если файла нет
                img = Image.open(photo_path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(photo_path)


class Nomination(models.Model):
    NOMINATION_TYPES = [
        ('orasta_qiz', 'ORASTA QIZ'),
        ('ibratli_ogil', 'IBRATLI O\'G\'IL'),
        ('hafta_lideri', 'HAFTA LIDERI'),
        ('yosh_musavvir', 'YOSH MUSAVVIR'),
        ('sanat_gunchasi', 'SAN\'AT G\'UNCHASI'),
        ('yosh_hunarmand', 'YOSH HUNARMAND'),
        ('sport_yulduzi', 'SPORT YULDUZI'),
        ('yosh_ijodkor', 'YOSH IJODKOR'),
        ('ielts', 'IELTS'),
        ('sat', 'SAT'),
        ('cefr', 'CEFR'),
        ('milliy_sertifikat', 'Milliy sertifikat'),
    ]
    
    name = models.CharField(max_length=50, choices=NOMINATION_TYPES, verbose_name="Номинация")
    title_ru = models.CharField(max_length=100, verbose_name="Название (RU)")
    title_uz = models.CharField(max_length=100, verbose_name="Название (UZ)")
    description_ru = models.TextField(verbose_name="Описание (RU)")
    description_uz = models.TextField(verbose_name="Описание (UZ)")
    image = models.ImageField(upload_to='nominations/', blank=True, null=True, verbose_name="Изображение")

    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Номинация"
        verbose_name_plural = "Номинации"
        ordering = ['name']
    
    def __str__(self):
        return self.title_ru

class StudentNomination(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='nominations', verbose_name="Ученик")
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, related_name='recipients', verbose_name="Номинация")
    achievement_description = models.TextField(verbose_name="Описание достижения")
    date_awarded = models.DateField(verbose_name="Дата получения")
    certificate_image = models.ImageField(upload_to='certificates/', blank=True, null=True, verbose_name="Сертификат")
    score = models.CharField(max_length=50, blank=True, verbose_name="Балл/Результат")
    
    class Meta:
        verbose_name = "Номинация ученика"
        verbose_name_plural = "Номинации учеников"
        unique_together = ['student', 'nomination']
        ordering = ['-date_awarded']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.nomination.title_ru}"



class SchoolSettings(models.Model):
    school_name_ru = models.CharField(max_length=100, default="Школа №13", verbose_name="Название школы (RU)")
    school_name_uz = models.CharField(max_length=100, default="13-maktab", verbose_name="Название школы (UZ)")
    total_students = models.IntegerField(default=5000, verbose_name="Общее количество учеников")
    total_achievements = models.IntegerField(default=12500, verbose_name="Общее количество достижений")
    phone = models.CharField(max_length=20, default="+998 XX XXX XX XX", verbose_name="Телефон")
    telegram = models.CharField(verbose_name="Telegram", max_length=100)
    address_ru = models.TextField(blank=True, verbose_name="Адрес (RU)")
    address_uz = models.TextField(blank=True, verbose_name="Адрес (UZ)")
    about_ru = models.TextField(blank=True, verbose_name="О школе (RU)")
    about_uz = models.TextField(blank=True, verbose_name="О школе (UZ)")
    
    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"
    
    def __str__(self):
        return "Настройки сайта школы"
    
    def save(self, *args, **kwargs):
        if not self.pk and SchoolSettings.objects.exists():
            raise ValueError('Может существовать только одна запись настроек')
        return super().save(*args, **kwargs)
