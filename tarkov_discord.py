import os
import urllib.parse

import discord
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

SEARCH_URL = os.environ.get(
    "SEARCH_URL",
    "https://escapefromtarkov.fandom.com/wiki/Special:Search?query={query}&scope=internal&navigationSearch=true",
)
ITEM_DETAILS_URL = os.environ.get(
    "ITEM_DETAILS_URL", "https://escapefromtarkov.fandom.com/wiki/{item}"
)
USER_AGENT = "takov-bot-discord"

tarkov_command_group = discord.app_commands.Group(
    name="tarkov", description="Check Escape from Tarkov wiki"
)


def item_details_url(item):
    safe_item = urllib.parse.quote_plus(item.replace(" ", "_"))
    url = ITEM_DETAILS_URL.format(item=safe_item)
    # headers = {"User-Agent": USER_AGENT}
    # return requests.get(url, headers=headers)
    return url


def get_search_results(query):
    safe_query = urllib.parse.quote_plus(query)
    url = SEARCH_URL.format(query=safe_query)
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find("ul", class_="unified-search__results")

    if not results:
        return []

    links = set()
    result_links = [
        a.get("href")
        for a in results.find_all("a")
        if not (a.get("href") in links or links.add(a.get("href")))
    ]
    return result_links


@tarkov_command_group.command()
@discord.app_commands.describe(query="Search query")
async def search(interaction: discord.Interaction, query: str):
    """Search Escape from Tarkov wiki"""
    results = get_search_results(query)
    max_results = 10
    description = (
        f"Here are the top {min(len(results), max_results)} search results for '{query}':"
        if results
        else f"No search results for '{query}'."
    )
    embed = discord.Embed(
        title=f"'{query}' Search Results",
        url=SEARCH_URL.format(query=urllib.parse.quote_plus(query)),
        description=description,
        color=discord.Color.blue(),
    )
    embed.set_author(name="TarkovBot", url="https://github.com/fredericojordan")
    for r in results[:max_results]:
        item = urllib.parse.unquote(r.split("/")[-1].replace("_", " "))
        embed.add_field(name=item, value=r, inline=False)
    await interaction.response.send_message(embed=embed)


@tarkov_command_group.command()
@discord.app_commands.describe(item="Check item")
async def details(interaction: discord.Interaction, item: str):
    """Search Escape from Tarkov wiki"""
    url = item_details_url(item)
    embed = discord.Embed(
        title=item, url=url, description=item, color=discord.Color.blue()
    )
    embed.set_author(name="TarkovBot", url="https://github.com/fredericojordan")
    await interaction.response.send_message(embed=embed)


@discord.app_commands.command()
async def poyta(interaction: discord.Interaction):
    """Poyta bio."""
    await interaction.response.send_message("Poyta é um bundão!")


class TarkovBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.command_tree = discord.app_commands.CommandTree(self)
        self.command_tree.add_command(tarkov_command_group)
        self.command_tree.add_command(poyta)

    async def setup_hook(self):
        await self.command_tree.sync()


if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")

    if token:
        client = TarkovBot(intents=discord.Intents.default())
        client.run(token)
    else:
        print("Please set the DISCORD_TOKEN environment variable!")
        exit(1)
