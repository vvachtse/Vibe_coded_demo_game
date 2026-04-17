# Preparation and getting started (LO1)

The initial process is to properly identify the initial requirements for our game to function as intented. We try to use a well defined initial prompt to request and generate the initial demo, however in order to properly phrase the prompt we must try to anticipate what the LLM will understand. Using keywords that connotate to specific brands and quirks helps the LLM better identify what in theory should be included. This can be very clear if we initially request the functionality that the game should have and then start with the code generation and compilation. 

For our educational framework we will try to identify two similar mechanically games. Final Fantasy and Pokemon. Both games share a lot of similarities however the ones we care more about are the following : 

1. free roaming around a predetermined map
2. random encounters within areas of the predetermined map
3. there is combat system that is turn based
4. party management and use of party within combat
5. menu
6. inventory management
7. npc and interactions

Those 7 are the basic functions we wish of our demo to be able to properly showcase. There are many other common aspects but we will return to those later. One last thing we need to remember is that for a complete game , graphical assets (like sprites) need to be generated. This in itself is a big problem when working solely using an LLM. Unless you are using a paid model with unlimited resource generation , using sprites will become the last priority of the demo and we will generate low quality ones.

One more detail that is interesting is the ability to move from one map to another without problems. This is something that we should also try to implement in the LLM generated demo as it will help us understand better some functions that are affecting the enviroment and not the characters. More enviromental processes can be added ( like toll house, switches etc) but the initial philosphy design is to create the a basic object, which we will enrich in the future.

An exemplary map of what we want to recreate (crudely) from the initial version.

```
                           +-----------------------------+
                           |         GAME ENGINE         |
                           +-----------------------------+
                                      |
                                      |
        +-------------------------------------------------------------+
        |                         ENVIRONMENT                         |
        |                 (World where gameplay occurs)               |
        +-------------------------------------------------------------+
        |                                                             |
        |   +------------------+      +----------------------------+  |
        |   | STATIC OBJECTS   |      |        DYNAMIC OBJECTS     |  |
        |   | (Environment)    |      |            (NPCs)          |  |
        |   +------------------+      +----------------------------+  |
        |   | - Trees          |      | - Villagers                |  |
        |   | - Rocks          |      | - Monsters                 |  |
        |   | - Buildings      |      | - Merchants                |  |
        |   | - Terrain Tiles  |      | - Quest Givers             |  |
        |   +------------------+      +----------------------------+  |
        |                                                             |
        |                     +---------------------+                 |
        |                     |   CHARACTER OBJECT  |                 |
        |                     |   (Player Avatar)   |                 |
        |                     +---------------------+                 |
        |                     | - Position in world |                 |
        |                     | - Stats             |                 |
        |                     | - State             |                 |
        |                     +---------------------+                 |
        +-------------------------------------------------------------+
                                      |
                                      |
        +-------------------------------------------------------------+
        |                        OUTSIDE ENVIRONMENT                  |
        |               (Systems not physically in the world)         |
        +-------------------------------------------------------------+
        |                                                             |
        |   +------------------+     +-----------------------------+  |
        |   |    INVENTORY     |     |      PARTY DICTIONARY       |  |
        |   +------------------+     +-----------------------------+  |
        |   | - Items          |     | - Allies                    |  |
        |   | - Equipment      |     | - Summons                   |  |
        |   | - Consumables    |     | - Followers                 |  |
        |   +------------------+     +-----------------------------+  |
        |                                                             |
        |                     +---------------------+                 |
        |                     | HERO / CREATURES    |                 |
        |                     | (Data Objects)       |                 |
        |                     +---------------------+                 |
        |                     | - Stats             |                 |
        |                     | - Abilities         |                 |
        |                     | - Metadata          |                 |
        |                     +---------------------+                 |
        +-------------------------------------------------------------+


```