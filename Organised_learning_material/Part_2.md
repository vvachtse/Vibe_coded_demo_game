# Generating the initial game (HTML) (LO2)

# HTML and JS

> Why should we use HTML/JS ?

The choice for HTML/JS is one made purely out of convinience. An LLM is more capable of generating and maintaining code in HTML due to the language's relative simplicity. Asking the LLM you want to use the question will provide you with extensive reasoning behind the benefits of designing a game demo on HTML/JS, however we will focus on the following benefits :

```

+-----------------------------+-----------------------------------------------+
| Simplicity                  | HTML is deterministic, easy to parse, and     |
|                             | easy for LLMs to generate without errors.     |
+-----------------------------+-----------------------------------------------+
| No Build Tools Needed       | Runs instantly in a browser—no compilers,     |
|                             | engines, SDKs, or dependencies required.      |
+-----------------------------+-----------------------------------------------+
| Instant Execution           | Just open index.html; perfect for rapid       |
|                             | iteration and debugging.                      |
+-----------------------------+-----------------------------------------------+
| Strong JS Integration       | HTML pairs naturally with JavaScript, which   |
|                             | LLMs can generate reliably for logic, input,  |
|                             | animation, and rendering.                     |
+-----------------------------+-----------------------------------------------+
| Canvas API Power            | Provides enough rendering capability for      |
|                             | 2D demos, sprites, animation loops, and UI.   |
+-----------------------------+-----------------------------------------------+
| Universal Compatibility     | Works on any browser, OS, or device without   |
|                             | installation—easy to share demos.             |
+-----------------------------+-----------------------------------------------+
| LLM Training Bias           | LLMs are heavily trained on HTML/JS, so       |
|                             | output quality is higher and more reliable.   |
+-----------------------------+-----------------------------------------------+
| Error Tolerance             | Browsers load partial or imperfect HTML,      |
|                             | making debugging and regeneration easier.     |
+-----------------------------+-----------------------------------------------+


```

Let's dive deeper to some of the benefits of using HTML/JS :

> Simplicity 

This simplicity dramatically increases the likelihood that an LLM will produce valid, functional output on the first attempt.  Two additional benefits is that the nature of HTML ( declarative, not procedural, which means that there’s no complex control flow for the LLM to get wrong. ) and it's relationship with browser allows for less optimal code to function as inteded . 

> No Build Tools Needed 

Most game engines or frameworks require compilers, SDKs, package managers, asset pipelines and project scaffolding . However for HTML the browser serves as the runtime environment. This removes friction and makes the LLM → test → refine loop extremely fast.

> Strong JS Integration

One of the strong elements of LLMs is the ability to generate event listeners, state machines, simple physics, input handling and DOM manipulation . 

# Generation of the first demo

Having clarified the benefits of using HTML/JS for the initial generation of the demo some thing become apparent. 
- We won't learn about complex structures
- We won't be able to create complex processes
- The initial code might be sub-par
- It will be difficult to translate to a different language/enviroment due to the declaratice nature of HTML

Those issues will be more in depth tackled during  Part 3, when we will focus on LO3 and LO4.

The initial part of this step is requesting from the LLM to generate the initial code, based on our well defined initial prompt. 

After generating the initial HTML code, we will generate an HTML file and run it. The process after generating it is the following : 

1. We test all functions that we requested
2. We assess their functionality
3. We request from the LLM to amend them 

When doing so, the LLMs in order to reduce the usege of tokens, will most probably try to amend only the relevant code. This is a great opportunity for us to slowly start understanding the different objects generated and the functions they represent.

Let's see for example the given demo we have. It is impossible to return to the initial map after you depart. Asking CGPT to solve this issue it points out that problem lies in the following objects : 

``` {id:'door_forest', x:18, y:6, type:'door', meta:{to:'forest', x:2, y:2}} ```

and specifically the event (function) 

```
'door_forest':[
  {type:'dialog', text:"You step through the gate..."},
  {type:'teleport', map:'forest', x:2, y:2}
]

```

By studying those two snippets we can infer the following :

A. We see how an enviroment object (door) is proped up
B. We see how we may add to the door object text, that appears when the teleport event takes place 

The LLM suggests to add a similar object on the forest map in order to solve our problem. The second suggestion is t upgrade the general architecture of the maps and the teleport process by importing both doors with a dictionary :

```

const mapObjects = {
  town: [
    {id:'door_forest', x:18, y:6, type:'door', meta:{to:'forest', x:2, y:2}}
  ],
  forest: [
    {id:'door_town', x:2, y:2, type:'door', meta:{to:'town', x:18, y:6}}
  ]
};

```

and 

```

function loadMap(mapName, spawnX, spawnY){
  if(!maps[mapName]) return;

  map.name = maps[mapName].name;
  map.width = maps[mapName].width;
  map.height = maps[mapName].height;
  map.tiles = JSON.parse(JSON.stringify(maps[mapName].tiles));

  objects = mapObjects[mapName] || [];

  player.map = mapName;
  player.px = spawnX;
  player.py = spawnY;
  player.tx = spawnX;
  player.ty = spawnY;
}

```

Those more extensive fixes give us a better insight on the manner the map objects are functioning. This allows for us to start to read different parts of the code and start to understand their structure. 

There are 2 interesting steps to take now. The first is to request for a visualisation of the different classes/objects/events that the code outlines. We will also request from the LLM to extensively comment on the code it has generated.

For example here we have one of the UML charts designed by the LLM in ordeer to explain the code's philosphy and how the objects within it interact. 

```

+-------------------+
|      Game         |
+-------------------+
| player            |
| map               |
| objects[]         |
| events{}          |
| party[]           |
| inventory{}       |
| PC[]              |
| battle            |
+-------------------+
| update()          |
| draw()            |
| handleInput()     |
+-------------------+
         |
         | uses
         v
+-------------------+
|      Player       |
+-------------------+
| map               |
| px, py            |
| tx, ty            |
| dir               |
| moving            |
| frame             |
| speed             |
| hp, maxHp         |
+-------------------+
| requestMove()     |
| interact()        |
+-------------------+

         |
         | interacts with
         v

+-------------------+
|       Map         |
+-------------------+
| name              |
| width, height     |
| tiles[][]         |
+-------------------+
| loadMap()         |
+-------------------+

         |
         | contains
         v

+-------------------+
|      Object       |
+-------------------+
| id                |
| x, y              |
| type              |
| meta{}            |
+-------------------+
| (npc, door, shop) |
+-------------------+

         |
         | triggers
         v

+-------------------+
|      Event        |
+-------------------+
| type              |
| text              |
| map, x, y         |
| code              |
+-------------------+
| runEventsFor()    |
+-------------------+

```

As we can see the game centers around the player object. The player objects interacts with the enviroment and interacts with different enviroment objects, triggering events. The non visual aspects like party, inventory , menus etc are elements that appear to exist within the set up but do not appear to be monitored when not in use. This is both a way for the game to reduce memory required for it to run, but also it is endemic to the enviroment. For a game oriented enviroment, monitoring those values (not necessarily having them loaded all the time) could be beneficial if we want to include special events, animations etc. However this level of sophistication will be studied later.

# Requesting comments for a large html file

This will strain the LLM a lot. It is suggested to request the commenting for the initial creation. This will allow for us to study the different pieces of code faster and for simpler structures. After an in-depth study of the code generated we will start to slowly request for the implementation of the required featured, as outlined from the design documentation. We must ensure that the features are introduced in a way that both ensures the functionality of the whole programme, but also we must be carefull to read well the suggested additions and changes. It is strongly suggested to keep notes for call backs and to remember some key aspects (for example map objects and NPC so far are treated as the same type of object, something that in the future we aim to change).

# Outcomes

At the end of this part we must have a functioning html file which showcases most (approx 70%) functionality of the features we have designed. We should also have our personal notes and diagrammes on the functionality of the code and object relations as well as a guide for the game generated by the LLM. Generating a guide is important in order for us to find where the LLM has missed it's mark and where not