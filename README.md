#This repository contains the proposal for combining Security Chaos Engineering into a Breach and Attack Simulation platform.

The initial version, used for the paper found on https://arxiv.org/abs/2508.03882 is currently archived as a standalone release, with tag 1.0.0.

The BAS platform chosen is MITRE Caldera, both branches, 4.2 and 5.3, work, as the API remains the same between them. For use with other platforms, modifications should be done.

A target machine should be virtualized, sharing network access with the machine on which MITRE Caldera is deployed.
###In order to run this proposal, several parameters have to be defined within secrets.py.
- "url" referencing the MITRE Caldera access point, includin the port in the form of 'http://IP_ADDRESS:PORT'.
- "auth" being the API session token found in the cookie obtained when logging in the web server of Caldera.
- "victim_ip" being the address of the machine selected to run simulations on.

Once these parameters are defined, a graph can be consumed from the same directory as the main file, and the simulations can proceed following the behavior defined in said graph.
This graph expects to follow a certain JSON schema, as the one found on the example.
