
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import requests
from Models.models import DeliveryPersonal
from config.envFile import GOOGLE_MAPS_API_KEY
import re
from config.eta import get_eta


async def find_nearby_delivery_partners(db: Session, restaurant_lat: float, restaurant_long: float, radius_km: int):
    try:
        # Fetch all available delivery partners

        delivery_partners = db.query(DeliveryPersonal).filter(DeliveryPersonal.is_available == True).all()

        # Prepare the origins and destinations
        origins = [(restaurant_lat, restaurant_long)]

        destinations = [(partner.current_latitude, partner.current_longitude) for partner in delivery_partners]

        # Prepare the Google Distance Matrix API request
        origins_str = "|".join([f"{lat},{long}" for lat, long in origins])
        destinations_str = "|".join([f"{lat},{long}" for lat, long in destinations])

        # Construct the Google Distance Matrix API URL
        google_maps_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins_str}&destinations={destinations_str}&key={GOOGLE_MAPS_API_KEY}"

        # Make the API request
        response = requests.get(google_maps_url)

        distance_data = response.json()


        # Extract and filter distances based on the radius
        nearby_partners = []

        for i, element in enumerate(distance_data["rows"][0]["elements"]):
            distance_text = element["distance"]["text"]  # e.g., "8.4 km"
            distance_value = element["distance"]["value"] / 1000  # in km

            if distance_value <= radius_km:
                delivery_partner = delivery_partners[i]
                nearby_partners.append({
                    "id": delivery_partner.id,
                    "name": delivery_partner.name,
                    "distance": distance_text,
                    "duration": element["duration"]["text"],  # e.g., "18 mins"
                    "current_latitude": delivery_partner.current_latitude,
                    "current_longitude": delivery_partner.current_longitude
                })

        # Return the filtered nearby partners

        return nearby_partners

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching nearby delivery partners: {str(e)}"
        )

async def get_nearest_restaurant( user_lat: float, user_lon: float):
    try:
        # get resturants lat and long
        #place url
        places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={user_lat},{user_lon}&radius=5000&type=restaurant&key={GOOGLE_MAPS_API_KEY}"
        response = requests.get(places_url)
        response_data = response.json()
        if response_data.get('status') != 'OK' or len(response_data['results']) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No nearby restaurants found"
            )
        resturant=response_data['results'][0]

        resturant_lat=resturant["geometry"]["location"]["lat"]
        resturant_long=resturant["geometry"]["location"]["lng"]
        return resturant_lat,resturant_long

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={str(e)}
        )


async def is_within_delivery_radius(user_lat: float, user_long: float, delivery_radius: float):

        # get resturants lat and long
        resturant_lat,resturant_long= await get_nearest_restaurant(user_lat, user_long)
        print(resturant_lat,resturant_long)

        # calulate eta between resturant and user
        eta= await get_eta(GOOGLE_MAPS_API_KEY, f"{resturant_lat},{resturant_long}", f"{user_lat},{user_long}")

        if not eta:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to calculate eta"
            )


        # check if eta is within delivery radius
        
        if float(eta.split(" ")[0]) > delivery_radius:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Address is outside the delivery radius"
            )

        return True


