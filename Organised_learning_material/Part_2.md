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