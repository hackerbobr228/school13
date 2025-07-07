#!/usr/bin/env python3
import re
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

def validate_translations():
    print(Fore.CYAN + "\n🔍 VALIDATING TRANSLATION SYSTEM...")
    print("=" * 60)

    test_cases = [
        {"ru": "Класс 11-И", "uz_expected": "11-И sinf", "context": "class-title"},
        {"ru": "Классный руководитель: Елена Валерьевна", "uz_expected": "Sinf rahbari: Елена Валерьевна", "context": "class-teacher"},
        {"ru": "Количество учеников: 1", "uz_expected": "O'quvchilar soni: 1", "context": "student-count"},
        {"ru": "Кабинет: 101", "uz_expected": "Xona raqami: 101", "context": "room-number"},
        {"ru": "14 лет", "uz_expected": "14 yoshda", "context": "age"},
        {"ru": "Мужской", "uz_expected": "Erkak", "context": "gender"},
        {"ru": "Женский", "uz_expected": "Ayol", "context": "gender"},
    ]

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

    passed = 0
    failed = 0

    print(Fore.YELLOW + "\n📦 ТЕСТЫ ПЕРЕВОДА:")
    print("-" * 60)

    for i, test_case in enumerate(test_cases, 1):
        ru_text = test_case["ru"]
        expected_uz = test_case["uz_expected"]

        translated = ru_text
        for pattern in patterns:
            if re.search(pattern["ru"], translated, re.IGNORECASE):
                translated = re.sub(pattern["ru"], pattern["uz"], translated, flags=re.IGNORECASE)

        if translated == expected_uz:
            print(Fore.GREEN + f"✅ Test {i} PASSED")
            passed += 1
        else:
            print(Fore.RED + f"❌ Test {i} FAILED")
            print(f"   🔹 Input:      {ru_text}")
            print(f"   🔹 Expected:   {expected_uz}")
            print(f"   🔸 Got:        {translated}")
            failed += 1

    print(Fore.CYAN + "\n🧩 ПРОВЕРКА КЛЮЧЕЙ В JS:")
    print("-" * 60)

    js_file = Path("static/js/script.js")
    if js_file.exists():
        js_content = js_file.read_text(encoding='utf-8')
        ru_keys = re.findall(r'"([^"]+)":\s*"[^"]*"', js_content)
        ru_keys = [k for k in ru_keys if not k.startswith('uz')]

        print(f"🔍 Найдено {len(ru_keys)} переводимых ключей")

        critical_keys = [
            "class-teacher", "student-count", "room-number", "class-description",
            "personal-info", "contact-info", "parent-info", "full-name", "age",
            "birth-date", "gender", "student-id", "class", "phone", "email",
            "parent-name", "parent-phone", "achievements", "hobbies", "male",
            "female", "years-old", "no-photo", "no-students", "received-nominations"
        ]

        missing = [key for key in critical_keys if key not in ru_keys]
        if missing:
            print(Fore.RED + f"⚠️  Отсутствуют важные ключи перевода: {missing}")
            failed += len(missing)
        else:
            print(Fore.GREEN + "✅ Все ключи перевода на месте")
            passed += len(critical_keys)
    else:
        print(Fore.RED + "❌ JS-файл перевода не найден: static/js/script.js")
        failed += 1

    print("\n" + "=" * 60)
    print(Fore.CYAN + f"📊 ИТОГ: УСПЕШНО: {passed}, НЕУДАЧНО: {failed}")
    if failed == 0:
        print(Fore.GREEN + "🎉 Все тесты пройдены успешно!")
    else:
        print(Fore.RED + "⚠️  Некоторые тесты провалены. Проверь переводы!")

if __name__ == "__main__":
    validate_translations()
