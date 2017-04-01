from urllib.parse import urlparse
import socket
from dns import resolver
import whois
import datetime
import json
# Get domain from URI
from influxdb import InfluxDBClient

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



def get_phishing_pages():

    jsonFile = open('scraper/links-old.json', 'r')
    data = json.load(jsonFile)
    jsonFile.close()

    link_array = []

    for index in data:
        link_array.append(index['url'])

    print(len(link_array))
    return link_array


def get_legit_pages():
    text_file = open("scraper/file.txt", "r")
    lines = text_file.read().split('\n')
    domains = []
    for line in lines:
        domains.append(line.replace(" ", ""))

    return domains

def to_influx_database(url, res):
    if res == 1:
        result = "phishing"
    else:
        result = "legitimate"


    points = [

        {
            "measurement": result,
            "tags": {
                "browser": "firefox"
            },
            "fields": {
                "url": url
            }
        }

    ]

    try:
        db_client = InfluxDBClient('localhost', '8086',
                                   'root', 'root', 'dns_module')
        db_client.create_database('dns_module')
        db_client.write_points(points)

    except IOError as error:
        print(str(error))



def start():

    # domains = get_legit_pages()
    urls = get_phishing_pages()
    for url in urls:
        try:
            domain = get_domain_from_uri(url)
            print(domain)
            # creation_date,expiration_date = check_whois(domain)
            # check_date_difference(creation_date,expiration_date)
            ip_local = get_ips_for_host(domain)
            ip_google_dns = get_Info_from_googleOpenDns(domain)
            if ip_local == ip_google_dns:
                print('domain match')
                to_influx_database(domain,0)
            else:
                print('Domain mismatch')
                to_influx_database(domain,1)
        except:
            continue


start()

# run('http://www.facebook.com')
