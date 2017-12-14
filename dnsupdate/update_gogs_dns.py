#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script to update OVH DNS entry to identify host running gogs instance, for SSH purposes

#import json
#import subprocess
import time
import configparser
import re
import docker
import ovh

Config = configparser.ConfigParser()
Config.read("./dns.ini")

dnsInfo = Config['OvhDns']
dnsUrl = '/domain/zone/'+dnsInfo['Domain']+"/"
dnsUrlRecord = dnsUrl+'record'
dnsSubDomain = dnsInfo['SubDomain']
dnsSubDomainUrl = dnsUrlRecord+"/"+dnsSubDomain

client = ovh.Client()
dock = docker.from_env()

while True:

	subDomainCurrent = client.get(dnsUrlRecord, fieldType='A', subDomain=dnsSubDomain,)

	subDomainCurrent = (str(subDomainCurrent).replace('[','').replace(']',''))

	currentHost = client.get(dnsUrlRecord+'/'+subDomainCurrent)

	currentHostIP = currentHost['target']

	print(currentHostIP)

	servs = dock.services.list()
	servList = []
	for serv in servs:
		servList.append(serv.name)

	#Le service doit matcher le sous-domaine
	servMatch = re.compile(".*"+dnsSubDomain)

	for serv in servList:
		if servMatch.match(serv):
			servName = servMatch.match(serv).group(0)

	newHost = dock.nodes.get(dock.services.get(servName).tasks(filters={'desired-state': 'running',})[0]['NodeID']).attrs['Description']['Hostname']	

	print(newHost)

	subDomainNew = client.get(dnsUrlRecord, fieldType='A', subDomain=newHost,)

	subDomainNew = (str(subDomainNew).replace('[','').replace(']',''))

	newHostDns = client.get(dnsUrlRecord+'/'+subDomainNew)

	print(newHostDns['target'])

	# if hostList[newHost] != currentHostIP:
	# 	dnsUpdate = client.put('/domain/zone/seboss666.ovh/record/1439796959', target=hostList[newHost], ttl=60, subDomain='gogs',)
	# 	print(dnsUpdate)

	# 	result = client.post('/domain/zone/seboss666.ovh/refresh')
	# 	print(result)
	time.sleep(60)
