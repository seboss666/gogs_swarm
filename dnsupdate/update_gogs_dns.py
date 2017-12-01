#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script to update OVH DNS entry to identify host running gogs instance, for SSH purposes

import ovh
import json
import subprocess
import time

client = ovh.Client()

while True:

	currentHost = client.get('/domain/zone/seboss666.ovh/record/1439796959')

	currentHostIP = currentHost['target']

	print(currentHostIP)

	#A remplacer par le module docker si y'a moyen de le faire fonctionner un jour
	newHost=subprocess.check_output("/usr/bin/docker service ps gs_gogs --format={{.Node}}", stderr=subprocess.STDOUT, shell=True).strip().decode("utf-8")
	print(newHost)

	hostList = { 'swarm1':"192.168.1.11", 'swarm2': "192.168.1.43", 'swarmleader':"192.168.1.9" }

	if hostList[newHost] != currentHostIP:
		dnsUpdate = client.put('/domain/zone/seboss666.ovh/record/1439796959', 
			target=hostList[newHost], # Resource record target (type: string)
			ttl=60, # Resource record ttl (type: long)
			subDomain='gogs', # Resource record subdomain (type: string)
		)
		print(dnsUpdate)

		result = client.post('/domain/zone/seboss666.ovh/refresh')
		print(result)
	time.sleep(60)
