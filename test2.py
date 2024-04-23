# Создаем словарь для хранения функций
function_dict = {}

# Функция, которую мы будем добавлять в словарь
def greet(name):
    return "Привет, {}!".format(name)

# Добавляем функцию в словарь
function_dict['greet'] = greet

# Теперь мы можем вызвать функцию из словаря, передав нужный аргумент
name = 'Alice'
if 'greet' in function_dict:
    result = function_dict['greet'](name)
    print(result)