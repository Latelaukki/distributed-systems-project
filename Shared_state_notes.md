# Shared State

## What is the role of a Shared distributed state?
1. Data Sharing: A shared distributed state allows multiple components or nodes in a distributed system to share data or information. This can be essential for scenarios where different parts of the system need to access or update the same data.

2. Consistency: Maintaining data consistency is a crucial role of a shared distributed state. It ensures that all participants in the distributed system see a consistent and up-to-date view of the shared data, despite concurrent access and updates.

3. Synchronization: Shared distributed states provide mechanisms for synchronization, ensuring that multiple operations on the shared data do not result in data corruption or conflicts. This can involve using locks, transactions, or other synchronization techniques.

## What specific technologies can we use to track a Shared distributed state?
1. Distributed Databases: Distributed databases like Apache Cassandra or Amazon DynamoDB can be used to store and manage game state data. They can handle the storage and retrieval of player profiles, game progress, scores, and other relevant information.
2. Real-Time Databases: Real-time databases such as Firebase Realtime Database or Firestore are designed for handling real-time updates and can be suitable for multiplayer games. They allow you to synchronize data across clients in real-time.
3. Game Servers: Multiplayer games often have dedicated game servers that manage the game state and enforce the game rules. These servers communicate with players' clients to maintain the shared state of the game world.
4. Message Queues: Message queuing systems like RabbitMQ or Apache Kafka can be used to transmit events and updates between game server instances, ensuring that changes in game state are consistently propagated to all players.

## Example projects which use a Shared distributed state

- [Building Shared State Microservices for Distributed Systems Using Kafka Streams](https://www.confluent.io/blog/building-shared-state-microservices-for-distributed-systems-using-kafka-streams/)

## Aditional resources

- [Medium: Distributed State — Challenges and Options](https://nittikkin.medium.com/distributed-state-management-80c8100bb563)

- [Stack exchange on game-state update structure and distribution in MMO](https://gamedev.stackexchange.com/questions/34798/game-state-update-structure-and-distribution-in-mmo)

- [Shared state vs message passing (distributed state)](https://slikts.github.io/concurrency-glossary/?id=shared-state-vs-message-passing-distributed-state)

- [Wikipedia on Distributed shared memory](https://en.wikipedia.org/wiki/Distributed_shared_memory)

