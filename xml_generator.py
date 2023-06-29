import xml.etree.ElementTree as ET


def generate_xml(user_id, user_category, user_object, user_branch, user_firstname_lastname,
                 user_number_phone_or_email, user_question):
    # Создание корневого элемента таблицы
    table = ET.Element('table')

    # Создание элемента для каждой записи данных
    entry = ET.SubElement(table, 'entry')

    # Добавление элементов данных в запись
    element = ET.SubElement(entry, 'user_id')
    element.text = str(user_id)

    element = ET.SubElement(entry, 'user_category')
    element.text = str(user_category)

    element = ET.SubElement(entry, 'user_object')
    element.text = str(user_object)

    element = ET.SubElement(entry, 'user_branch')
    element.text = str(user_branch)

    element = ET.SubElement(entry, 'user_firstname_lastname')
    element.text = str(user_firstname_lastname)

    element = ET.SubElement(entry, 'user_number_phone_or_email')
    element.text = str(user_number_phone_or_email)

    element = ET.SubElement(entry, 'user_question')
    element.text = str(user_question)

    # Создание XML-дерева
    tree = ET.ElementTree(table)

    # Сохранение XML-дерева в файл
    tree.write('user_data.xml', encoding='utf-8', xml_declaration=True)
