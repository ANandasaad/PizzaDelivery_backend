import  requests




async def get_location(api_key):
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}"
    payload = {"considerIp": True}

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")