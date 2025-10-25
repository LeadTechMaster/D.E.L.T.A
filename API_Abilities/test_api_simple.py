import requests, json
result = {"status": "starting"}
try:
    r = requests.get("https://serpapi.com/search", params={"engine": "google", "q": "pizza", "api_key": "850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c", "num": 3}, timeout=30)
    result = {"status": "success" if r.status_code == 200 else "error", "code": r.status_code, "data": r.json() if r.status_code == 200 else r.text}
except Exception as e:
    result = {"status": "exception", "error": str(e)}
with open("/Users/udishkolnik/543/D.E.L.T.A/API_Abilities/result.json", "w") as f:
    json.dump(result, f, indent=2)

