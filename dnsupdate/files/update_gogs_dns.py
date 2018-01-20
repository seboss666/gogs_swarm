#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Seboss666
# Script to update OVH DNS entry to identify host running gogs instance, for SSH purposes

from time import sleep
import configparser
import re
import docker
import ovh

Config = configparser.ConfigParser()
Config.read("/app/dns.ini")

DNSINFO = Config['OvhDns']
DNSURL = '/domain/zone/'+DNSINFO['Domain']+"/"
DNSURLRECORD = DNSURL+'record'
DNSSUBDOMAIN = DNSINFO['SubDomain']
DNSSUBDOMAINURL = DNSURLRECORD+"/"+DNSSUBDOMAIN

dns = ovh.Client()
dock = docker.from_env()

#Retrieve IP from OVH DNS entry
def getsubdomainip(subdomain):
	subDomainInfo = dns.get(DNSURLRECORD, fieldType='A', subDomain=subdomain,)
	subDomainInfo = (str(subDomainInfo).replace('[','').replace(']',''))

	currentHost = dns.get(DNSURLRECORD+'/'+subDomainInfo)
	currentHostIP = currentHost['target']

	return currentHostIP

#Update OVH DNS entry with new IP
def updatesubdomainip(subdomain,ip):
	subDomainInfo = dns.get(DNSURLRECORD, fieldType='A', subDomain=subdomain,)
	subDomainInfo = (str(subDomainInfo).replace('[','').replace(']',''))
	dnsUpdate = dns.put(DNSURLRECORD+'/'+subDomainInfo, target=ip, ttl=60, subDomain=subdomain,)	
	result = dns.post(DNSURL+'refresh')
	return result

# Default main
if __name__ == "__main__":

#	while True:

		currentIP = getsubdomainip(DNSSUBDOMAIN)

		print("IP actuelle : ", currentIP)

		servs = dock.services.list()
		servList = []
		for serv in servs:
			servList.append(serv.name)

		#I'm usig the subdomain as base for service discovery
		servMatch = re.compile(".*"+DNSSUBDOMAIN)

		for serv in servList:
			if servMatch.match(serv):
				servName = servMatch.match(serv).group(0)

		newHost = dock.nodes.get(dock.services.get(servName).tasks(filters={'desired-state': 'running',})[0]['NodeID']).attrs['Description']['Hostname']	

		print("Hôte en cours d'exécution : ", newHost)

		newHostIP = getsubdomainip(newHost)

		#Update DNS if host changed
		if newHostIP != currentIP:
			print("Nouvelle IP : ", newHostIP)
			updatesubdomainip(DNSSUBDOMAIN,newHostIP)
			print("Zone DNS mise à jour")

#		sleep(60)
