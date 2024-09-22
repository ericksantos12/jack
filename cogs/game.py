import asyncio
import discord
from discord.ui import Select
from discord.ext import commands
from discord.commands import Option
from backend import log, error_template

from utils.game_info import retrieve_game_details, retrieve_game_links


class Game(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: game.py Loaded")

    # Get Games
    @commands.slash_command(name="get", description="Search for a game")
    async def get(
        self,
        ctx,
        name: Option(str, "The game you want to search for", required=True),
        # provider: Option(choices=["SteamRIP", "Fitgirl"], description="The provider to search for"),
    ):
        try:
            game_results = await retrieve_game_links(name)
            if game_results:
                log.info(f"Found {len(game_results)} games")

                select = Select(
                    custom_id="select_game",
                    placeholder="Select a game",
                    options=[
                        discord.SelectOption(
                            label=game["title"],
                            description=game["fileSize"],
                            value=str(index),
                        )
                        for index, game in enumerate(game_results)
                    ],
                )

                view = discord.ui.View()
                view.add_item(select)

                async def callback(interaction):
                    await interaction.response.defer()
                    game = game_results[int(interaction.data["values"][0])]
                    download_links = [uri for uri in game["uris"]]

                    embed = discord.Embed(title=game["stripped_title"], color=0xFF0000)
                    try:
                        game_details = retrieve_game_details(game["stripped_title"])

                        embed.add_field(
                            name="Summary", value=f"{game_details['summary']}", inline=False
                        )
                        embed.add_field(
                            name="File Size", value=f"📦 {game['fileSize']}", inline=True
                        )
                        embed.add_field(
                            name="Total Rating",
                            value=f"⭐ {round((game_details['total_rating']/10), 1)}/10",
                            inline=True,
                        )
                        embed.add_field(
                            name=f"🔗 Download Links",
                            value="\n".join(download_links),
                            inline=False,
                        )
                        embed.set_image(url=game_details["header"])
                    except IndexError as e:
                        log.error(f"IGDB Data not found for {game['stripped_title']}")
                        embed.add_field(
                            name="File Size", value=f"📦 {game['fileSize']}", inline=True
                        )
                        embed.add_field(
                            name=f"🔗 Download Links",
                            value="\n".join(download_links),
                            inline=False,
                        )
                        
                    embed.set_footer(text="Be aware of the risks of downloading from third-party sites")
                        
                    await interaction.followup.send(embed=embed)

                select.callback = callback

                embed = discord.Embed(title="Select a Game", color=0xFF0000)
                game_titles = [
                    f"{i+1}. {game['title']}" for i, game in enumerate(game_results)
                ]
                embed.add_field(
                    name="Games", value="\n".join(game_titles), inline=False
                )

                await ctx.respond(embed=embed, view=view, ephemeral=True)

            else:
                await ctx.respond(f"Game not found", ephemeral=True)
        except Exception as e:
            log.error(e)
            await ctx.respond(embed=error_template(e), ephemeral=True)


def setup(client):
    client.add_cog(Game(client))
