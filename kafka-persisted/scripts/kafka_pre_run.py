#! /usr/bin/env python

import os, re, sys, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kafka_pre_run")

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "/tmp/server.properties"

zookeperconnect = ""
# search for Kubernetes services environment variable with host and port 
# (<servicename>_SERVICE_HOST and <servicename>_SERVICE_PORT)
for key in os.environ.keys():
    matchobj = re.match("ZOOKEEPER([0-9]*)_SERVICE_HOST", key, re.M|re.I)
    if matchobj:
        # env variable name ZOOKEEPER<serverid>_SERVICE_HOST
        envhost = matchobj.group()
        # get the serverid
        serverid = matchobj.group(1)
        # env variable name ZOOKEEPER<serverid>_SERVICE_PORT
        envport = "ZOOKEEPER{0}_SERVICE_PORT".format(serverid)
        
        logger.info("%s = %s", key, os.environ[key])
        logger.info("%s = %s", envport, os.environ[envport])
        
        # append to zookeeper.connect parameter string for Kafka
        zookeperconnect += "{0}:{1},".format(os.environ[key], os.environ[envport])        
        
# remove last ',' character
zookeperconnect = zookeperconnect.strip(',')

# append Zookeeper connect paramater at the end of configuration file
f = open(filename, "a");
f.write("zookeeper.connect={0}".format(zookeperconnect))
f.close()

print zookeperconnect

