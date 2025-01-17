#!/usr/bin/python
"""
With this module we check the OpenStreetMap data.
"""

import datetime  # for the timestamp
import json      # read and write json
import sys       # to check the python version
from urllib.parse import urlparse

import requests  # to check if websites are reachable
from email_validator import EmailNotValidError, validate_email

''' constants '''
# the actual date and time
TIMESTAMP = str(datetime.datetime.now())
# the actual date
DATE = str(datetime.date.today())
# the raw overpass output file (useful for later use)
OVERPASS_FILE = "../data/overpass.json"
VEGGIEPLACES_CHECK_RESULT_FILE = "../data/check_results.json"   # check results
# results of previous url checks
URL_DATA_FILE = "../data/urldata.json"

# variables to handle the json data
url_data = {}


# Get the OSM data.
def get_osm_data():
    """
    Open overpass data file.
    """
    with open(OVERPASS_FILE) as overpass_json_file:
        # Get overpass data
        overpass_data = json.load(overpass_json_file)
    return overpass_data


def is_url_format_valid(url):
    """
    Check if the URL has a valid format by trying to parse it.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def is_url_ok(url):
    """
    Check if the URL is okay by the following steps.
     1. Check if the URL has checked recently.
     2. If not, check if the URL has a valid format.
     3. If so, check if the URL is reachable.
    """
    global url_data

    result = {'date': DATE}

    if url in url_data:
        # URL has recently checked, so we save time to check again and take the last result.
        result['isOk'] = url_data[url]['isOk']
        result['text'] = url_data[url]['text']
    else:
        # URL not recently checked
        if is_url_format_valid(url):
            try:
                # Try to reach the URL
                response = requests.get(url, timeout=5)
            except Exception as e:
                # Catch all exception if the URL isn't reachable
                result['isOk'] = False
                result['text'] = f"Exception: {str(e.__class__.__name__)}"
                print(url, ' ', result['text'])
            else:
                # URL is reachable
                if response.status_code < 400:
                    # All status_codes below 400 should be fine
                    result['isOk'] = True
                    result['text'] = "OK"
                elif response.status_code == 403:
                    # We get that status from a lot of websites which are available with a browser
                    result['isOk'] = True
                    result['text'] = "Can't do full check: HTTP response: Forbidden"
                elif response.status_code == 429:
                    # We get that status from a lot of websites which are available with a browser (especially from instagram)
                    result['isOk'] = True
                    result['text'] = "Can't do full check: HTTP response: Too Many Requests"
                else:
                    result['isOk'] = False
                    result['text'] = f"HTTP response code {response.status_code}"
                    print(url, ' ', response.status_code)
        else:
            result['isOk'] = False
            result['text'] = "No valid URL format"
    return result


def check_data(data):

    places_data_checks = {"_timestamp": TIMESTAMP,
                          "type": "FeatureCollection", "features": []}

    # Variables to print progress in the console
    osm_elements_number = len(data["elements"])

    # Go through every osm element and put the information into a new places element.
    for osm_element in data["elements"]:

        osm_element_index = data["elements"].index(osm_element) + 1

        print(osm_element_index, ' / ', osm_elements_number, '\t')
        element_id = osm_element["id"]
        element_type = osm_element["type"]
        tags = osm_element.get("tags", {})

        place_check_obj = {"type": "Feature", "properties": {}}
        place_check_obj["properties"]["_id"] = element_id
        place_check_obj["properties"]["_type"] = element_type
        place_check_obj["properties"]["undefined"] = []
        place_check_obj["properties"]["issues"] = []

        if element_type == "node":
            lat = osm_element.get("lat", None)
            lon = osm_element.get("lon", None)
        elif element_type == "way" or element_type == "relation":
            # get the coordinates from the center of the object
            center_coordinates = osm_element.get("center", None)
            lat = center_coordinates.get("lat", None)
            lon = center_coordinates.get("lon", None)

        place_check_obj["geometry"] = {}
        place_check_obj["geometry"]["type"] = "Point"
        place_check_obj["geometry"]["coordinates"] = [lon, lat]

        # Name
        if "name" in tags:
            name = tags["name"]
            place_check_obj["properties"]["name"] = name
        else:
            # If there is no name, take the english if exists
            if "name:en" in tags:
                name = tags["name:en"]
            # If it is a vending machine, name it "vending machine"
            elif tags.get("amenity", "") == "vending_machine":
                name = "vending machine"
            else:
                # If there is no name given from osm, we build one
                name = "%s %s" % (element_type, element_id)
                # Log this
                place_check_obj["properties"]["undefined"].append("name")
        # Double quotes could escape code, so we have to replace them:
        name = name.replace('"', '”')
        place_check_obj["properties"]["name"] = name

        # Diet tags
        if "diet:vegan" in tags:
            diet_vegan = tags.get("diet:vegan", "")
            place_check_obj["properties"]["diet_vegan"] = diet_vegan
            if diet_vegan != "only" and diet_vegan != "yes" and diet_vegan != "limited" and diet_vegan != "no":
                place_check_obj["properties"]["issues"].append(
                    "'diet:vegan' has an unusual value: " + diet_vegan)
        else:
            place_check_obj["properties"]["undefined"].append("diet:vegan")
            #place_check_obj["properties"]["diet_vegan"] = "undefined"

        if tags.get("diet:vegan", "") != "no":
            # Cuisine
            if "cuisine" not in tags and "shop" not in tags:
                if tags.get("amenity", "") != "cafe" and tags.get("amenity", "") != "ice_cream" and tags.get("amenity", "") != "bar":
                    place_check_obj["properties"]["undefined"].append(
                        "cuisine")

            # Address
            if "addr:street" not in tags:
                place_check_obj["properties"]["undefined"].append(
                    "addr:street")
            if "addr:housenumber" not in tags:
                place_check_obj["properties"]["undefined"].append(
                    "addr:housenumber")
            if "addr:city" not in tags:
                if "addr:suburb" not in tags:
                    place_check_obj["properties"]["undefined"].append(
                        "addr:city/suburb")
            if "addr:postcode" not in tags:
                place_check_obj["properties"]["undefined"].append(
                    "addr:postcode")

            # Website (till now we only check if the URI is valid, not if the website is reachable)
            website = 'undefined'
            if "contact:website" in tags:
                website = tags.get("contact:website", "")
                if is_url_ok(website)['isOk'] is False:
                    place_check_obj["properties"]["issues"].append(
                        "'contact:website' URI invalid")
            if "website" in tags:
                website = tags.get("website", "")
                if is_url_ok(website)['isOk'] is False:
                    place_check_obj["properties"]["issues"].append(
                        "'website' URI invalid")
            if "facebook" in website:
                place_check_obj["properties"]["issues"].append(
                    "'facebook' URI as website -> change to 'contact:facebook'")
            if "instagram" in website:
                place_check_obj["properties"]["issues"].append(
                    "'instagram' URI as website -> change to 'contact:instagram'")
            if "contact:website" in tags and "website" in tags:
                place_check_obj["properties"]["issues"].append(
                    "'website' and 'contact:website' defined -> remove one")

            # Facebook
            if "contact:facebook" in tags:
                contact_facebook = tags.get("contact:facebook", "")
                if contact_facebook.startswith("http://"):
                    place_check_obj["properties"]["issues"].append(
                        "'contact:facebook' starts with 'http' instead of 'https'")
                elif not contact_facebook.startswith("https://www.facebook.com/"):
                    place_check_obj["properties"]["issues"].append(
                        "'contact:facebook' does not starts with 'https://www.facebook.com/'")
                elif is_url_ok(contact_facebook)['isOk'] is False:
                    place_check_obj["properties"]["issues"].append(
                        "'contact:facebook' URI invalid")
            if "facebook" in tags:
                place_check_obj["properties"]["issues"].append(
                    "old tag: 'facebook' -> change to 'contact:facebook'")

            # Instagram
            if "contact:instagram" in tags:
                contact_instagram = tags.get("contact:instagram", "")
                if contact_instagram.startswith("http://"):
                    place_check_obj["properties"]["issues"].append(
                        "'contact:instagram' starts with 'http' instead of 'https'")
                elif not contact_instagram.startswith("https://www.instagram.com/"):
                    place_check_obj["properties"]["issues"].append(
                        "'contact:instagram' does not starts with 'https://www.instagram.com/'")
                elif is_url_ok(contact_instagram)['isOk'] is False:
                    place_check_obj["properties"]["issues"].append(
                        "'contact:instagram' URI invalid")
            if "instagram" in tags:
                place_check_obj["properties"]["issues"].append(
                    "old tag 'instagram'")

            # E-Mail
            if "contact:email" in tags:
                email = tags.get("contact:email", "")
            elif "email" in tags:
                email = tags.get("email", "")
            if "contact:email" in tags or "email" in tags:
                try:
                    validate_email(email)
                except EmailNotValidError as e:
                    place_check_obj["properties"]["issues"].append(
                        "E-Mail is not valid: " + str(e))
            if "contact:email" in tags and "email" in tags:
                place_check_obj["properties"]["issues"].append(
                    "'email' and 'contact:email' defined -> remove one")

            # Phone
            if "contact:phone" in tags:
                contact_phone = tags.get("contact:phone", "")
                if not contact_phone.startswith("+"):
                    place_check_obj["properties"]["issues"].append(
                        "'contact:phone' has no international format like '+44 20 84527891'")
            if "phone" in tags:
                phone = tags.get("phone", "")
                if not phone.startswith("+"):
                    place_check_obj["properties"]["issues"].append(
                        "'phone' has no international format like '+44 20 84527891'")
            if "contact:phone" in tags and "phone" in tags:
                place_check_obj["properties"]["issues"].append(
                    "'phone' and 'contact:phone' defined -> remove one")

            # Opening hours
            opening_hours = 'undefined'
            if "opening_hours:covid19" in tags and tags["opening_hours:covid19"] != "same" and tags["opening_hours:covid19"] != "restricted":
                opening_hours = tags["opening_hours:covid19"]
            elif "opening_hours" in tags:
                opening_hours = tags["opening_hours"]
            else:
                place_check_obj["properties"]["undefined"].append(
                    "opening_hours")
            if "\n" in opening_hours or "\r" in opening_hours:
                place_check_obj["properties"]["issues"].append(
                    "There is a line break in 'opening_hours' -> remove")

            # Disused
            if "disused" in "".join(tags):
                place_check_obj["properties"]["issues"].append(
                    "There is a 'disused' tag: Check whether this tag is correct. If so, please remove the diet tags.")

            # Count issues
            place_check_obj["properties"]["issue_number"] = len(
                place_check_obj["properties"]["issues"]) + len(place_check_obj["properties"]["undefined"])

            if len(place_check_obj["properties"]["issues"]) == 0:
                del(place_check_obj["properties"]["issues"])
            if len(place_check_obj["properties"]["undefined"]) == 0:
                del(place_check_obj["properties"]["undefined"])

            # Only use elements with issues
            # if place_check_obj["properties"]["issue_number"] > 0:
            places_data_checks["features"].append(place_check_obj)
    print(osm_elements_number, ' elements.')
    return places_data_checks


def main():
    global url_data

    # Open url data file
    with open(URL_DATA_FILE) as url_json_file:

        # Get previous url data
        url_data = json.load(url_json_file)

        key_list = list(url_data.keys())

        for element in key_list:
            today = datetime.datetime.strptime(DATE, '%Y-%m-%d')
            url_data_date = datetime.datetime.strptime(
                url_data[element]['date'], '%Y-%m-%d')
            delta = today - url_data_date
            if delta.days > 28:
                del (url_data[element])

    # Call the functions to get and write the osm data.
    osm_data = get_osm_data()

    # Write data
    if osm_data is not None:
        check_result = check_data(osm_data)

        # Write check result file in pretty format
        outfile = open(VEGGIEPLACES_CHECK_RESULT_FILE, "w")
        outfile.write(json.dumps(check_result, indent=1, sort_keys=True))
        outfile.close()
    else:
        print("A problem has occurred. osm_data is None")

    # Write data
    if url_data is not None:
        print(url_data)
        url_outfile = open(URL_DATA_FILE, "w")
        url_outfile.write(json.dumps(url_data, indent=1, sort_keys=True))
        url_outfile.close()
    else:
        print("A problem has occurred. url_data is None")


main()
