import random
import math

from discord.ext import commands
import discord
import datetime

from util import cards_db,cards,TradeUnit

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

trades = dict() #Channel -> TradeUnit
currently_trading = set()
times = dict()

async def trade_valid(ctx):
    #Checks if the trade command was typed in a valid channel
    if ctx.channel not in trades:
        await ctx.send('Not in a valid trade chat')
        return False
    trade = trades[ctx.channel]
    if ctx.author not in trade.usrs:
        await ctx.send('You are not part of this trade')
        return False
    return True

class CardGame(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='balance',aliases = ['bal'])
    @commands.check(has_account)
    async def _balance(self,ctx):
        '''Displays the balance of the user'''
        #======== Temporary
        id = ctx.author.id
        await has_account(id)
        if id in times:
            if datetime.datetime.utcnow() - times[id] > datetime.timedelta(minutes=1):
                balance = cards_db.get_balance(id)
                cards_db.update_balance(id,balance + random.randint(20,40))
                times[id] = datetime.datetime.utcnow()
        else:
            times[id] = datetime.datetime.utcnow()
        #===============
        id = ctx.author.id
        balance = cards_db.get_balance(id)
        embed = discord.Embed(title=f"Current Balance: **{balance}** Big Bucks", color = 16744272)
        embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.description = "Keep typing to earn more money!"
        await ctx.send(embed=embed)


    @commands.command(name='buy',)
    @commands.check(has_account)
    async def _buy(self,ctx,arg = ''):
        '''Buy a card pack'''
        id = ctx.author.id
        balance = cards_db.get_balance(id)
        pack = arg.capitalize()
        #Check the pack can be bought
        if pack not in PACKS:
            await ctx.send('Please enter a valid card pack!\nCurrent availible packs: Wood, Iron, Gold')
            return
        if PACKS[pack] > balance:
            await ctx.send(f'You can not afford the {pack} pack! \nThe pack costs {PACKS[pack]} Big Bucks, but you only have {balance}.')
            return
        if id in currently_trading:
            await ctx.send(f"You are currently trading. Please complete the trade to buy.")
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

#=============================================== Market values
    def buy_value(card):
        market = cards_db.market_cards()
        if int(card['id']) not in market:
            return int(card['value'])
        return round(int(card['value']) * math.pow(1.005,market[int(card['id'])]))
    def sell_value(card):
        market = cards_db.market_cards()
        if int(card['id']) not in market:
            return int(card['value'])
        return round(int(card['value']) * math.pow(0.995,market[int(card['id'])]))
#===============================================

    @commands.command(name='market',)
    async def _market_show(self,ctx,arg0: int = 1):
        '''Display the cards currently in the market'''
        market = cards_db.market_cards()
        market = cards.organize_market(market)
        count = len(market)
        #Pagination
        if arg0 <= 0 or (count // 10) + 1 < arg0:
            await ctx.send(f'Invalid Page requested: {arg0}')
            return
        #Stylistic and Discord embed limits, so paginate cards
        card_names = ''
        for tp in market[(arg0-1) * 10 : (arg0-1) * 10 + 10]:
            card = cards.get_card(tp[0])
            card_names += cards.format_string(card) + f' x{tp[1]}\n'
        embed = discord.Embed(title="**Market**", color = 16744272)
        embed.set_author(name=self.bot.user.name, icon_url = self.bot.user.avatar_url)
        if card_names == '':
            embed.add_field(name='**Cards**', value= "There are no cards in the market.")
        else:
            embed.add_field(name='**Cards**', value= card_names)
        embed.set_footer(text=f"Showing page {arg0} of {count//10 + 1}")
        await ctx.send(embed=embed)

    @commands.command(name='market-buy',)
    async def _market_buy(self,ctx,arg):
        '''Buy a card from the market'''
        id = ctx.author.id
        card_info = cards.get_card(arg)
        market = cards_db.market_cards()
        #The card does not exist
        if card_info == None:
            await ctx.send(f"There doesn't seem to be a **{arg}** in our records.")
            return
        #Check if the market has the card
        if int(card_info['id']) not in market:
            await ctx.send(f"The market doesn't seem to have a copy of {card_info['name']}.")
            return
        if id in currently_trading:
            await ctx.send(f"You are currently trading. Please complete the trade to buy from the market.")
            return
        buy_val = CardGame.buy_value(card_info)
        balance = cards_db.get_balance(id)
        if buy_val > balance:
            await ctx.send(f"You can't afford {card_info['name']}! It costs {buy_val} Big Bucks, but you only have {balance}")
            return
        cards_db.remove_from_market(card_info['id'])
        cards_db.add_cards(id,[card_info['id']])
        cards_db.update_balance(id,balance-buy_val)
        embed = discord.Embed(title=f"💰 Bought: **{card_info['name']}** 💰", color = 15834065)
        embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.description = f"Bought the card for {buy_val} Big Bucks."
        await ctx.send(embed=embed)


    @commands.command(name='sell',)
    @commands.check(has_account)
    async def _sell(self,ctx,*args):
        '''Sell a card for Big Bucks!'''
        id = ctx.author.id
        for arg in args:
            card_info = cards.get_card(arg)
            usr_cards = cards_db.get_cards(id)
            #The card does not exist
            if card_info == None:
                await ctx.send(f"There doesn't seem to be a **{arg}** in our records.")
                continue
            #Check if the user has the card
            if int(card_info['id']) not in usr_cards:
                await ctx.send(f"You don't seem to have a copy of {card_info['name']}.")
                continue
            if id in currently_trading:
                await ctx.send(f"You are currently trading. Please complete the trade to sell.")
                continue
            #If they do, remove the card, add the big bucks
            sell_val = CardGame.sell_value(card_info)
            cards_db.remove_card(id,card_info['id'])
            balance = cards_db.get_balance(id)
            cards_db.update_balance(id,balance + sell_val)
            cards_db.add_to_market(card_info['id'])

            embed = discord.Embed(title=f"💰 Sold: **{card_info['name']}** 💰", color = 15834065)
            embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
            embed.description = f"Sold the card for {sell_val} Big Bucks."
            await ctx.send(embed=embed)

    @commands.command(name='value')
    async def _value(self,ctx,arg):
        '''Check the value of a card'''
        card_info = cards.get_card(arg)

        if card_info == None:
            await ctx.send(f"There doesn't seem to be a **{arg}** in our records.")
            return
        sell_val = CardGame.sell_value(card_info)
        buy_val = CardGame.buy_value(card_info)
        embed = discord.Embed(title=f"**{card_info['name']}**", color = 15834065)
        embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.description = f"{card_info['name']} is a(n) {card_info['rarity']} card.\nCurrently worth {sell_val} Big Bucks to sell.\nCurrently worth {buy_val} Big Bucks to buy."
        await ctx.send(embed=embed)

    @commands.command(name='cards',)
    @commands.check(has_account)
    async def _cards(self,ctx,arg0: int = 1):
        '''Displays the cards in your deck'''
        id = ctx.author.id
        usr_cards = cards_db.get_cards(id)
        card_names = cards.format(usr_cards)
        count = len(card_names)
        #Pagination
        if arg0 <= 0 or (count // 10) + 1 < arg0:
            await ctx.send(f'Invalid Page requested: {arg0}')
            return
        #Stylistic and Discord embed limits, so paginate cards
        card_names = '\n'.join(card_names[(arg0-1) * 10 : (arg0-1) * 10 + 10])
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
        if id not in [184002906981269505,178663053171228674]:
            pass
        cards_db.update_balance(id,arg)

    @commands.command(name='card-get', hidden=True)
    @commands.check(has_account)
    async def _card_get(self,ctx,arg: int,arg1:int = 1):
        id = ctx.author.id
        if id not in [184002906981269505,178663053171228674]:
            pass
        cards_db.add_cards(id,[arg]*arg1)

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
        if id in currently_trading:
            await ctx.send(f"You are currently trading. Please complete the trade to buy.")
            return
        await has_account(usr1.id)
        #Bunch of checks
        if arg1 <= 0:
            await ctx.send('Please specify a positive amount.')
            return
        balance = cards_db.get_balance(id)
        if arg1 > balance:
            await ctx.send('You do not have enough Big Bucks!')
            return
        #Update balances
        cards_db.update_balance(id,balance - arg1)
        balance1 = cards_db.get_balance(usr1.id)
        cards_db.update_balance(usr1.id,balance1 + arg1)
        await ctx.send(f"Successfully gave **{arg1}** Big Bucks to {usr1.mention}!")

    @commands.command(name='trade',)
    @commands.check(has_account)
    async def _trade(self,ctx,arg0):
        '''Trade cards with other people'''
        id = ctx.author.id
        #Get the other user
        usr1 = self.bot.get_user(id=int(arg0.strip('!<@').strip('>')))
        if usr1 == None:
            await ctx.send('Could not find that person!')
            return
        if usr1.id == id:
            await ctx.send("Can't trade with yourself!")
            return
        await has_account(usr1.id)
        if ctx.channel in trades:
            await ctx.send("Can not create a trade in this channel")
            return
        if id in currently_trading or usr1.id in currently_trading:
            await ctx.send("Either you or the other person is already in a trade")
            return
        overwrites = {
            ctx.guild.get_member(id) : discord.PermissionOverwrite(read_message_history=True,send_messages=True,read_messages=True),
            ctx.guild.get_member(usr1.id) : discord.PermissionOverwrite(read_message_history=True,send_messages=True,read_messages=True)
        }
        channel = await ctx.guild.create_text_channel(name=f'trade-{ctx.author.display_name}-{usr1.display_name}', category = ctx.channel.category,overwrites=overwrites)
        a = TradeUnit.TradeUnit(ctx,channel,ctx.author,usr1)
        trades[channel] = a
        await a.setup()
        currently_trading.add(id)
        currently_trading.add(usr1.id)

    @commands.command(name='trade-add',hidden=True)
    @commands.check(trade_valid)
    async def _trade_add(self,ctx,*arg):
        '''Adds an item to the trade'''
        trade = trades[ctx.channel]
        await trade.add(ctx.author,arg)
        await ctx.message.delete()

    @commands.command(name='trade-remove',hidden=True)
    @commands.check(trade_valid)
    async def _trade_remove(self,ctx,*arg):
        '''Removes an item from the trade'''
        trade = trades[ctx.channel]
        await trade.remove(ctx.author,arg)
        await ctx.message.delete()

    @commands.command(name='trade-accept',hidden=True)
    @commands.check(trade_valid)
    async def _trade_accept(self,ctx):
        '''Accepts the trade'''
        trade = trades[ctx.channel]
        traded = await trade.accept(ctx.author)
        await ctx.message.delete()
        if traded:
            old_ctx = trade.ctx
            usr0,usr1 = trade.usrs[0],trade.usrs[1]
            await trade.channel.delete()
            await old_ctx.send(f'Trade successful between {usr0.mention} and {usr1.mention}')
            del trades[ctx.channel]
            currently_trading.remove(usr0.id)
            currently_trading.remove(usr1.id)

    @commands.command(name='trade-deny',hidden=True)
    @commands.check(trade_valid)
    async def _trade_deny(self,ctx):
        '''Denies the trade'''
        trade = trades[ctx.channel]
        old_ctx = trade.ctx
        usr0,usr1 = trade.usrs[0],trade.usrs[1]
        currently_trading.remove(usr0.id)
        currently_trading.remove(usr1.id)
        await trade.channel.delete()
        del trades[ctx.channel]
        await old_ctx.send(f'{ctx.author.mention} has denied the trade between {usr0.mention} and {usr1.mention}')

    async def on_message(self,ctx):
        #Update a dictionary every message, gaining xp every minute
        id = ctx.author.id
        await has_account(id)
        if id in times:
            if datetime.datetime.utcnow() - times[id] > datetime.timedelta(minutes=1):
                balance = cards_db.get_balance(id)
                cards_db.update_balance(id,balance + random.randint(20,40))
                times[id] = datetime.datetime.utcnow()
        else:
            times[id] = datetime.datetime.utcnow()

def setup(bot):
    bot.add_cog(CardGame(bot))
