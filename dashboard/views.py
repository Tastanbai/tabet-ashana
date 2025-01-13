from django.shortcuts import render
from django.db import connections


def index(request): 
    return render (request, 'dashboard/index.html')

def kitapdb_view(request):
    with connections['db2'].cursor() as cursor:
        cursor.execute("""
            SELECT 
                au.username AS school_name,
                p.name AS student_name,
                b.name AS book_name,
                p.date_out AS date_out,
                p.date_in AS date_in,
                p.iin AS iin,
                p.phone AS phone,
                'Нет' AS is_returned
            FROM 
                auth_user au
            LEFT JOIN 
                myapp_publish p ON au.id = p.user_id
            LEFT JOIN 
                myapp_book b ON p.book_id = b.id
            WHERE 
                p.id IS NOT NULL

            UNION

            SELECT 
                au.username AS school_name,
                rb.name AS student_name,
                rb.book_name AS book_name,
                rb.date_out AS date_out,
                rb.date_in AS date_in,
                rb.iin AS iin,
                rb.phone AS phone,
                'Да' AS is_returned
            FROM 
                auth_user au
            LEFT JOIN 
                myapp_returnedbook rb ON au.id = rb.user_id
            WHERE 
                rb.id IS NOT NULL

            ORDER BY 
                school_name, student_name;
        """)
        data = cursor.fetchall()

    return render(request, 'dashboard/kitapdb.html', {'data': data})


from django.shortcuts import render
from django.db import connections

def apkdb(request):
    with connections['default'].cursor() as cursor:  
        cursor.execute("""
            SELECT id, card, data, s_number, hik, a1, a2, a3, a4, navigate
            FROM School
        """)
        data = cursor.fetchall()

    # Передаём данные в шаблон
    return render(request, 'dashboard/apkdb.html', {'data': data})


from django.shortcuts import render
from django.db import connections

def ashanadb(request):
    data = []
    error_messages = []

    with connections['db1'].cursor() as cursor:  
        cursor.execute("SELECT name FROM users")
        school_names = [row[0] for row in cursor.fetchall()]

        for school_name in school_names:
            try:
                cursor.execute(f"SHOW TABLES LIKE %s", [school_name])
                if cursor.fetchone():
                    cursor.execute(f"""
                        SELECT id, card, data, s_number, hik, a1, navigate
                        FROM `{school_name}`
                    """)
                    rows = cursor.fetchall()
                    for row in rows:
                        data.append({
                            'school': school_name,
                            'id': row[0],
                            'card': row[1],
                            'data': row[2],
                            's_number': row[3],
                            'hik': row[4],
                            'a1': row[5],
                            'navigate': row[6],
                        })
                else:
                    error_messages.append(f"Таблица '{school_name}' не существует.")
            except Exception as e:
                error_messages.append(f"Ошибка при доступе к таблице '{school_name}': {str(e)}")

    return render(request, 'dashboard/ashanadb.html', {'data': data, 'error_messages': error_messages})



from django.shortcuts import render
from django.http import JsonResponse
from .utils import register_user_in_api  # Убедитесь, что это функция отправки запросов к вашему API

def register_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Отладка: вывод входных данных
        print(f"Отправляемые данные: name={name}, email={email}, password={password}")

        if not name or not email or not password:
            return render(request, 'dashboard/register.html', {
                'message': 'Все поля обязательны!',
                'success': False
            })

        # Отправка данных в API
        result = register_user_in_api(email, password, name)

        # Отладка: вывод ответа API
        print(f"Ответ API: {result}")

        return render(request, 'dashboard/register.html', {
            'message': result.get('message', 'Неизвестная ошибка'),
            'success': result.get('status') == 'success'
        })

    return render(request, 'dashboard/register.html')

