# Gogs on Swarm

Docker Swarm description for gogs deployment. There are two components : 
 * gogs image
 * ovhdnsupdate

## OVH Dns update
I'm using OVH as my DNS provider. To ensure SSH connection on the good swarm host, I'm using a little python script relying on ovh and docker python module (installed via pip), that is also containerized.

To build it, just enter the dnsupdate folder and run the classic `docker build ...` sequence. Be sur to adapt the repository path in the stack description.