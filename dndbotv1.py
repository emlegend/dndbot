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


def api_request(base_url, params=None, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code}. Retrying...")
                time.sleep(3)
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            time.sleep(3)
    return None

def search_monster(monster_name):
    url = "https://api.open5e.com/monsters/"
    data = api_request(url, params={"search": monster_name})
    if data:
        monsters = data.get('results', [])
        unique_monsters = {monster['name'].lower(): monster for monster in monsters}
        return list(unique_monsters.values())
    return None

def get_monster(monster_slug):
    url = f"https://api.open5e.com/monsters/{monster_slug}/"
    return api_request(url)

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
        await ctx.send("Please provide the name of the monster you're looking for. Usage: !monster <monster_name>")
        return
    
    monsters = search_monster(monster_name)
    
    if monsters is None:
        await ctx.send("Unable to fetch monster data. The server might be down. Please try again later.")
        return
    
    if not monsters:
        await ctx.send(f"No monsters found matching '{monster_name}'.")
        return
    
    if len(monsters) == 1:
        monster = get_monster(monsters[0]['slug'])
        if monster:
            await ctx.send(format_monster_info(monster))
    else:
        response = "**Monsters found:**\n"
        for i, monster in enumerate(monsters):
            response += f"{i + 1}. {monster['name']}\n"
        
        await ctx.send(response + "\nPlease type a number to select a monster (e.g., 1).")

        def check(m):
            return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= len(monsters)

        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            choice = int(msg.content) - 1
            monster = get_monster(monsters[choice]['slug'])
            if monster:
                await ctx.send(format_monster_info(monster))
        except Exception:
            await ctx.send("You didn't reply in time or entered an invalid choice. Please try again.")

def search_spell(spell_name):
    url = "https://api.open5e.com/spells/"
    data = api_request(url, params={"search": spell_name})
    if data:
        spells = data.get('results', [])
        unique_spells = {spell['name'].lower(): spell for spell in spells}
        return list(unique_spells.values())
    return None

def format_spell_info(spell):
    return (f"**Name:** {spell['name']}\n"
            f"**Level:** {spell['level']}\n"
            f"**School:** {spell['school']}\n"
            f"**Casting Time:** {spell['casting_time']}\n"
            f"**Range:** {spell['range']}\n"
            f"**Components:** {spell['components']}\n"
            f"**Duration:** {spell['duration']}\n"
            f"**Description:** {spell['desc']}")

@bot.command(name='spell', help='Look up a D&D spell by name. Usage: !spell <spell_name>')
async def spell_lookup(ctx, *, spell_name: str = None):
    if not spell_name:
        await ctx.send("Please provide the name of the spell you're looking for. Usage: !spell <spell_name>")
        return
    
    spells = search_spell(spell_name)
    
    if spells is None:
        await ctx.send("Unable to fetch spell data. The server might be down. Please try again later.")
        return
    
    if not spells:
        await ctx.send(f"No spells found matching '{spell_name}'.")
        return
    
    if len(spells) == 1:
        await ctx.send(format_spell_info(spells[0]))
    else:
        response = "**Spells found:**\n"
        for i, spell in enumerate(spells):
            response += f"{i + 1}. {spell['name']}\n"
        
        await ctx.send(response + "\nPlease type a number to select a spell (e.g., 1).")

        def check(m):
            return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= len(spells)

        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            choice = int(msg.content) - 1
            await ctx.send(format_spell_info(spells[choice]))
        except Exception:
            await ctx.send("You didn't reply in time or entered an invalid choice. Please try again.")
bot.run(TOKEN)
