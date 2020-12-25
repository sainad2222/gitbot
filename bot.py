from github import Github
import discord
import os
from discord.ext import commands,tasks

# github instance
gh = Github(os.getenv('GITHUB'))
# discord instance
bot = commands.Bot(command_prefix='!')

## EVENTS

@bot.event  # to make function represent a event
async def on_ready():
    # change_status.start()
    print("Bot is ready to rock and roll")

@bot.event  # if invalid command
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Command not found')

@bot.command()
async def update(ctx):
    # getting current no of channels
    channels = []
    for channel in ctx.guild.text_channels:
        channels.append(channel.name)
    channels.remove('general')
    curChannelLen = len(channels)
    
    # getting current no of repos
    repos = []
    repourls = {}
    for repo in gh.get_user().get_repos():
        cur = repo.name
        cur = cur.replace('.','')
        cur = cur.lower()
        repos.append(cur)
        repourls[cur] = 'https://github.com/'+repo.full_name+'/settings/hooks'
    curRepoLen = len(repos)

    # if no updates needed
    if curChannelLen == curRepoLen:
        await ctx.send('Already up to date')
        return

    # main code(creating channel and webhook)
    cnt = 0
    for repo in repos:
        if repo not in channels:
            channel = await ctx.guild.create_text_channel(repo)
            await ctx.send(f'{channel} created')
            try:
                webhook = await channel.create_webhook(name=repo)
                webhook_url = webhook.url + '/github'
                await ctx.send(f' use {webhook_url} for {repourls[repo]}')
            except Exception as e:
                print(e)
            cnt+=1

    await ctx.send(f"created {cnt} channels")
            
bot.run(os.getenv('DISCORD'))
