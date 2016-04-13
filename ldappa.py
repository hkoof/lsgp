#!/usr/bin/env python

import sys
import logging
import os.path

import bonsai

import prog
import logging
from config import Config

log = logging.getLogger(prog.name)

def wait_result(connection, msgid):
    i = 0
    result = None
    while result is None:
        i += 1
        result = connection.get_result(msgid)
    print ("spin wait:", i)
    return result

def main():
    conf = Config(os.path.expanduser('~/.lsgprc'))['monitor']

    client = bonsai.LDAPClient(conf['url'])
    client.set_credentials("SIMPLE", (conf['binddn'], conf['password']))

    connection = bonsai.LDAPConnection(client, is_async=True)
    msgid = connection.open()
    result = wait_result(connection, msgid)
    print ("async connection result:", result)

    msgid = connection.search('cn=Bytes,cn=Statistics,cn=monitor', 0, '', ['+'])
    result = wait_result(connection, msgid)
    print (result)
    nBytes = result[0]['monitorCounter'][0]

    msgid = connection.search('cn=Entries,cn=Statistics,cn=monitor', 0, '', ['+'])
    result = wait_result(connection, msgid)
    nEntries = result[0]['monitorCounter'][0]
    
    msgid = connection.search('cn=Total,cn=Connections,cn=monitor', 0, '', ['+'])
    result = wait_result(connection, msgid)
    totalConnections = result[0]['monitorCounter'][0]

    msgid = connection.search('cn=Current,cn=Connections,cn=monitor', 0, '', ['+'])
    result = wait_result(connection, msgid)
    currentConnections = result[0]['monitorCounter'][0]

    msgid = connection.search('cn=Max File Descriptors,cn=Connections,cn=monitor', 0, '', ['+'])
    result = wait_result(connection, msgid)
    maxDescriptors = result[0]['monitorCounter'][0]

    connection.close()

    print()
    print("Connections:")
    print("  Max descr:", maxDescriptors)
    print("  Current:", currentConnections)
    print("  Total:", totalConnections)
    print()
    print("Statistics:")
    print("  Bytes:", nBytes)
    print("  Entries:", nEntries)

if __name__ == "__main__":
    main()
