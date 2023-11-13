# Role within a distributed system?

Naming is used to share resources, identify entities or locations and many other things depending on the service. A name is string of bits which refers to an entity. Entities can be anything from processes to files, printers, users, connections etc. Additionally, entities are operated through an access point which is another special entity. Name of that entity is address.

Node discovery (also resource discovery) is a technique to find available nodes or resources. Node discovery is often the first thing an application does to operate if it uses additional resources.


# Naming techniques:

## 1. Flat-naming

Entities are named with identifier which has no relation to the entity. Flat-naming lacks structure and requires other techniques to keep track of named entities for example hash tables.

## 2. Structured-naming
Entities are named with human readable names. Files and hostnames are usually named like this. Structured-naming often uses name spaces organize names. Name spaces can be organized in multiple ways but a common one is tree structure where entities are leaf nodes and their parents directory nodes.

## 3. Attribute-based naming
In attribute-based naming, entities are described with attributes. Attributes might refer to multiple entities, but this is up to the system implementation. Attribute-based naming allows wider searches and is useful when there are many entities and user do not have complete information of the entity but can describe it. These naming systems are also called directory services. Emails are an example of this. 

# Node discovery techniques

Gossip and broadcast. In gossiping, node asks for all other nodes for their local information. In broadcasting, one node shares its information with all other nodes.

# Implementation within an example project if we can find open-source code?

Not quite the same but Kubernetes has feature discovery which also seems to show whether an entity is occupied or not

https://github.com/kubernetes-sigs/node-feature-discovery
