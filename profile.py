"""
Loom (NSDI '19) Reproduction Profile
"""

import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.emulab as emulab

pc = portal.Context()

node_types = [
    ("c6320", "c6320"),
    ("c6420", "c6420"),
    ("c220g5", "c220g5"),
    ("c6620", "c6620"),
    ("r6615", "r6615"),
    ("r6525", "r6525"),
    ("c6525-25g", "c6525-25g"),
]

pc.defineParameter(
    "nodeType",
    "Node type",
    portal.ParameterType.STRING,
    node_types[0][0],
    node_types,
    "",
)

pc.defineParameter(
    "osImage",
    "Disk image",
    portal.ParameterType.IMAGE,
    "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU16-64-STD",
    longDescription=(
        ""
    ),
)

params = pc.bindParameters()

request = pc.makeRequestRSpec()

sender = request.RawPC("sender")
sender.hardware_type = params.nodeType
sender.disk_image = params.osImage
sender_iface = sender.addInterface("sender-if")

receiver = request.RawPC("receiver")
receiver.hardware_type = params.nodeType
receiver.disk_image = params.osImage
receiver_iface = receiver.addInterface("receiver-if")

# Private LAN link between the two nodes
link = request.Link(members=[sender_iface, receiver_iface])
link.bandwidth = 10000000 
link.setNoInterSwitchLink() 

pc.printRequestRSpec(request)
