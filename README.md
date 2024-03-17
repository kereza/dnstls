# DNS to DNS-over-TLS proxy

DNS proxy that listens to conventional DNS and sends it over TLS to Cloudflare public DNS

## Description

Nowadays, some DNS providers (such as Cloudflare) offer a DNS-over-TLS feature that could let
us enhance privacy by encrypting our DNS queries. This is a python script which listens on port 53 (UDP and TCP)
and forward the queries over TLS to Cloudflare public DNS. There is also Docker file included and docker image uploaded in Dockerhub

## Getting Started

### Executing program

* If you would like to build the Dcoker image locally, clone the repo and from inside the folder run:
```
docker build -t name:tag .
```
name - the name of the image which you want to give. For example dnstls <br>
tag - the version of the image. For example 1.0

* If you would like to download the Docker image for public DockerHUb:
```
docker pull kerezov/dnstls:1.1
```

* Once one of the above steps is completed you can run the container locally:
```
docker run -d -p 127.0.0.1:53:53 -p 127.0.0.1:53:53/udp kerezov/dnstls:1.1
```
This will start the container locally and it will listen on the localhost interface on port 53 (UDP and TCP)    

* You can test if the resolving works with NSLOOKUP or DIG for example:
```
nslookup google.com 127.0.0.1

dig google.com @127.0.0.1 +tcp
```

## Considerations
### Security
* Firewall and Network Security - Use firewalls to control traffic to and from your DNS server. Ensure network security policies are in place to only allow necessary traffic on port 53 (both TCP and UDP).
* DDoS Protection - Be prepared for Distributed Denial of Service (DDoS) attacks. Consider using DDoS mitigation services or techniques if your DNS server is public-facing.
* Patching and Software Updates - Keep your DNS server software and the underlying operating system up-to-date with the latest security patches.
* Redundancy and Failover - Implement redundancy and failover mechanisms to maintain DNS availability in case of server or network failures.
### Deploy in distributed, microservices-oriented architecture
asasasas