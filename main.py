import discord
from discord.ext import commands
TOKEN = "MTA4MjYxMDEwMDQ0MDY2NjExMg.GOtV9S.Wbtd49czur2PYaL8n3nbLHyiWmWmQPzks51_4c"
class ExampleBot(commands.Bot):
    def __init__(self):
        # initialise l'objet bot
        # ici on prend les intents all au cas ou on en ai besoin
        super().__init__( 
            command_prefix="$",
            intents=discord.Intents.all()
        )
    
    async def setup_hook(self): # on crée une fonction pour charger les extensions
        await self.load_extension("bjorgus") # on charge l'extension bjorgus.py

ExampleBot().run(TOKEN) # on lance le bot