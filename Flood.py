from concurrent.futures import ThreadPoolExecutor
import requests
import random
import string

def random_string(n):
    return ''.join(random.choices(string.ascii_letters, k=n))

def post_flood():
    while True:
        try:
            payload = {
                "nama": random_string(8),
                "tanggal": "2025-05-07",
                "deskripsi": random_string(20)
            }
            r = requests.post("http://localhost:3000/data", json=payload, timeout=3)
            print(r.status_code)
        except:
            pass

with ThreadPoolExecutor(max_workers=200) as executor:
    for _ in range(1000):
        executor.submit(post_flood)
