import requests

def register_user_in_api(email, password, name):
    api_url = "https://tabet-app.kz/api/login_api/nomad_ashana/registr.php"
    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    try:
        # Отправляем POST-запрос
        response = requests.post(api_url, data=payload)

        # Логируем ответ API
        print(f"Статус ответа: {response.status_code}")
        print(f"Ответ API: {response.text}")

        # Если ответ успешный, пытаемся обработать JSON
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": f"Ошибка API: {response.status_code}"}
    except Exception as e:
        # Обрабатываем исключения
        return {"status": "error", "message": f"Исключение: {str(e)}"}
