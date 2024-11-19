
D&D Bot README

This bot is designed to help you quickly look up monsters and spells from the Dungeons & Dragons 5th Edition (D&D 5e) using the Open5e API. Follow the instructions below to set up and use the bot.

---

Features
- Monster Lookup: Search for D&D monsters by name and view detailed information.
- Spell Lookup: Search for D&D spells by name and view descriptions, casting details, and more.

---

Setup Instructions

Prerequisites
- Python: Install Python 3.8 or later.
- Dependencies: Install the required Python libraries:
  pip install discord requests

Configuration
1. Obtain a Discord Bot Token:
   - Go to the Discord Developer Portal (https://discord.com/developers/applications).
   - Create a new application, add a bot, and copy the bot token.
2. Add the Bot to a Server:
   - Under the OAuth2 tab, generate an invite link for the bot:
     - Select the "bot" scope.
     - Assign necessary permissions (e.g., "Administrator").
   - Use the link to invite the bot to your Discord server.
3. Set Up the Bot:
   - Replace the placeholder TOKEN in the dndbot.py script with your bot token.
     TOKEN = 'your-bot-token-here'
   - Alternatively, use an environment variable:
     - Set an environment variable called DISCORD_TOKEN with your token.
     - Modify the script to read the token from the environment:
       import os
       TOKEN = os.getenv('DISCORD_TOKEN')

Run the Bot
Start the bot by running the script:
python dndbot.py

---

Commands

1. !monster <monster_name>
- Description: Search for a D&D monster by name.
- Usage: 
  - Example: !monster dragon
- What It Does:
  - If only one match is found, detailed monster information is displayed.
  - If multiple matches are found, you'll be prompted to select one by typing a number.

2. !spell <spell_name>
- Description: Search for a D&D spell by name.
- Usage: 
  - Example: !spell fireball
- What It Does:
  - If only one match is found, detailed spell information is displayed.
  - If multiple matches are found, you'll be prompted to select one by typing a number.

---

Troubleshooting

Common Issues
1. Bot Not Responding:
   - Ensure the bot is running (check your terminal for errors).
   - Verify the bot is invited to your server and online.
   - Ensure your commands are correctly formatted (e.g., !monster <name>).
2. Invalid Token:
   - Double-check the bot token in your script.
   - Regenerate the token in the Developer Portal if needed.

Debugging
Run the bot in your terminal to view error messages or debug logs.

---

Contributing
Feel free to contribute to the bot by adding new features or improving the code. Submit a pull request or fork the repository to get started.

---

License
This project uses the MIT License (https://opensource.org/licenses/MIT). Feel free to use, modify, and distribute this bot as needed.
