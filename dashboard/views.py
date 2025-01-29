from django.shortcuts import render
from django.db import connections
from django.contrib.auth.decorators import login_required

@login_required
def index(request): 
    return render (request, 'dashboard/index.html')
@login_required
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
@login_required
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
@login_required
def ashanadb(request):
    data = []
    error_messages = []

    try:
        with connections['db1'].cursor() as cursor:
            # Извлекаем данные из таблицы ashana
            cursor.execute("""
                SELECT 
                    a.id, 
                    a.card, 
                    a.data, 
                    a.s_number, 
                    a.hik, 
                    a.a1, 
                    a.navigate,
                    u.name AS school_name
                FROM ashana a
                LEFT JOIN users u ON a.hik = u.name
            """)
            rows = cursor.fetchall()
            
            # Формируем данные
            for row in rows:
                data.append({
                    'id': row[0],
                    'card': row[1],
                    'data': row[2],
                    's_number': row[3],
                    'hik': row[4],
                    'a1': row[5],
                    'navigate': row[6],
                    'school_name': row[7],  # Имя школы
                })

    except Exception as e:
        # Добавляем сообщение об ошибке
        error_messages.append(f"Ошибка при доступе к таблице ashana: {str(e)}")

    return render(request, 'dashboard/ashanadb.html', {'data': data, 'error_messages': error_messages})


from django.shortcuts import render
from django.http import JsonResponse
from .utils import register_user_in_api  # Убедитесь, что это функция отправки запросов к вашему API
@login_required
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



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
@login_required
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Перенаправляем на дашборд
        else:
            messages.error(request, "Неверный логин или пароль")
    
    return render(request, "dashboard/login.html")
