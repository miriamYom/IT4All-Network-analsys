import requests

url = "http://127.0.0.1:8000/auth/sign_up"

payload = {
    "FirstName": "Chani",
    "LastName": "Chalmish",
    "RoleName": "technician",
    "Email": "chani@example.com",
    "Password": "secret"
}

response = requests.post(url, json=payload)
print(response.status_code)  # Should print the HTTP status code of the response
print(response.text)  # Should print the response body as a dictionary (if it returns JSON data)
