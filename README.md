# Dovesitter

**Dovesitter** is a dovecot director health checker.
It tests IMAP backend servers and enable/disable servers as needed.

In order to test, it sends a TCP/SYN package to IMAP port and waits for a TCP/SYN+ACK response.

## Licence

Copyright (c) 2015 Eduardo L. Ramos (eduardo at freedominterface dot org)

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2, or (at your option) any
later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
