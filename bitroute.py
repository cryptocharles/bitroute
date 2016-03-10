#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import shutil
import subprocess
import sys

__all__ = ["bitroute"]


def is_compatible():
    """ Checks whether the current machine is capable of running bitroute

    Returns:
        bool: True if the machine is compatible false if not.

    """
    # check for Windows
    if hasattr(sys, 'getwindowsversion'):
        print('error: Windows is currently not supported.')
        return False

    # check for command presence
    if not shutil.which('traceroute'):
        print('error: Missing `traceroute` binary.')
        return False

    return True


def get_server_info():
    """Gets network metadata for the machine calling the function.

    see http://ipinfo.io for more info.
    Returns:
        dict: A dictionary with keys ip, hostname, city, region, country, loc, org, postal

    """
    uri = 'http://ipinfo.io'
    raw = requests.get(uri)
    data = raw.json()
    return data


def bitroute(url):
    """ runs traceroute against the url.

    Args:
        url (str): A url to run traceroute against.

    Raises:
        ValueError: if the url is malformed or traceroute cannot be performed on it.
    Returns:
        dict: A dictionary containing traceroute information.

    """
    if not is_compatible():
        return

    uri = url.replace('https://', '').replace('http://', '')
    try:
        out = subprocess.check_output(['traceroute', str(uri)]).decode('unicode_escape')
    except subprocess.CalledProcessError:
        raise ValueError("traceroute cannot be performed on url={}".format(uri))
    res = [line for line in out.split('\n') if line != '']
    info = {
        'traceroute': res,
        'server': get_server_info()
    }
    return info


if __name__ == '__main__':
    url = sys.argv[1]
    data = bitroute(url)
    formatted_data = json.dumps(data, indent=4, sort_keys=True)
    print(formatted_data)
