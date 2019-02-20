import random

from discord.ext import commands
import discord
import datetime

from util import cards_db,cards

#All the types of packs
PACKS = {
    'Wood' : 50,
    'Iron' : 150,
    'Gold' : 450
}

async def has_account(ctx):
    #Creates an account for the user, if they do not already have one
    if not isinstance(ctx,int):
        id = ctx.author.id
    else:
        id = ctx
    if not cards_db.user_exists(id):
        cards_db.add_user(id)
    return True

class CardGame:

    def __init__(self, bot):
        self.bot = bot
        self.times = dict()

    @commands.command(name='balance',)
    @commands.check(has_account)
    async def _balance(self,ctx):
        '''Displays the balance of the user'''
        id = ctx.author.id
        balance = cards_db.get_balance(id)
        embed = discord.Embed(title=f"Current Balance: **{balance}** Big Bucks", color = 16744272)
        embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.description = "Keep typing to earn more money!"
        await ctx.send(embed=embed)

    @commands.command(name='buy',)
    @commands.check(has_account)
    async def _buy(self,ctx,arg):
        '''Buy a card pack'''
        id = ctx.author.id
        balance = cards_db.get_balance(id)
        pack = arg.capitalize()
        #Check the pack can be bought
        if pack not in PACKS:
            await ctx.send('Please enter a valid card pack!\nCurrent availible packs: Wood, Iron, Gold')
            return
        if PACKS[pack] > balance:
            await ctx.send(f'You can not afford the {pack} pack! \nThe pack costs {PACKS[pack]}, but you only have {balance}.')
            return

        #Opens the pack
        items = cards.open_pack(pack)
        cards_db.add_cards(id,items) #Adds the cards
        cards_db.update_balance(id,balance - PACKS[pack]) #Updates balance
        card_names = '\n'.join(cards.format(items))

        embed = discord.Embed(title=f"🎁 Opened a **{pack}** pack 🎁", color = 15834065)
        embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.add_field(name='**Cards**', value= card_names)
        await ctx.send(embed=embed)

    @commands.command(name='sell',)
    @commands.check(has_account)
    async def _sell(self,ctx,arg):
        '''Sell a card for Big Bucks!'''
        id = ctx.author.id
        card_info = cards.get_card(arg)
        usr_cards = cards_db.get_cards(id)
        #The card does not exist
        if card_info == None:
            await ctx.send(f"There doesn't seem to be a **{arg}** in our records.")
            return
        #Check if the user has the card
        if int(card_info['id']) not in usr_cards:
            await ctx.send(f"You don't seem to have a copy of {card_info['name']}.")
            return
        #If they do, remove the card, add the big bucks
        cards_db.remove_card(id,card_info['id'])
        balance = cards_db.get_balance(id)
        cards_db.update_balance(id,balance + int(card_info['value']))

        embed = discord.Embed(title=f"💰 Sold: **{card_info['name']}** 💰", color = 15834065)
        embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.description = f"Sold the card for {card_info['value']} Big Bucks."
        await ctx.send(embed=embed)

    @commands.command(name='cards',)
    @commands.check(has_account)
    async def _cards(self,ctx,arg0: int = 1):
        '''Displays the cards in your deck'''
        id = ctx.author.id
        usr_cards = cards_db.get_cards(id)
        count = len(usr_cards)
        #Pagination
        if arg0 <= 0 or (count // 10) + 1 < arg0:
            await ctx.send(f'Invalid Page requested: {arg0}')
        #Stylistic and Discord embed limits, so paginate cards
        card_names = cards.format(usr_cards[(arg0-1) * 10 : (arg0-1) * 10 + 10])
        card_names = '\n'.join(card_names)
        embed = discord.Embed(title=f"Card Count: {count}", color = 16744272)
        embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
        if card_names == '':
            embed.add_field(name='**Cards**', value= "You have no cards! You can buy card packs with !buy")
        else:
            embed.add_field(name='**Cards**', value= card_names)
        embed.set_footer(text=f"Showing page {arg0} of {count//10 + 1}")
        await ctx.send(embed=embed)

    @commands.command(name='balupd', hidden=True)
    @commands.check(has_account)
    async def _balupd(self,ctx,arg: int):
        id = ctx.author.id
        cards_db.update_balance(id,arg)

    @commands.command(name='pay',)
    @commands.check(has_account)
    async def _pay(self,ctx,arg0,arg1: int):
        '''Pay someone money'''
        id = ctx.author.id
        #Get the other user
        usr1 = self.bot.get_user(id=int(arg0.strip('!<@').strip('>')))
        if usr1 == None:
            await ctx.send('Could not find that person!')
            return
        await has_account(usr1.id)
        #Bunch of checks
        if arg1 <= 0:
            await ctx.send('Please specify a positive amount.')
            return
        balance = cards_db.get_balance(id)
        if arg1 > balance:
            await ctx.send('You do not have enough money!')
            return
        #Update balances
        cards_db.update_balance(id,balance - arg1)
        balance1 = cards_db.get_balance(usr1.id)
        cards_db.update_balance(usr1.id,balance1 + arg1)
        await ctx.send(f"Successfully gave {arg1} to {arg0}!")

    async def on_message(self,ctx):
        #Update a dictionary every message, gaining xp every minute
        id = ctx.author.id
        await has_account(id)
        if id in self.times:
            if datetime.datetime.utcnow() - self.times[id] > datetime.timedelta(minutes=1):
                balance = cards_db.get_balance(id)
                cards_db.update_balance(id,balance + random.randint(10,15))
                self.times[id] = datetime.datetime.utcnow()
        else:
            self.times[id] = datetime.datetime.utcnow()


def setup(bot):
    bot.add_cog(CardGame(bot))
