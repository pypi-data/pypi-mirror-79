## NSXEZ

NSXEZ is a Python library to remotely manage/automate NSX-T platforms. The user is NOT required to be a Software Programmer, or have sophisticated knowledge of NSX-T environments, or have a complex understanding of the NSX-T REST API. It does however expect that someone has built a functional NSX-T environment which includes a functional Tier-0 router and potentially edge gatway services and VNI pool for VRF examples...if you expect to have any decent functionality. This is very much a work in progress and being updated daily at this stage. 

The module will aim to provide functions of SET, DEL and GET for various API calls into the NSX-T manager, using common industry terminology. For example to read the routing table would be get_route_table() while creating an EVPN instance would be set_routing_instance(). As these are created an ongoing list of commands would/should be maintained. 


## Installation

Installation requires Python 2.7 or 3.X and the associated python pip tool. The only other requirements currently as the requests and uuid libraries which are installed automatically through pip. To install NSXEZ simply use the following command from your shell, provided pip is installed and operational. 

`
pip install nsxez
`

## Upgrade

Upgrading has the same requirements as installation and has the same format for install with the addition of -U 

`
pip install -U nsxez
`

## Inital usage

Teh library operates on a preexisting Tier0 router and when initiated it expects you to pass a valid NSX-T manager IP address, username, password and Tier0 router name. All ongoing operations are performed against this Tier0 router enviornment. 

```python
from nsxez import operations as nsx
dev = nsx.device("192.168.0.22","admin","VMware1!VMware1!","Peering")
```

Example creating a new VRF called "Blue". Values to be passed are the name of the VRF, the Route Target (used for import and export) as well as the unique route distinguisher and the VNI for VXLAN overlay from the edge node to the peer. 

```python
from nsxez import operations as nsx
dev = nsx.device("192.168.0.22","admin","VMware1!VMware1!","Peering")
dev.set_routing_instance("Blue","65000:7001","7001","79423")
```

Example output creating a new network segment called "Blue_Web_Servers" and attaching to existing VRF "Blue"

```python
from nsxez import operations as nsx
dev = nsx.device("192.168.0.22","admin","VMware1!VMware1!","Peering")
dev.set_network("Blue_Web_Servers","192.168.123.1","24","Blue","Overlay_TZ")
```

Example of assigning a routing distribution policy to an existing VRF instance. Currently only supports the concept of "all routes". 

```python
from nsxez import operations as nsx
dev = nsx.device("192.168.0.22","admin","VMware1!VMware1!","Peering")
dev.set_route_policy("ALL","Blue","all")
```

Example output gathering EVPN routing instance details (VRF attached to a Tier0) for VRF "Blue"

```python
from nsxez import operations as nsx
dev = nsx.device("192.168.0.22","admin","VMware1!VMware1!","Peering")
dev.get_routing_instance("Blue")
```
