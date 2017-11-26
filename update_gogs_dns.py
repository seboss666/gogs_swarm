#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script to update OVH DNS entry to identify host running gogs instance, for SSH purposes

import ovh
import json
import os

client = ovh.Client()

currentHost = client.get('/domain/zone/seboss666.ovh/record/1439796959')

currentHostIP=currentHost['target']

print(currentHostIP)

#A remplacer par le module docker si y'a moyen de le faire fonctionner un jour
newHost=os.system('docker service ps gogs --format={{.Node}}')

print(newHost)


# result = client.put('/domain/zone/seboss666.ovh/record/1439796959', 
#     target='192.168.1.25', // Resource record target (type: string)
#     ttl=60, // Resource record ttl (type: long)
#     subDomain='gogs', // Resource record subdomain (type: string)
# )


#result = client.post('/domain/zone/seboss666.ovh/refresh')