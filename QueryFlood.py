import requests, random, string
from concurrent.futures import ThreadPoolExecutor

def rand_domain():
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + ".com"

def flood():
    while True:
        try:
            d = rand_domain()
            r = requests.get(f"http://127.0.0.1:3000/resolve?domain={d}", timeout=3)
            print(r.status_code)
        except:
            pass

with ThreadPoolExecutor(max_workers=100) as ex:
    for _ in range(100):
        ex.submit(flood)
