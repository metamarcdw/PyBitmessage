PyBitmessage-I2P
============

This is a fork of PyBitmessage that runs natively over I2P (ONLY)
It requires a running I2P router with SAM Bridge activated.

**UPDATE: A Windows binary has been created using PyInstaller.
It has been tested and is working under Windows 8.1.
It is available from the GitHub repository at:**

https://github.com/metamarcdw/PyBitmessage-I2P/releases/

Differences from vanilla Bitmessage
----------
PyBitmessage-I2P has several important differences from vanilla Bitmessage.
Always remember _THIS IS A SEPARATE NETWORK_! PyBitmessage-I2P forms a completely
new and separate Bitmessage network inside of I2P. Since this is a new network,
the client must bootstrap by accessing an eepsite and reading a list of known nodes.
This bootstrapping process can cause delays if your I2P router is not well
integrated with the I2P network. Another important difference to take note of
is that the format for Bitmessage addresses has been changed slightly to signify
that you are seeing a BM-I2P address rather than a vanilla address.
PyBitmessage-I2P addresses start with "BM+" rather than "BM-".

If you would like to contribute to the network by running a node 24/7 for newcomers
to bootstrap from, navigate to your Network Settings dialog and send a copy of
your I2P destination string to:

BM+2cToiiYrW92SSZ3616VTgQYmSmg5bVDi8w (PyBItmessage-I2P)

BM-2cToiiYrW92SSZ3616VTgQYmSmg5bVDi8w (Vanilla Bitmessage)

----------
Bitmessage is a P2P communications protocol used to send encrypted messages to
another person or to many subscribers. It is decentralized and trustless,
meaning that you need-not inherently trust any entities like root certificate
authorities. It uses strong authentication, which means that the sender of a
message cannot be spoofed, and it aims to hide "non-content" data, like the
sender and receiver of messages, from passive eavesdroppers like those running
warrantless wiretapping programs.


Development
----------
Bitmessage is a collaborative project. You are welcome to submit pull requests 
although if you plan to put a non-trivial amount of work into coding new
features, it is recommended that you first solicit feedback on the DevTalk
pseudo-mailing list:
BM-2D9QKN4teYRvoq2fyzpiftPh9WP9qggtzh


References
----------
* [Project Website](https://bitmessage.org)
* [Protocol Specification](https://bitmessage.org/wiki/Protocol_specification)
* [Whitepaper](https://bitmessage.org/bitmessage.pdf)
* [Installation](https://bitmessage.org/wiki/Compiling_instructions)
