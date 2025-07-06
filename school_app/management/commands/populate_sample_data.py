from django.core.management.base import BaseCommand
from school_app.models import Achievement, Student
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with sample achievements'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample achievements...')
        
        achievements_data = [
            {
                'title': 'Победа в республиканской олимпиаде по математике',
                'description': 'Наши ученики заняли призовые места в республиканской олимпиаде по математике, показав высокий уровень знаний и аналитического мышления.',
                'achievement_type': 'academic',
                'level': 'national',
                'teacher_responsible': 'Иванова А.И.',
                'is_featured': True,
            },
            {
                'title': 'Чемпионат по футболу среди школ района',
                'description': 'Школьная команда по футболу стала чемпионом районных соревнований, продемонстрировав отличную командную работу.',
                'achievement_type': 'sports',
                'level': 'district',
                'teacher_responsible': 'Петров С.М.',
                'is_featured': True,
            },
            {
                'title': 'Международный конкурс детского рисунка',
                'description': 'Ученики нашей школы получили дипломы на международном конкурсе детского творчества.',
                'achievement_type': 'arts',
                'level': 'international',
                'teacher_responsible': 'Сидорова Е.В.',
                'is_featured': True,
            },
            {
                'title': 'Научно-практическая конференция "Шаг в будущее"',
                'description': 'Проекты наших учеников были отмечены жюри на региональной научно-практической конференции.',
                'achievement_type': 'science',
                'level': 'regional',
                'teacher_responsible': 'Козлова Н.П.',
                'is_featured': True,
            },
            {
                'title': 'Волонтерская акция "Помоги ближнему"',
                'description': 'Ученики школы организовали и провели благотворительную акцию помощи нуждающимся семьям.',
                'achievement_type': 'social',
                'level': 'city',
                'teacher_responsible': 'Морозова Т.А.',
                'is_featured': True,
            },
            {
                'title': 'Городская олимпиада по информатике',
                'description': 'Команда программистов заняла первое место в городской олимпиаде по информатике.',
                'achievement_type': 'academic',
                'level': 'city',
                'teacher_responsible': 'Волкова И.Н.',
                'is_featured': True,
            },
            {
                'title': 'Театральный фестиваль "Золотая маска"',
                'description': 'Школьный театр получил гран-при на региональном театральном фестивале.',
                'achievement_type': 'arts',
                'level': 'regional',
                'teacher_responsible': 'Орлова С.М.',
            },
            {
                'title': 'Экологический проект "Зеленая школа"',
                'description': 'Школа получила сертификат "Зеленая школа" за активную экологическую деятельность.',
                'achievement_type': 'social',
                'level': 'national',
                'teacher_responsible': 'Лебедева К.С.',
            },
            {
                'title': 'Соревнования по плаванию',
                'description': 'Школьная команда пловцов завоевала золотые медали на городских соревнованиях.',
                'achievement_type': 'sports',
                'level': 'city',
                'teacher_responsible': 'Соколова Д.В.',
            },
            {
                'title': 'Конкурс "Лучший ученический проект"',
                'description': 'Инновационные проекты учеников получили признание на школьном уровне.',
                'achievement_type': 'science',
                'level': 'school',
                'teacher_responsible': 'Белова Л.И.',
            },
        ]
        
        created_count = 0
        for achievement_data in achievements_data:
            # Random date within last year
            days_ago = random.randint(1, 365)
            achievement_date = date.today() - timedelta(days=days_ago)
            
            achievement, created = Achievement.objects.get_or_create(
                title=achievement_data['title'],
                defaults={
                    **achievement_data,
                    'date_achieved': achievement_date,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'✅ Created achievement: {achievement.title}')
                
                # Add random participants from 8-A class
                students_8a = Student.objects.filter(school_class__grade=8, school_class__section='A')
                if students_8a.exists():
                    # Add 1-5 random participants
                    num_participants = random.randint(1, min(5, students_8a.count()))
                    participants = random.sample(list(students_8a), num_participants)
                    achievement.participants.set(participants)
                    
                    self.stdout.write(f'   Added {num_participants} participants')
            else:
                self.stdout.write(f'⚠️  Achievement already exists: {achievement.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} achievements!')
        )
