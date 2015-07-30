# Dovesitter

**Dovesitter** is a dovecot director health checker.
It tests IMAP backend servers and enable/disable servers as needed.

In order to test, it sends a TCP/SYN package to IMAP port and waits for a TCP/SYN+ACK response.

## Configure and run

* Create the directory **/opt/dovesitter**
* Copy all \*.py to **/opt/dovesitter**
* Create the directory **/etc/dovesitter**
* Copy all \*.conf to **/etc/dovesitter**

If you use RHEL/CentOS 7.x or another distro with systemd:

* Copy **dovesitter.service** to **/etc/systemd/system/**
* Reload systemd with **systemctl daemon-reload**
* Enable and run **dovesitter** with **systemctl enable dovesitter.service && systemctl start dovesitter.service**

## Licence

Copyright (c) 2015 Eduardo Ramos (ramos.eduardo87@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
