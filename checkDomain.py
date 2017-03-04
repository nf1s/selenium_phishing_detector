from urllib.parse import urlparse
import socket
from dns import resolver
import whois
import datetime

# Get domain from URI
def get_domain_from_uri(uri):

    domain_name = urlparse(uri).hostname.split('.')
    domain = domain_name[-2] +'.'+ domain_name[-1]
    return domain

# resolve Ip from domain by querying the local Dns
def get_ips_for_host(host):

    ip_list = []
    try:
        ips = socket.gethostbyname_ex(host)
        ip_list = ips[2]
        ip_list.sort()
        print(ip_list)
    except socket.gaierror:
       print('error')
    return ip_list

# Query google open dns to get ip of the same domain
def get_Info_from_googleOpenDns(domain):
    res = resolver.Resolver()
    res.nameservers = ['8.8.8.8']
    answers = res.query(domain)

    index = 0
    ip_list = []

    for rdata in answers:
        ip_list.append(rdata.address)
        ip_list.sort()

    print(ip_list)
    return ip_list

def check_whois(domain):
    whois_query = whois.query(domain)
    creation_date = whois_query.creation_date
    expiration_date = whois_query.expiration_date
    return creation_date,expiration_date

def check_date_difference(cer_date,exp_date):

    todays_date = datetime.date.today()
    days_since_creation = (todays_date - cer_date.date()).days
    days_till_expiration = (exp_date.date() -todays_date).days
    print(days_since_creation)
    print(days_till_expiration)

#
# def run(uri):
#     domain = get_domain_from_uri(uri)
#     print(domain)
#     creation_date,expiration_date = check_whois(domain)
#     check_date_difference(creation_date,expiration_date)
#     ip_local = get_ips_for_host(domain)
#     ip_google_dns = get_Info_from_googleOpenDns(domain)
#
#     if ip_local == ip_google_dns:
#         print('domain match')
#     else:
#         print('Domain mismatch')
#
#
# run('http://www.facebook.com')
