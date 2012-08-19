"""
breakGFW DNS Resolver
"""
import os
from twisted.names import dns, server, client, cache
from twisted.application import service, internet

class BFWResolver(client.Resolver):
    def __init__(self, servers):
        client.Resolver.__init__(self, servers=servers)
        self.ttl = 10

    def lookupAddress(self, name, timeout = None):
        if not blocked(name):
            return chinaResolver.lookupAddress(name, timeout)
        else:
             return freeResolver.lookupAddress(name, timeout)

CONF_PATH = os.path.dirname(os.path.abspath(os.path.join(os.getcwd(), __file__)))

chinaServers = []

if os.path.exists(CONF_PATH + '/china_resolv.conf'):
    for nameserver in open(CONF_PATH + '/china_resolv.conf').readlines():
        chinaServers.append((nameserver.strip(), 53))
else:
     for nameserver in open(CONF_PATH + '/detected_resolv.conf').readlines():
        chinaServers.append((nameserver.strip(), 53))

freeServers = []
for nameserver in open(CONF_PATH + '/free_resolv.conf').readlines():
    freeServers.append((nameserver.strip(), 53))

blockDomains = []
for domain in open(CONF_PATH + '/gfw_domain.lst').readlines():
    blockDomains.append(domain.strip())

if os.path.exists(CONF_PATH + '/break_domain.lst'):
    for domain in open(CONF_PATH + '/break_domain.lst').readlines():
        blockDomains.append(domain.strip())

def blocked(name):
    parts = name.split('.')
    domains = []
    while len(parts) > 0:
        domains.append(parts.pop())
        tmp = [part for part in domains]
        tmp.reverse()
        if '.'.join(tmp) in blockDomains:
            return True

    return False

#print blockDomains

application = service.Application('dnsserver', 1, 1)

chinaResolver = client.Resolver(servers=chinaServers)
freeResolver = client.Resolver(servers=freeServers)

f = server.DNSServerFactory(caches=[cache.CacheResolver()], clients=[BFWResolver(servers=freeServers)])
p = dns.DNSDatagramProtocol(f)
f.noisy = p.noisy = False

ret = service.MultiService()

s = internet.UDPServer(53, p)
s.setServiceParent(ret)

ret.setServiceParent(service.IServiceCollection(application))

if __name__ == '__main__':
    import sys
    print "Usage: twistd -y %s" % sys.argv[0]

