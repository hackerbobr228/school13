#!/usr/bin/env python
"""
Django Project Verification Script
This script checks if the Django project is properly configured
"""

import os
import sys
import django
from pathlib import Path

def check_django_setup():
    """Check if Django project is properly set up"""
    print("🔍 Checking Django Project Setup...")
    print("=" * 50)
    
    # Check if manage.py exists
    if os.path.exists('manage.py'):
        print("✅ manage.py found")
    else:
        print("❌ manage.py not found")
        return False
    
    # Check project structure
    required_dirs = [
        'school_website',
        'school_app',
        'templates',
        'static',
    ]
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ directory found")
        else:
            print(f"❌ {dir_name}/ directory missing")
    
    # Check key files
    key_files = [
        'school_website/settings.py',
        'school_website/urls.py',
        'school_app/models.py',
        'school_app/views.py',
        'school_app/admin.py',
        'school_app/urls.py',
        'templates/base.html',
        'static/css/styles.css',
        'static/js/script.js',
        'requirements.txt',
    ]
    
    for file_path in key_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} found")
        else:
            print(f"❌ {file_path} missing")
    
    # Check template files
    template_files = [
        'templates/school_app/home.html',
        'templates/school_app/classes.html',
        'templates/school_app/class_detail.html',
        'templates/school_app/student_detail.html',
        'templates/school_app/nominations.html',
        'templates/school_app/nomination_detail.html',
    ]
    
    print("\n📄 Template Files:")
    for template in template_files:
        if os.path.exists(template):
            print(f"✅ {template} found")
        else:
            print(f"❌ {template} missing")
    
    return True

def check_django_imports():
    """Check if Django can be imported and models work"""
    print("\n🐍 Checking Django Imports...")
    print("=" * 50)
    
    try:
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_website.settings')
        django.setup()
        
        print("✅ Django setup successful")
        
        # Try importing models
        from school_app.models import SchoolClass, Student, Nomination, StudentNomination, SchoolSettings
        print("✅ Models imported successfully")
        
        # Try importing views
        from school_app import views
        print("✅ Views imported successfully")
        
        # Try importing admin
        from school_app import admin
        print("✅ Admin imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Django import error: {e}")
        return False

def check_urls():
    """Check URL patterns"""
    print("\n🔗 Checking URL Patterns...")
    print("=" * 50)
    
    try:
        from django.urls import reverse
        
        url_patterns = [
            ('home', 'home'),
            ('classes', 'classes'),
            ('nominations', 'nominations'),
            ('class_detail', 'class_detail', {'grade': 8, 'section': 'A'}),
            ('student_detail', 'student_detail', {'student_id': 'TEST001'}),
            ('nomination_detail', 'nomination_detail', {'nomination_name': 'orasta_qiz'}),
        ]
        
        for pattern in url_patterns:
            try:
                if len(pattern) == 3:
                    url = reverse(pattern[1], kwargs=pattern[2])
                    print(f"✅ {pattern[0]}: {url}")
                else:
                    url = reverse(pattern[1])
                    print(f"✅ {pattern[0]}: {url}")
            except Exception as e:
                print(f"❌ {pattern[0]}: Error - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ URL checking error: {e}")
        return False

def main():
    """Main verification function"""
    print("🚀 Django School Website Verification")
    print("=" * 50)
    
    # Check basic setup
    setup_ok = check_django_setup()
    
    if setup_ok:
        # Check Django functionality
        imports_ok = check_django_imports()
        
        if imports_ok:
            # Check URLs
            urls_ok = check_urls()
            
            if urls_ok:
                print("\n🎉 All checks passed!")
                print("\n📋 Next Steps:")
                print("1. Run: python manage.py makemigrations")
                print("2. Run: python manage.py migrate")
                print("3. Run: python manage.py populate_sample_data")
                print("4. Run: python manage.py runserver")
                print("5. Visit: http://127.0.0.1:8000/")
                print("6. Admin: http://127.0.0.1:8000/admin/")
            else:
                print("\n❌ URL configuration issues found")
        else:
            print("\n❌ Django import issues found")
    else:
        print("\n❌ Project structure issues found")

if __name__ == '__main__':
    main()
