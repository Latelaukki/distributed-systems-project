# Design plan (Alexaner Engelhardt)

## Names of team members and one paragraph of the selected topic
We are planning to create a multiplayer game as a simple distributed system. The game will be a simple dungeon crawler where players' goal is to escape the dungeon as quickly as possible. Players are put in different instances and when each player has completed the run (or time runs out??) the player with the quickest time wins the game.

## More detailed description of the topic + selected solutions
The dungeons where players find themselves in are split into several regions. Each region will be handled by a dedicated gameserver. In practice this will mean that player-character information will be transfered from one server to another when a player moves from one region to another. The communication between servers is going to be asynchronous.
To guarantee consistency a total ordering of events will be achieved through vector clocks.

## Description of the different nodes
As stated earlier different regions will be handled by different nodes. They will certainly share alot of logic, but we may have to come up with some uniqueness to underline some differneces as well.

## Description of messages send and received by the nodes (syntax and semantics)
The messages between nodes will consist of player data, like gear, level, etc. This data can be transferred from one node to another using some standard data format like JSON. 

## Scalability and Load Balancing
To achieve scalability and load balancing we can use a Load Balancer to apply Horizontal Duplication on those nodes that experience high amount of traffic.

## Fault Tolerance
We can replicate player data and keep backup servers incase some node crashes.
