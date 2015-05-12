#!/usr/bin/env python

# Dovesitter is a dovecot director health checker. It tests backend 
# servers and enable/disable servers as needed.
#
# Eduardo L Ramos <eduardo@freedominterface.org>
#
### License:
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
###

import logging
import logging.config
import ConfigParser
import time
import signal
import threading
import os, sys
import signal
import getopt

import checkimap
import director

UMASK=0
WORKDIR = '/'
RUNNING = True
PIDFILE = '/var/run/dovesitter.pid'
CONFDIR = '/etc/dovesitter/'
CONFFILE = CONFDIR + './dovesitter.conf'

logging.config.fileConfig(CONFDIR + './logging.conf')
logger = logging.getLogger('dovesitter')

config = ConfigParser.ConfigParser()
config.read(CONFFILE)

def sighandler(signum, frame):
    global RUNNING
    if signum == signal.SIGTERM:
        logger.info('Signal term received')
        RUNNING = False

def writepid(pid):
    if os.path.isfile(PIDFILE):
        return False
    try:
        fp = open(PIDFILE, 'w')
        fp.write(str(pid))
    except IOError:
        return False
    return True

def daemonize():
    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)
    
    if (pid == 0):
        if not writepid(os.getpid()):
            print "Check if there is another dovesitter instance running! " + PIDFILE
            os._exit(1)
            os.setsid()
            os.chdir(WORKDIR)
            os.umask(UMASK)
        else:
            os._exit(0)
            
        try:
            si = open('/dev/null', 'r')
            so = open('/dev/null', 'a+')
            se = open('/dev/null', 'a+', 0)
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())
        except OSError:
            pass
        
        return True
    
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd', [])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    DAEMON = False
    for o, a in opts:
        if o == '-d':
            DAEMON = True
            daemonize()
        else:
            assert False, 'unhandled option'

    signal.signal(signal.SIGTERM, sighandler)
    logger.info('Starting dovesitter main thread')
    director = director.director(config.get('general', 'director_socket'))
    threads = []
    t = checkimap.checkimap(config.get('general', 'host_port'), director)
    t.start()
    threads.append(t)
    while len(threads) > 0:
        try:
            for t in threads:
                if not RUNNING:
                    t.kill_received = True
                if t is not None and t.isAlive():
                    t.join(1)
                else:
                    threads.pop(threads.index(t))
        except KeyboardInterrupt:
            print "Ctrl-c received! Sending kill to threads..."
            for t in threads:
                t.kill_received = True
    logger.info('Stopping...')
    if DAEMON:
        if(os.path.exists(PIDFILE)):
            os.remove(PIDFILE)
