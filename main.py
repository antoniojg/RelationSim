import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from db.DBClient import DBClient

load_dotenv()

db_file = "relationsim.db"
db = DBClient(db_file)

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="!")
bot = commands.Bot(command_prefix="$", intents= discord.Intents.default())

sleep = 0
use = 1

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown, you can use it in {round(error.retry_after, 2)} seconds")

@bot.command()
@commands.cooldown(use, sleep, commands.BucketType.user)
async def join(ctx):
    try:
        user = (ctx.message.author.id, ctx.message.author.name)
        db.insert_new_user(user)
        await ctx.send('>>> Welcome to **RelationSim** {},\n\nYou will be able to meet and have a relationship\nindicator in your server similar to relationships\nin the sims!\n__Commands are as follow:__\n**$meet** *@user* - `Allows you to start a friendship with another user`\n**$up** *@user* - `Adds relationship points`\n**$down** *@user* - `Subtracts relationship points`\n**$relationship** *@user* - `Allows you to check your status with another user`'.format(ctx.message.author))
    except:
        await ctx.send('> Looks like you already joined!')


@bot.command()
@commands.cooldown(use, sleep, commands.BucketType.user)
async def meet(ctx):
    try:
        if ctx.message.mentions[0].id:
            mentionedUserID = ctx.message.mentions[0].id
            db.create_relationship(ctx.message.author.id,  mentionedUserID)
            await ctx.send('>>> @{} and {} have **met!**'.format(ctx.message.author, ctx.message.mentions[0].mention))
    except:
        await ctx.send('> @{}, Please mention a user'.format(ctx.message.author))

@bot.command()
@commands.cooldown(use, sleep, commands.BucketType.user)
async def up(ctx):
    try:
        if ctx.message.mentions[0].id:
            mentionedUserID = ctx.message.mentions[0].id
            status = db.positive_relationship(ctx.message.author.id, mentionedUserID)
            await ctx.send('> @{} and {}: :simspositivemeote: {}'.format(ctx.message.author, ctx.message.mentions[0].mention, status))
    except:
        await ctx.send('> @{}, Please mention a user'.format(ctx.message.author))

@bot.command()
@commands.cooldown(use, sleep, commands.BucketType.user)
async def down(ctx):
    try:
        if ctx.message.mentions[0].id:
            mentionedUserID = ctx.message.mentions[0].id
            status = db.negative_relationship(ctx.message.author.id, mentionedUserID)
            print(status)
            await ctx.send('> @{} and {}: :grinning: {}'.format(ctx.message.author,ctx.message.mentions[0].mention, status))
    except:
        await ctx.send('> @{}, Please mention a user'.format(ctx.message.author))

@bot.command()
@commands.cooldown(use, sleep, commands.BucketType.user)
async def relationship(ctx):
    try:
        if ctx.message.mentions[0].id:
            mentionedUserID = ctx.message.mentions[0].id
            status = db.relationship_status(ctx.message.author.id, mentionedUserID)
            await ctx.send('> @{} and {} are **{}**'.format(ctx.message.author, ctx.message.mentions[0].mention, status))
    except:
        await ctx.send('> @{}, Please mention a user'.format(ctx.message.author))

@bot.command()
@commands.cooldown(use, sleep, commands.BucketType.user)
async def test_test_test(ctx):
    await ctx.send("> This is just a test event")


bot.run(os.getenv('TOKEN'))