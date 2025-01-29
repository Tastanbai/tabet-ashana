import requests
import json

def register_user_in_api(email, password, name):
    api_url = "https://tabet-app.kz/api/login_api/nomad_ashana/registr.php"
    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers, timeout=10)
    return response.json()

register_user_in_api("tastanbay02@gmail.com", "AlemAlem2002@", "Оспан Мизамов")
