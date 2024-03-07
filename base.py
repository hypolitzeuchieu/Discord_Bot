import discord
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

    salutation_name = ['hey', 'hi', 'hello']
    if message.content.lower() in salutation_name:
        await message.channel.send(f"hello **{message.author.display_name}** hope *you are fine*!", delete_after=10)


@bot.event
async def on_member_join(member):
    try:
        general_channel = bot.get_channel(1214528710414307340)
        if general_channel:
            content = f"welcome **{member.display_name}** to this server **{member.guild.name}** this is a message of **{bot.user.name}**"
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
    except discord.NotFound:
        await ctx.send(f"**{user.name}** not found")
    except discord.Forbidden:
        await ctx.send("permission denied")

bot.run(token_key)
