from berserker_resolver import Resolver
resolver = Resolver()

result = resolver.query('google.com')
print(list(result)) # [<DNS IN A rdata: 173.252.120.6>]

# Query to the local dns.
result = resolver.query('google.com', '127.0.0.1')
print(list(result)) # [<DNS IN A rdata: 173.252.120.6>]