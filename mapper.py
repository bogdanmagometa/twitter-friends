from typing import Tuple
from typing import Union

import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
import folium

from pprint import pprint

from hidden import get_keys


def create_map_for_user(username: str) -> Union[str, None]:
    """
    Return map in form of string containing html. There'are the locations of user specified by passed in
    username and his friends marked on the map.
    Return None if the user with specified username doesn't exist.
    """

    # get info about user and friends
    user = get_user_info(username)
    if user == None:
        return None
    friends = get_friends(username)

    print(f"Number of friends is {len(friends)}")

    fg_users = folium.FeatureGroup(name="User and his friends")

    # add user's marker to map if possible
    if 'location' in user:
        user_coords = get_coords_by_address(user['location'])
        world_map = folium.Map(location=user_coords, zoom_start=7)
        if user_coords:
            fg_users.add_child(folium.Marker(popup=user['name'], location=user_coords))
    else:
        print('no location for entered user')
        world_map = folium.Map()

    # add friends' markers to map if possible
    for friend in friends:
        if 'location' not in friend:
            print('no location for ' + friend['name'])
            continue
        print(f"location of {friend['name']} is {friend['location']}")
        friend_coords = get_coords_by_address(friend['location'])
        if friend_coords:
            fg_users.add_child(folium.CircleMarker(popup=friend['name'], location=friend_coords,
                                                                fill_color='red', fill_opacity=100))

    world_map.add_child(fg_users)

    return world_map._repr_html_()


def get_coords_by_address(address: str) -> Tuple[float, float]:
    """
    Transform passed in address to coordinates (lattitude and longitude).
    Return coordinates if successful, otherwise, return None.
    """

    try:
        geocoder = Nominatim(user_agent="twitter-friends")
        location = geocoder.geocode(address)
        return location.latitude, location.longitude
    except (GeocoderUnavailable, AttributeError):
        return None


def get_friends(username: str) -> dict:
    """
    Get list of user objects that are friends of the user specified by passed in username.

    Precondition: the user with passed in username exists.
    """

    url = "https://api.twitter.com/1.1/friends/list.json"

    headers = {'Authorization': "Bearer " + get_keys()['Bearer token']}
    query = {'screen_name': username, 'count': 20}

    response = requests.get(url=url, headers=headers, params=query)

    return response.json()['users']


def get_user_info(username: str) -> dict:
    """
    Return information about profile of the user specified by passed in username.
    Return None if the user with specified username doesn't exist or some there's another problem.
    """

    url = "https://api.twitter.com/2/users/by/username/" + username

    headers = {'Authorization': "Bearer " + get_keys()['Bearer token']}
    query = {'user.fields': "location"}

    response = requests.get(url, headers=headers, params=query)

    json_dict = response.json()

    if 'data' in json_dict:
        return response.json()['data']

    return None
