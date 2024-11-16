import discord
import requests
import time
from discord.ext import commands

# Replace this with bot token
TOKEN = ''


intents = discord.Intents.default()
intents.message_content = True  
intents.guilds = True           
intents.members = True          


bot = commands.Bot(command_prefix="!", intents=intents)
def search_monster(monster_name):
    url = "https://api.open5e.com/monsters/"
    retries = 3 
    for attempt in range(retries):
        try:
            response = requests.get(url, params={"search": monster_name})
            if response.status_code == 200:
                monsters = response.json()['results']
                
               
                unique_monsters = {}
                for monster in monsters:
                    name_key = monster['name'].lower()
                    if name_key not in unique_monsters:
                        unique_monsters[name_key] = monster

                return list(unique_monsters.values())
                
            else:
                print(f"Error fetching monster list. Status code: {response.status_code}")
                if attempt < retries - 1:
                    print("Retrying...")
                    time.sleep(3)  
                else:
                    return None
        except Exception as e:
            print(f"An error occurred: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(3)  
            else:
                return None

def get_monster(monster_slug):
    url = f"https://api.open5e.com/monsters/{monster_slug}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            monster_data = response.json()
            return monster_data
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def format_monster_info(monster):
    info = (f"**Name:** {monster['name']}\n"
            f"**Size:** {monster['size']}\n"
            f"**Type:** {monster['type']}\n"
            f"**Alignment:** {monster['alignment']}\n"
            f"**Hit Points:** {monster['hit_points']}\n"
            f"**Armor Class:** {monster['armor_class']}\n"
            f"**Challenge Rating:** {monster['challenge_rating']}\n"
            f"**Actions:**\n")
    for action in monster.get('actions', []):
        info += f"  - {action['name']}: {action['desc']}\n"
    return info

@bot.command(name='monster', help='Look up a D&D monster by name. Usage: !monster <monster_name>')
async def monster_lookup(ctx, *, monster_name: str = None):
    if not monster_name:
        await ctx.send("Please provide the name of the monster you're looking for. Usage: `!monster <monster_name>`")
        return
    
    monsters = search_monster(monster_name)
    
    if monsters is None:
        await ctx.send("Unable to fetch monster data. The server might be down. Please try again later.")
        return
    
    if not monsters:
        await ctx.send(f"No monsters found matching '{monster_name}'.")
        return
    
    if len(monsters) == 1:
        monster_slug = monsters[0]['slug']
        monster = get_monster(monster_slug)
        if monster:
            await ctx.send(format_monster_info(monster))
    else:
        response = "**Monsters found:**\n"
        for i, monster in enumerate(monsters):
            response += f"{i + 1}. {monster['name']}\n"
        
        await ctx.send(response + "\nPlease type a number to select a monster (e.g., `1`).")

        def check(m):
            return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= len(monsters)

        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            choice = int(msg.content) - 1
            monster_slug = monsters[choice]['slug']
            monster = get_monster(monster_slug)
            if monster:
                await ctx.send(format_monster_info(monster))
        except Exception as e:
            await ctx.send("You didn't reply in time or entered an invalid choice. Please try again.")

bot.run(TOKEN)
