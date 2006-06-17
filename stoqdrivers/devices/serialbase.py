# -*- Mode: Python; coding: iso-8859-1 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Stoqdrivers
## Copyright (C) 2005,2006 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
## USA.
##
## Author(s):   Johan Dahlin     <jdahlin@async.com.br>
##              Henrique Romano  <henrique@async.com.br>
##

from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
from zope.interface import implements

from stoqdrivers.log import Logger
from stoqdrivers.devices.interfaces import ISerialPort

class SerialPort(Serial):
    implements(ISerialPort)

    def __init__(self, device):
        Serial.__init__(self, device)
        self.setDTR(True)
        self.flushInput()
        self.flushOutput()
        self.set_options()

    def set_options(self, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE,
                    stopbits=STOPBITS_ONE, read_timeout=3, write_timeout=0):
        self.setBaudrate(baudrate)
        self.setByteSize(bytesize)
        self.setParity(parity)
        self.setStopbits(stopbits)
        self.setTimeout(read_timeout)
        self.setWriteTimeout(write_timeout)

class SerialBase(Logger):
    log_domain = 'serial'

    # All commands will have this prefixed
    CMD_PREFIX = '\x1b'
    CMD_SUFFIX = ''

    # used by readline()
    EOL_DELIMIT = '\r'

    def __init__(self, port):
        Logger.__init__(self)
        self._port = port

    def set_port(self, port):
        self._port = port

    def get_port(self):
        return self._port

    def writeline(self, data):
        self.write(self.CMD_PREFIX + data + self.CMD_SUFFIX)
        return self.readline()

    def write(self, data):
        self.debug(">>> %r (%d bytes)" % (data, len(data)))
        self._port.write(data)

    def read(self, n_bytes):
        return self._port.read(n_bytes)

    def readline(self):
        out = ''
        while True:
            c = self._port.read(1)
            if c == self.EOL_DELIMIT:
                self.debug('<<< %r' % out)
                return out
            out += c
