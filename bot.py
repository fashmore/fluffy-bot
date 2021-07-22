#import
import discord
import json
from discord.ext import commands

#assign bot token
TOKEN = ''

#assign bot prefix
client = commands.Bot(command_prefix = '?')

#error for missing argument
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Use the right syntax, stupid ass.')

#ready check
@client.event
async def on_ready():
    print('Bot is ready')

#global variables
class Captain:
    def __init__(self, ID, Amount, AvailableSlots):
        self.ID = ID
        self.Amount = Amount
        self.AvailableSlots = AvailableSlots

#bidding Cog
class BiddingCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.topbidder = 0
        self.cost = 0
        self.player = 'scrub'
        self.isbidding = False
        self.captains = {}


    #add captains
    @commands.command()
    @commands.has_role('Mini Admin')
    async def addcaptain(self, ctx, player, cost:int, slots:int):
        self.captains[player] = Captain(player, cost, slots)
        await ctx.send(f'{player} is a captain with {cost} dollars and {slots} slots available.')


    #start bidding
    @commands.command()
    async def startbid(self, ctx, cost:int, player):
        self.isbidding = True
        captain = self.captains[str(ctx.message.author)]
        if cost <= captain.Amount and captain.AvailableSlots > 0 and cost >= 0:
            self.topbidder = ctx.message.author
            self.cost = cost
            self.player = player
            await ctx.send(f'{self.topbidder} nominates {self.player} and starts the bidding at {self.cost} dollars.')
        else:
            await ctx.send(f'{ctx.message.author} is a poor ass.')


    #additional bidding
    @commands.command()
    async def bid(self, ctx, cost:int):
        if self.isbidding == True:
            captain = self.captains[str(ctx.message.author)]
            if cost >= (self.cost + 5) and cost <= captain.Amount and captain.AvailableSlots > 0 and cost >= 0:
                self.topbidder = ctx.message.author
                self.cost = cost
                await ctx.send(f'{self.topbidder} bids {self.cost}.')
            else:
                await ctx.send(f'{ctx.message.author} is a poor ass.')
        else:
            await ctx.send(f'{ctx.message.author} is a stupid ass.')


    #end bidding
    @commands.command()
    @commands.has_role('Mini Admin')
    async def sold(self, ctx):
        if self.isbidding == True:
            captain = self.captains[str(self.topbidder)]
            captain.Amount = (captain.Amount - self.cost)
            captain.AvailableSlots = captain.AvailableSlots - 1
            await ctx.send(f'Round over. {self.player} is sold to {self.topbidder} for {self.cost} dollars.')
            embed=discord.Embed(color=0x4682B2)
            for key, value in self.captains.items():
                embed.add_field(name=key, value=f'${value.Amount} \n {value.AvailableSlots} slots', inline=True)
            embed.set_footer(text = 'wheeeeeeeeeeeeeeeeeee', icon_url = ctx.author.avatar_url)
            await ctx.send(embed=embed)
            self.isbidding = False
        else:
            await ctx.send(f'{ctx.message.author} is a stupid ass.')


    #display balance
    @commands.command()
    async def balance(self,ctx):
        embed=discord.Embed(color=0x4682B2)
        for key, value in self.captains.items():
            embed.add_field(name=key, value=f'${value.Amount} \n {value.AvailableSlots} slots', inline=True)
        embed.set_footer(text = 'wheeeeeeeeeeeeeeeeeee', icon_url = ctx.author.avatar_url)
        await ctx.send(embed=embed)


#add bidding cog
client.add_cog(BiddingCommands(client))

#run bot
client.run(TOKEN)
