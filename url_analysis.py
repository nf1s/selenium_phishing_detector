from urllib.parse import urlparse
import whois
import datetime


def get_domain_from_uri(uri):

    domain_name = urlparse(uri).hostname.split('.')
    domain = domain_name[-2] +'.'+ domain_name[-1]
    return domain


def check_whois(domain):
    whois_query = whois.query(domain)
    creation_date = whois_query.creation_date
    expiration_date = whois_query.expiration_date
    return creation_date,expiration_date

def check_date_difference(cer_date,exp_date):

    todays_date = datetime.date.today()
    days_since_creation = (todays_date - cer_date.date()).days
    days_till_expiration = (exp_date.date() -todays_date).days
    return days_since_creation,days_till_expiration

def url_contain_symbols(url):
    dots = url.count('.')
    dashes = url.count('-')
    ats = url.count('@')
    return dots, dashes, ats


def check(url):
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
    dots,dashes,ats = url_contain_symbols(url)
    if dots >= 5:
        count +=4
    if dashes > 0:
        count +=1
    if ats > 0:
        count += 3
    return count
