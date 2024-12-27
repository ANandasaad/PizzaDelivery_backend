import  requests
from fastapi import HTTPException,status
async def get_eta(api_key:str, origin:str, destination:str) -> dict:
    try:
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={api_key}"
        response = requests.get(url)
        response_data = response.json()

        duration = response_data['rows'][0]['elements'][0]["distance"]['text']
        return duration
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching eta: {str(e)}"
        )