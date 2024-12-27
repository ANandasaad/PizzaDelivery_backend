from http.client import HTTPException
from fastapi import HTTPException,status
import requests

from config.envFile import GOOGLE_MAPS_API_KEY


async def validate_address(address: str, locality: str):
  try:
    url = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={GOOGLE_MAPS_API_KEY}"
    payload = {
        "address": {
            "regionCode": "IN",
            "locality": locality,
            "addressLines": [address]
        }
    }
    response = requests.post(url, json=payload)
    data = response.json()

    # Extract address components from the response
    address_components = data.get("result", {}).get("address", {}).get("addressComponents", [])
    formatted_address = data.get("result", {}).get("address", {}).get("formattedAddress", "")
    latitude = data.get("result", {}).get("geocode", {}).get("location", {}).get("latitude")
    longitude = data.get("result", {}).get("geocode", {}).get("location", {}).get("longitude")

    # Check if formatted_address, latitude, and longitude are available
    if not formatted_address or not latitude or not longitude:
        print("Address validation failed: Missing address data (formatted address or coordinates).")
        return None, None, None  # Return None if address is invalid

    # Loop through address components to check confirmation levels
    for component in address_components:
        confirmation_level = component.get('confirmationLevel')

        # Skip the component if it has 'UNCONFIRMED_BUT_PLAUSIBLE'
        if confirmation_level == 'UNCONFIRMED_BUT_PLAUSIBLE':
            print(f"Ignoring component: {component['componentName']['text']} due to unconfirmed status.")
            continue

    # If there are any components with unconfirmed status, we should not process
    # if any(component.get('confirmationLevel') != 'CONFIRMED' for component in address_components):
    #     print("Address validation failed: Some address components are not confirmed.")
    #     return None, None, None  # Return None if address is invalid

    # If we have valid data, return the formatted address and coordinates
    return formatted_address, latitude, longitude

  except Exception as e:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=f"Address validation failed: {str(e)}"
      )