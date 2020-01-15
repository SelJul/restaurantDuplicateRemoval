import re
import pprint
from collections import defaultdict
from typing import Dict

''' Audit Name '''


def restaurant_name_regex(name):
    """
    Regex to search for words in ( )

    Parameters
    ----------
    name : str
        Restaurant name which has to be checked for ()

    Returns
    -------
    match object
        Return match of the regex or none
    """

    name_re = re.compile(r'\([a-zA-Z0-9_ ]+\)')
    return name_re.search(name)


def print_all_name_exceptions(data_set):
    """ Print all the found ( <word> ) in the name category of the data set"""
    data = data_set.get_restaurant_data()
    exceptions = defaultdict(set)

    for row in data:
        restaurant_name = row["name"]
        m = restaurant_name_regex(restaurant_name)
        if m:
            exception = m.group()
            exceptions[exception].add(restaurant_name)

    pprint.pprint(exceptions)


def audit_name(data_set):
    """
    Change the string in the name category if it contains ( <word> )

    Parameters
    ----------
    data_set : DataSet
        DataSet object from where the current data will loaded and where the new data will be saved
    """

    data = data_set.get_restaurant_data()

    for row in data:
        restaurant_name = row["name"]
        restaurant_name = re.sub(r'\([a-zA-Z0-9_ ]+\)', '', restaurant_name)
        row["name"] = restaurant_name

    data_set.set_restaurant_data(data)


''' Audit Street '''

street_mapping = {
    "ave.": "avenue",
    "aves": "avenues",
    "blv.": "boulevard",
    "blvd": "boulevard",
    "blvd.": "boulevard",
    "dr.": "drive",
    "hwy.": "highway",
    "ne": "northeast",
    "nw": "northwest",
    "pkwy": "parkway",
    "pl.": "place",
    "rd.": "road",
    "s": "south",
    "s.": "south",
    "se": "southeast",
    "st.": "street",
    "sts.": "streets",
}


def street_regex(street_name):
    """
    Regex to search for the street type which is at the end of the street name

    Parameters
    ----------
    street_name : str
        Street name which has to be checked for the street type

    Returns
    -------
    match object
        Return match of the regex or none
    """

    street_type_re = re.compile(r'\b\S+\.?$')
    return street_type_re.search(street_name)


def print_all_street_types(data_set):
    """ Print all the found street types with their corresponding street"""
    data = data_set.get_restaurant_data()
    street_types = defaultdict(set)

    for row in data:
        street_name = row["address"]
        m = street_regex(street_name)
        if m:
            street_type = m.group()
            street_types[street_type].add(street_name)

    pprint.pprint(street_types)


def update_street_name(n, street_name, mapping):
    """
    Change abbreviated street types to their full name according to the mapping

    Parameters
    ----------
    n : match object
        Match object of the street_regex()
    street_name : str
        Current street name
    mapping : Dict[str, str]
        Dict of the abbreviated street types and their according full name

    Returns
    -------
    street_name : str
        Updated or original string of the street name
    """

    n = n.group()
    for m in mapping:
        if n == m:
            street_name = street_name[:-len(n)] + mapping[m]
    return street_name


def audit_street(data_set):
    """
    Change the String in the street category to have uniform street types

    Parameters
    ----------
    data_set : DataSet
        DataSet object from where the current data will loaded and where the new data will be saved
    """

    data = data_set.get_restaurant_data()

    for row in data:
        street_name = row["address"]
        name_m = street_regex(street_name)
        if name_m:
            row["address"] = update_street_name(name_m, street_name, street_mapping)

    data_set.set_restaurant_data(data)


''' Audit City '''

city_mapping = {
    "la": "los angeles",
    "new york": "new york city",
    "w. hollywood": "hollywood",
    "west la": "los angeles",
}


def print_all_cities(data_set):
    """ Print all the found cities from the city category of the data set"""
    data = data_set.get_restaurant_data()
    cities = dict()

    for row in data:
        city = row["city"]
        cities[city] = cities.get(city, 0) + 1

    pprint.pprint(cities)


def update_city_name(city, mapping):
    """
    Change abbreviated cities to their full name according to the mapping

    Parameters
    ----------
    city : str
        Current city name
    mapping : dict[str, str]
        Dict of the abbreviated city names and their according full name

    Returns
    -------
    city : str
        Updated or original string of the city name
    """

    for m in mapping:
        if city == m:
            city = mapping[m]
    return city


def audit_city(data_set):
    """
    Change the string in the city category to have uniform names

    Parameters
    ----------
    data_set : DataSet
        DataSet object from where the current data will loaded and where the new data will be saved
    """

    data = data_set.get_restaurant_data()

    for row in data:
        city = row["city"]
        row["city"] = update_city_name(city, city_mapping)

    data_set.set_restaurant_data(data)


''' Audit Restaurant Type'''

restaurant_type_mapping = {
    "american (new)": "american",
    "american (traditional)": "american",
    "bbq": "barbecue",
    "delis": "delicatessen",
    "eastern european": "east european",
    "french (classic)": "french",
    "french (new)": "french",
    "steak houses": "steakhouses",
}


def print_all_restaurant_types(data_set):
    """ Print all the found types from the type category of the data set """

    data = data_set.get_restaurant_data()
    types = dict()

    for row in data:
        restaurant_type = row["type"]
        types[restaurant_type] = types.get(restaurant_type, 0) + 1

    pprint.pprint(types)


def update_type_name(restaurant_type, mapping):
    """
    Change similar restaurant types to the same type according to the mapping

    Parameters
    ----------
    restaurant_type : str
        Current restaurant type
    mapping : dict[str,str]
        Dict of the similar type names and their according same type

    Returns
    -------
    city : str
        Updated or original string of the type name
    """

    for m in mapping:
        if restaurant_type == m:
            restaurant_type = mapping[m]
    return restaurant_type


def audit_restaurant_type(data_set):
    """
    Change the string in the type category to have uniform restaurant types

    Parameters
    ----------
    data_set : DataSet
        DataSet object from where the current data will loaded and where the new data will be saved
    """

    data = data_set.get_restaurant_data()

    for row in data:
        restaurant_type = row["type"]
        row["type"] = update_type_name(restaurant_type, restaurant_type_mapping)

    data_set.set_restaurant_data(data)


''' Audit Phone Format'''

phone_format_mapping = {
    "-": "/"
}


def phone_regex(phone_number):
    """
    Regex to check whether the phone number corresponds to two specific phone formats or not

    Parameters
    ----------
    phone_number : str
        Phone number which has to be checked

    Returns
    -------
    match object
        Return match of the regex or none
    """
    pr = re.compile(r'''
         (\d{3}) # first 3 digits
         (\s|-|/) # separator
         (\d{3}) # first 3 digits
         (\s|-|/) # separator
         (\d{4}) # last 4 digits
         ''', re.VERBOSE)
    return pr.search(phone_number.replace(" ", ""))


def print_all_phone_formats(data_set):
    """ Print the first symbol of the phone format or whether it has an exception """
    data = data_set.get_restaurant_data()
    formats = dict()

    for row in data:
        phone_number = row["phone"]
        m = phone_regex(phone_number)
        if m:
            symbol = m.group(2)
            formats[symbol] = formats.get(symbol, 0) + 1
        else:
            formats["exception"] = formats.get("exception", 0) + 1

    pprint.pprint(formats)


def update_phone_format(n, mapping):
    """
    Change the symbol to the most common symbol according to the mapping

    Parameters
    ----------
    n : match object
        Match object result of the phone_regex()
    mapping : dict[str,str]
        Dict of the symbol and its replacement

    Returns
    -------
    city : String
        Updated or original string of the phone number
    """

    phone_number = n.group()
    for m in mapping:
        if n.group(2) == m:
            phone_number = n.group(1) + mapping[m] + n.group(3) + n.group(4) + n.group(5)

    return phone_number


def audit_phone_format(data_set):
    """
    Change the string in the phone category to have uniform phone format

    Parameters
    ----------
    data_set : DataSet
        DataSet object from where the current data will be loaded and where the new data will be saved
    """

    data = data_set.get_restaurant_data()

    for row in data:
        m = phone_regex(row["phone"])
        if m:
            row["phone"] = update_phone_format(m, phone_format_mapping)

    data_set.set_restaurant_data(data)
