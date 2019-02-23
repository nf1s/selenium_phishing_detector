import datetime

import whois
from urllib.parse import urlparse


def get_domain_from_uri(uri):
    """Function splits uri and gets domain

    Args:
        uri: (str) uri

    Returns:
        str: domain

    """
    domain_name = urlparse(uri).hostname.split('.')
    domain = domain_name[-2] + '.' + domain_name[-1]
    return domain


def check_whois(domain):
    """Functions performs who is check to check
        1. creation date
        2. expiration date

    Args:
        domain: (str) domain name

    Returns:
        tuple: creation date, expiration date

    """
    whois_query = whois.query(domain)
    creation_date = whois_query.creation_date
    expiration_date = whois_query.expiration_date
    return creation_date, expiration_date


def check_date_difference(cer_date, exp_date):
    """ get the difference between creation date and expiration date

    Args:
        cer_date: (datetime) domain registration date
        exp_date: (datetime) domain expiration date

    Returns:

    """
    todays_date = datetime.date.today()
    days_since_creation = (todays_date - cer_date.date()).days
    days_till_expiration = (exp_date.date() - todays_date).days
    return days_since_creation, days_till_expiration


def url_contain_symbols(url):
    """ Checking url for subdomains and chars like "-" and "@"

    Args:
        url: (str) url

    Returns:
        Tuple: (no of dots, no of dashes, no of "@"s)

    """
    dots = url.count('.')
    dashes = url.count('-')
    ats = url.count('@')
    return dots, dashes, ats


def check(url):
    """Check domain for
        1. living duration
        2. url chars like ".", "-", "@"

    Args:
        url: (str) Url

    Returns:
        int: number representing the total weight if phishing possibility

    """
    count = 0
    domain = get_domain_from_uri(url)
    try:
        cer_date, exp_date = check_whois(domain)
        cer_days, exp_days = check_date_difference(cer_date, exp_date)
        if cer_days < 365:
            count += 5
        if exp_days < 180:
            count += 2
    except:
        count = 6
    dots, dashes, ats = url_contain_symbols(url)
    if dots >= 5:
        count += 4
    if dashes > 0:
        count += 1
    if ats > 0:
        count += 3
    return count
