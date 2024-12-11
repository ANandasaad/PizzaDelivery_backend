import  requests
from fastapi import HTTPException,status


async def get_location(api_key: str, address: str) -> dict:
    """Fetch latitude and longitude from Google Maps API."""
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
        response = requests.get(url)
        response_data = response.json()

        if response.status_code != 200 or 'results' not in response_data or not response_data['results']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to fetch geolocation for the provided address."
            )

        location = response_data["results"][0]["geometry"]["location"]
        return location
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching geolocation: {str(e)}"
        )