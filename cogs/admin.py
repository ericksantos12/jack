from discord.ext import commands
from discord.commands import Option
from backend import log, error_template


class Admin(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: admin.py Loaded")
        
    # Load
    @commands.slash_command(name="load", description="Load a cog")
    @commands.is_owner()
    async def load(self, ctx, extension: Option(str, "The name of the cog to load")):
        try:
            self.bot.load_extension(f"cogs.{extension}")
            log.info(f"Loaded {extension}")
            await ctx.respond(f"✅ Loaded {extension}", ephemeral=True)
        except Exception as e:
            log.error(e)
            await ctx.respond(embed=error_template(e), ephemeral=True)
        
    # Unload
    @commands.slash_command(name="unload", description="Unload a cog")
    @commands.is_owner()
    async def unload(self, ctx, extension: Option(str, "The name of the cog to unload")):
        try:
            self.bot.unload_extension(f"cogs.{extension}")
            log.info(f"Unloaded {extension}")
            await ctx.respond(f"🔥 Unloaded {extension}", ephemeral=True)
        except Exception as e:
            log.error(e)
            await ctx.respond(embed=error_template(e), ephemeral=True)
        
    # Reload
    @commands.slash_command(name="reload", description="Reload a cog")
    @commands.is_owner()
    async def reload(self, ctx, extension: Option(str, "The name of the cog to reload")):
        try:
            self.bot.reload_extension(f"cogs.{extension}")
            log.info(f"Reloaded {extension}")
            await ctx.respond(f"🔃 Reloaded {extension}", ephemeral=True)
        except Exception as e:
            log.error(e)
            await ctx.respond(embed=error_template(e), ephemeral=True)
    
    # Sync
    @commands.slash_command(name="sync", description="Sincronizar todos os comandos de barra")
    @commands.is_owner()
    async def sync_commands(self, ctx):
        try:
            await self.bot.sync_commands()
            log.info(f"Synced commands globally.")
            await ctx.respond(f"📡 Synced commands globally.", ephemeral=True)
        except Exception as e:
            log.error(e)
            await ctx.respond(embed=error_template(e), ephemeral=True)

def setup(client):
    client.add_cog(Admin(client))