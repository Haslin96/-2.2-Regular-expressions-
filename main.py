import re
from pprint import pprint
import csv


def format_phone(phone):
    # Удаляем все нецифровые символы из номера телефона
    digits = re.sub(r'\D', '', phone)
    # Форматируем номер телефона в виде +7(999)999-99-99
    formatted_phone = re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\2)\3-\4-\5', digits)
    return formatted_phone


def cleanup_contacts(contacts):
    cleaned_contacts = []
    unique_contacts = {}

    for contact in contacts:
        last_name, first_name, surname, organization, position, phone, email = contact

        # Разделяем полное имя на фамилию, имя и отчество
        name_parts = re.split(r'\s+', f'{last_name} {first_name} {surname}')
        last_name, first_name, surname = name_parts[:3]

        # Форматируем номер телефона
        formatted_phone = format_phone(phone)

        # Группируем контакты по имени и фамилии
        key = f'{first_name} {last_name}'
        if key in unique_contacts:
            # Объединяем дублирующиеся контакты, обновляя организацию, должность и электронную почту
            existing_contact = unique_contacts[key]
            existing_contact[3] = organization
            existing_contact[4] = position
            existing_contact[6] = email
        else:
            unique_contacts[key] = [last_name, first_name, surname, organization, position, formatted_phone, email]

    # Преобразуем словарь уникальных контактов обратно в список
    cleaned_contacts = list(unique_contacts.values())
    return cleaned_contacts


# Читаем CSV-файл в список
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Очищаем контакты
cleaned_contacts_list = cleanup_contacts(contacts_list)

# Выводим очищенные контакты
pprint(cleaned_contacts_list)

# Сохраняем очищенные контакты в новый файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(cleaned_contacts_list)