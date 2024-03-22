import json
import random
import os
from dotenv import load_dotenv

load_dotenv()

import discord
import requests
from discord.ext.commands.errors import UserNotFound

from key_token import token_key
from discord import Intents
from discord.ext import commands

intents = Intents.all()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", description="try discord Bot", intents=intents)


@bot.event
async def on_ready():
    print(f"ready for {bot.user.name}...")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

    if message.content.startswith('!'):
        return

    salutation_name = ['hey', 'hi', 'hello', 'coucou']
    if message.content.lower() in salutation_name:
        await message.channel.send(f"hello **{message.author.display_name}** hope *you are fine*!", delete_after=10)


@bot.event
async def on_member_join(member):
    try:
        general_channel = bot.get_channel(1214528710414307340)
        guild = member.guild
        permissions = discord.Permissions(read_messages=True, send_messages=True)
        role = await guild.create_role(name="member_join", permissions=permissions)
        await member.add_roles(role)
        print(role)
        if general_channel:
            content = f"welcome **{member.display_name}** to this server **{member.guild.name}** this is a message of **{bot.user.name}**"
            await general_channel.send(content)
    except Exception as e:
        print(f"something went wrong : {e}")


@bot.event
async def on_member_remote(member):
    try:
        general_channel = bot.get_channel(1214528710414307340)
        if general_channel:
            content = f" **{member.display_name}** has left that server **{member.guild.name}** this is a message of **{bot.user.name}**"
            await general_channel.send(content)
    except Exception as e:
        print(f"something went wrong : {e}")


@bot.command(name='drop')
async def drop(ctx, number_of_message: int):
    try:
        if ctx.author.guild_permissions.manage_messages:

            messages = await ctx.channel.purge(limit=number_of_message + 1)
            await ctx.send(f"**{len(messages)-1}** was deleted", delete_after=10)
        else:
            await ctx.send("permission denied")

    except Exception as e:
        print(f"something went wrong : {e}")
        await ctx.send("something went wrong.")


@bot.command(name="kick")
async def kick_member(ctx, user: discord.Member, *raison):
    reason = " ".join(raison)
    if not reason:
        reason = "no reason provided"
    try:
        if ctx.author.guild_permissions.kick_members:
            await ctx.guild.kick(user=user, reason=reason)
            await ctx.send(f"**{user}** was kicked and the reason is **{reason}**", delete_after=20)
    except Exception as e:
        print(f"something went wrong : {e}")
        await ctx.send("something went wrong.")


@bot.command(name='ban')
async def ban_member(ctx, user: discord.User, *reason):

    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("permission denied")

    reason = " ".join(reason)
    if not reason:
        reason = "no reason provided"

    try:
        await ctx.guild.ban(user=user, reason=reason)
        await ctx.send(f"**{user}** was banned and the reason is **{reason}**")

    except discord.Forbidden:
        await ctx.send("i've not permission to ban that member")

    except discord.HTTPException as e:
        await ctx.send(f"error **{e}**")

    except UserNotFound:
        await ctx.send(f"**{user}** not found")

    except Exception as e:
        print(f"something went wrong : {e}")
        await ctx.send("something went wrong.")


@bot.command(name='unban')
async def unban(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    if not reason:
        reason = "no reason provided"
    try:
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f"**{user.name}** was unbanned and the reason is **{reason}**")
    except UserNotFound:
        await ctx.send(f"**{user.name}** not found")
    except discord.Forbidden:
        await ctx.send("permission denied")


# get endpoint data (quote command !quote)
def get_api_data():
    url = "https://dummyjson.com/quotes"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["quotes"]
    else:
        print("get error")
        return []


# random choice function
def get_random_quote(quotes):
    return random.choice(quotes)


@bot.command(name="quote")
async def quote(ctx):
    quote_data = get_api_data()
    if quote_data:
        random_quote = get_random_quote(quote_data)
        await ctx.send(f"**{random_quote['quote']}**")

    else:
        await ctx.send("not found")

# challenges command(!challenge)


def open_file():
    with open('test.json', 'r') as f:
        data = json.load(f)
        return data


def random_challenges(challenges):
    return random.choice(challenges)


@bot.command(name="challenge")
async def challenge(ctx):
    property_challenge = open_file()
    data = property_challenge['challenges']
    if data:
        random_challenge = random_challenges(data)
        await ctx.send(f"challenge:**{random_challenge['name']}**\n**{random_challenge['url']}**")
    else:
        await ctx.send("page not found")

# add list command ( !list )


@bot.command(name="list")
async def list_challenges(ctx):
    property_list = open_file()
    data = property_list['challenges']
    for i in data:
        await ctx.send(f"**{i['name']}**:{i['url']}")

# add command( !add)


@bot.command(name="add")
async def add_command(ctx, urls):
    com = open_file()
    data = com['challenges']
    for i in data:
        if i['url'] == urls:
            await ctx.send(f"**{i['name']}**:{i['url']} already  exist")
            return
    await ctx.send(f"unable to add: **{urls}** please check it is a valid Coding Challenge")

    # new_challenge = {"name": "new challenge", "url": urls}
    # data.append(new_challenge)
    #
    # with open('test.json', 'w') as file:
    #     json.dump(com, file, indent=4)
    #
    # await ctx.send(f"**{new_challenge['name']}**:{new_challenge['url']} added successfully")

# function to retrieve a guild's roles


async def get_role(guild):
    return await guild.fetch_roles()

    # command to list role


@bot.command(name="listroles")
async def list_role(ctx):
    guild = ctx.guild
    roles = await get_role(guild)

    if roles:
        embed = discord.Embed(title=f"Role in {guild.name}")

        for role in roles:
            embed.add_field(name=role.name, value=f"ID={role.id}", inline=False)
            await ctx.send(embed=embed)
    else:
        await ctx.send(f"this server currently has no role.")

# command to add role


bot.run(os.getenv("token_key"))
