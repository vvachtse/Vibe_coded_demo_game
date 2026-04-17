# Vibe_coded_demo_game
This repository includes a small game inspired by the original Pokemon and Final Fantasy games. The whole demo for the game is made using vibe coding. The aim is to showcase how to interact with LLMs/Agents (Henceforth shorthanded as simply LLMs) and perform prompt engineering in order to learn through experience how to start up with video game design.

# Status
Monthly updates

Updates planned for May : 
1. Add the analysis materials
2. Finish Part_3.md

Updates planned for June : 
-> Optimise the Pygame version

# Tools_used 
- Copilot & ChatGPT
- Microsoft edge ( ideally you want to try multiple browsers)
- Visual Studio Code

# Creative_process

Using Copilot (Smart mode) / ChatGPT we initially request from the LLM to design a prompt for an LLM to generate code for a Pokemon/FF like small game that runs on the browser. It is important to specify some requests. 

- Use 8-bit graphics and sprites
- Make the enviroment interactible
- Add menus
- Generate buildings and NPC

After reaching a desired result you can do the following: 

A. Generate a guide for the demo 
B. Ask the LLM to comment on the code
C. Ask a different LLM to explain the code

Ideally one should do all 3 in order to better understand the philosophy behind OOP for game development. You may then try to tinker with those values in order to make changes to the outcome of the game (for example change the random encounter frequency).  It is strongly advised that once the code generated exceeds the limits of messages it would be the ideal point to "translate" the code into Unity/Unreal Engine / Pygames or any other game development tool/language in order to be able to work with it extensively, as most adjustments by LLMs will be focused on specific aspects of the code only. 

> ! IMPORTANT ! 

When the LLM starts to provide you the code in chunks it means that it is nearing its capabilities therefore form that point on you should start hybrid code development.

# The Next Steps

After translating the html code into a different tool, use your prefered IDE and start fleshing out your own games. This small repo is purely for educaticational purposes.

# Generating the Pygame version

The first generation of pygames code seems a lot like a downgrade for the initial version of the demo. This is because the LLM is always trying to cut corners for the most complex codes. We will need to once again probe it to enrich the initial seed version to partly match the capabilities of the HTML version ( or code it ourselves - more ethical !)

