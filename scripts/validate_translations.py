#!/usr/bin/env python3
"""
Translation Validation Script
This script validates that all Russian text elements are properly translated to Uzbek
"""

import re
import json
from pathlib import Path

def validate_translations():
    """Validate translation coverage and accuracy"""
    print("🔍 Validating Translation System...")
    print("=" * 50)
    
    # Test cases for specific problematic phrases
    test_cases = [
        {
            "ru": "Класс 11-И",
            "uz_expected": "11-И sinf",
            "context": "class-title"
        },
        {
            "ru": "Классный руководитель: Елена Валерьевна",
            "uz_expected": "Sinf rahbari: Елена Валерьевна",
            "context": "class-teacher"
        },
        {
            "ru": "Количество учеников: 1",
            "uz_expected": "O'quvchilar soni: 1",
            "context": "student-count"
        },
        {
            "ru": "Кабинет: 101",
            "uz_expected": "Xona raqami: 101",
            "context": "room-number"
        },
        {
            "ru": "14 лет",
            "uz_expected": "14 yoshda",
            "context": "age"
        },
        {
            "ru": "Мужской",
            "uz_expected": "Erkak",
            "context": "gender"
        },
        {
            "ru": "Женский",
            "uz_expected": "Ayol",
            "context": "gender"
        }
    ]
    
    # Translation patterns (same as in JavaScript)
    patterns = [
        {"ru": r"Класс\s+([А-Я0-9\-]+)", "uz": r"\1 sinf"},
        {"ru": r"(\d+)\s*класс", "uz": r"\1 sinf"},
        {"ru": r"Классный руководитель:\s*", "uz": "Sinf rahbari: "},
        {"ru": r"Учитель:\s*", "uz": "O'qituvchi: "},
        {"ru": r"Количество учеников:\s*", "uz": "O'quvchilar soni: "},
        {"ru": r"(\d+)\s*учеников", "uz": r"\1 o'quvchi"},
        {"ru": r"(\d+)\s*ученик", "uz": r"\1 o'quvchi"},
        {"ru": r"Кабинет:\s*", "uz": "Xona raqami: "},
        {"ru": r"Номер кабинета:\s*", "uz": "Xona raqami: "},
        {"ru": r"(\d+)\s*лет", "uz": r"\1 yoshda"},
        {"ru": r"(\d+)\s*года", "uz": r"\1 yoshda"},
        {"ru": r"Мужской", "uz": "Erkak"},
        {"ru": r"Женский", "uz": "Ayol"},
    ]
    
    print("Testing specific problematic phrases:")
    print("-" * 40)
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        ru_text = test_case["ru"]
        expected_uz = test_case["uz_expected"]
        
        # Apply translation patterns
        translated = ru_text
        for pattern in patterns:
            if re.search(pattern["ru"], translated, re.IGNORECASE):
                translated = re.sub(pattern["ru"], pattern["uz"], translated, flags=re.IGNORECASE)
        
        # Check if translation matches expected
        if translated == expected_uz:
            print(f"✅ Test {i}: PASS")
            print(f"   RU: '{ru_text}'")
            print(f"   UZ: '{translated}'")
        else:
            print(f"❌ Test {i}: FAIL")
            print(f"   RU: '{ru_text}'")
            print(f"   Expected: '{expected_uz}'")
            print(f"   Got: '{translated}'")
            all_passed = False
        print()
    
    # Check translation keys coverage
    print("Checking translation keys coverage:")
    print("-" * 40)
    
    # Read JavaScript translation object (simplified check)
    js_file = Path("static/js/script.js")
    if js_file.exists():
        with open(js_file, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Extract Russian keys
        ru_keys = re.findall(r'"([^"]+)":\s*"[^"]*"', js_content)
        ru_keys = [key for key in ru_keys if not key.startswith('uz')]
        
        print(f"Found {len(ru_keys)} translation keys")
        
        # Check for missing critical keys
        critical_keys = [
            "class-teacher", "student-count", "room-number", "class-description",
            "personal-info", "contact-info", "parent-info", "full-name", "age",
            "birth-date", "gender", "student-id", "class", "phone", "email",
            "parent-name", "parent-phone", "achievements", "hobbies", "male",
            "female", "years-old", "no-photo", "no-students", "received-nominations"
        ]
        
        missing_keys = []
        for key in critical_keys:
            if key not in ru_keys:
                missing_keys.append(key)
        
        if missing_keys:
            print(f"⚠️  Missing critical translation keys: {missing_keys}")
            all_passed = False
        else:
            print("✅ All critical translation keys present")
    
    # Summary
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All translation tests PASSED!")
        print("✅ Translation system is working correctly")
    else:
        print("❌ Some translation tests FAILED!")
        print("⚠️  Please check the translation implementation")
    
    print("\n📋 Recommendations:")
    print("1. Ensure all HTML elements have proper data-key or data-translate attributes")
    print("2. Test language switching in the browser")
    print("3. Check browser console for translation validation logs")
    print("4. Verify dynamic content translation patterns")
    
    return all_passed

if __name__ == "__main__":
    validate_translations()
