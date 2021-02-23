from typing import Tuple
from typing import Union
from typing import Optional

import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
import folium
from folium.plugins import MarkerCluster

from pprint import pprint

from hidden import get_keys


def create_map_for_user(username: str, token: Optional[str]) -> Union[str, None]:
    """
    Return map in form of string containing html. There'are the locations of user specified by passed in
    username and his friends marked on the map.
    Return None if the user with specified username doesn't exist.
    """

    # get info about user and friends
    user = get_user_info(username, token)
    friends = get_friends(username, token)

    if user is None or friends is None:
        return None

    print(f"Number of friends is {len(friends)}")

    fg_users = folium.FeatureGroup(name="Without clusters", show=False)
    marker_cluster = MarkerCluster(name="With clusters")

    # add user's marker to map if possible
    if 'location' in user:
        user_coords = get_coords_by_address(user['location'])
        world_map = folium.Map(location=user_coords, zoom_start=7)
        if user_coords:
            icon = folium.Icon(icon="user", color='red')
            marker_cluster.add_child(folium.Marker(popup=user['name'], location=user_coords,
                                                        icon=icon))
            fg_users.add_child(folium.Marker(popup=user['name'], location=user_coords,
                                                        icon=icon))
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
            image_url = friend["profile_image_url_https"].replace("_normal", "")
            icon = folium.features.CustomIcon(image_url, icon_size=(60,60))
            marker_cluster.add_child(folium.Marker(popup=friend['name'], location=friend_coords,
                                    icon=icon))
            icon = folium.features.CustomIcon(image_url, icon_size=(60,60))
            fg_users.add_child(folium.Marker(popup=friend['name'], location=friend_coords,
                                    icon=icon))

    world_map.add_child(fg_users)
    world_map.add_child(marker_cluster)
    world_map.add_child(folium.LayerControl())

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


def get_friends(username: str, token: Optional[str]) -> dict:
    """
    Get list of user objects that are friends of the user specified by passed in username.

    Precondition: the user with passed in username exists.
    """

    url = "https://api.twitter.com/1.1/friends/list.json"

    if not token:
        token = get_keys()['Bearer token']

    NUM_FRIENDS = 20

    headers = {'Authorization': "Bearer " + token}
    query = {'screen_name': username, 'count': NUM_FRIENDS}

    response = requests.get(url=url, headers=headers, params=query)

    json_dict = response.json()

    if 'users' in json_dict:
        return json_dict['users']

    return None



def get_user_info(username: str, token: Optional[str]) -> dict:
    """
    Return information about profile of the user specified by passed in username.
    Return None if the user with specified username doesn't exist or some there's another problem.
    """

    url = "https://api.twitter.com/2/users/by/username/" + username

    if not token:
        token = get_keys()['Bearer token']

    headers = {'Authorization': "Bearer " + token}
    query = {'user.fields': "location"}

    response = requests.get(url, headers=headers, params=query)

    json_dict = response.json()

    if 'data' in json_dict:
        return response.json()['data']

    return None


def is_valid(username: str) -> bool:
    """
    Return True if specified username is valid, False otherwise.

    >>> is_valid("BarackObama")
    True
    >>> is_valid("b.23")
    False
    >>> is_valid("Helloworld ")
    False
    """

    for char in username:
        if (97 <= ord(char) <= 122) or (65 <= ord(char) <= 90) or char == '_':
            continue
        return False

    return True
