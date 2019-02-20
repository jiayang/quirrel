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

trades = dict() #Channel -> TradeUnit
currently_trading = set()

async def trade_valid(ctx):
    if ctx.channel not in trades:
        await ctx.send('Not in a valid trade chat')
        return False
    trade = trades[ctx.channel]
    if ctx.author not in trade.usrs:
        await ctx.send('You are not part of this trade')
        return False
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
        if id in currently_trading:
            await ctx.send(f"You are currently trading. Please complete the trade to sell.")
            return
        #If they do, remove the card, add the big bucks
        cards_db.remove_card(id,card_info['id'])
        balance = cards_db.get_balance(id)
        cards_db.update_balance(id,balance + int(card_info['value']))

        embed = discord.Embed(title=f"💰 Sold: **{card_info['name']}** 💰", color = 15834065)
        embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.description = f"Sold the card for {card_info['value']} Big Bucks."
        await ctx.send(embed=embed)

    @commands.command(name='value')
    async def _value(self,ctx,arg):
        card_info = cards.get_card(arg)
        if card_info == None:
            await ctx.send(f"There doesn't seem to be a **{arg}** in our records.")
            return
        embed = discord.Embed(title=f"**{card_info['name']}**", color = 15834065)
        embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.description = f"{card_info['name']} is a(n) {card_info['rarity']} and currently worth {card_info['value']} Big Bucks."
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
        if id not in [184002906981269505,178663053171228674]:
            pass
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
        channel = await ctx.guild.create_text_channel(name=f'trade-{ctx.author.display_name}-{usr1.display_name}', category = ctx.channel.category)
        a = TradeUnit(ctx,channel,ctx.author,usr1)
        trades[channel] = a
        await a.setup()
        currently_trading.add(id)
        currently_trading.add(usr1.id)

    @commands.command(name='trade-add',hidden=True)
    @commands.check(trade_valid)
    async def _trade_add(self,ctx,*arg):
        trade = trades[ctx.channel]
        await trade.add(ctx.author,arg)
        await ctx.message.delete()

    @commands.command(name='trade-remove',hidden=True)
    @commands.check(trade_valid)
    async def _trade_remove(self,ctx,*arg):
        trade = trades[ctx.channel]
        await trade.remove(ctx.author,arg)
        await ctx.message.delete()

    @commands.command(name='trade-accept',hidden=True)
    @commands.check(trade_valid)
    async def _trade_accept(self,ctx):
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
        if id in self.times:
            if datetime.datetime.utcnow() - self.times[id] > datetime.timedelta(minutes=1):
                balance = cards_db.get_balance(id)
                cards_db.update_balance(id,balance + random.randint(20,40))
                self.times[id] = datetime.datetime.utcnow()
        else:
            self.times[id] = datetime.datetime.utcnow()


class TradeUnit:

    def __init__(self,ctx,channel,usr0,usr1):
        self.ctx = ctx
        self.channel = channel
        self.usrs = (usr0,usr1)
        self.money = [0,0]
        self.offers = ([],[])
        self.confirm = [False,False]
        self.embeds = [None,None]
        self.embed_messages = [None,None]

    async def setup(self):
        await self.channel.send(content=f'created new trade for {self.usrs[0].mention}-{self.usrs[1].mention}\nTrade by using !trade-add, !trade-remove, !trade-accept, !trade-deny')
        for i in range(2):
            usr = self.usrs[i]
            embed = discord.Embed(title=f"{usr.name}'s Offers", color = 16744272)
            embed.set_author(name=usr.name, icon_url = usr.avatar_url)
            embed.add_field(name='Offering:', value=self.get_string(i))
            embed.set_thumbnail(url=usr.avatar_url)
            self.embeds[i] = embed
            self.embed_messages[i] = await self.channel.send(embed=embed)

    def get_string(self,i):
        s = ''
        if self.money[i] != 0:
            s += f'{self.money[i]} Big Bucks\n'
        offers = cards.format(self.offers[i])
        s += '\n'.join(offers)
        if s == '':
            s = 'Not offering anything currently'
        return s

    async def add(self,usr,args):
        i = 0 if usr == self.usrs[0] else 1
        self.confirm = [False,False]
        for arg in args:
            if arg.strip().isdigit():
                val = int(arg)
                balance = cards_db.get_balance(usr.id)
                if val > balance:
                    await self.channel.send(content=f"You can not afford that! Your current balance is {balance}")
                    continue
                self.money[i] += val
                await self.channel.send(content=f"{usr.mention} added {val} Big Bucks to the trade.")
            else:
                if len(self.offers[i]) > 15:
                    await self.channel.send(content=f"Sorry, due to Discord's limits you can only add up to 15 cards to a trade.")
                    continue
                card_info = cards.get_card(arg)
                usr_cards = cards_db.get_cards(usr.id)
                #The card does not exist
                if card_info == None:
                    await self.channel.send(content=f"There doesn't seem to be a **{arg}** in our records.")
                    continue
                #Check if the user has the card
                if int(card_info['id']) not in usr_cards:
                    await self.channel.send(content=f"You don't seem to have a copy of {card_info['name']}.")
                    continue

                count = usr_cards.count(int(card_info['id'])) #Number of the type of card
                offered_count = self.offers[i].count(int(card_info['id'])) #Number of offered
                if offered_count == count:
                    await self.channel.send(content=f"You already offered all **{count}** of your {card_info['name']}'s")
                    continue
                if offered_count > count:
                    await self.channel.send(content=f"Error: You offered more than you have! (Did you trade while trading?)\nRemoved excess offers for {card_info['name']}")
                    for j in range(offered_count-count):
                        self.offers[i].remove(int(card_info['id']))
                    continue
                self.offers[i].append(int(card_info['id']))
                await self.channel.send(content=f"{usr.mention} added {card_info['name']} to the trade.")
        self.embeds[i].set_field_at(index=0,name='Offering:',value=self.get_string(i))
        await self.embed_messages[i].edit(embed=self.embeds[i])

    async def remove(self,usr,args):
        i = 0 if usr == self.usrs[0] else 1
        self.confirm = [False,False]
        for arg in args:
            if arg.strip().isdigit():
                val = int(arg)
                offered = self.money[i]
                if val > offered:
                    await self.channel.send(content=f"You can not remove that! Your current Big Bucks offer is {offered}")
                    continue
                self.money[i] -= val
                await self.channel.send(content=f"{usr.mention} removed {val} Big Bucks from the trade.")
            else:
                card_info = cards.get_card(arg)
                usr_cards = self.offers[i]
                #The card does not exist
                if card_info == None:
                    await self.channel.send(content=f"There doesn't seem to be a **{arg}** in our records.")
                    continue
                #Check if the user has the card
                if int(card_info['id']) not in usr_cards:
                    await self.channel.send(content=f"It doesn't seem like you offered any {card_info['name']}'s.")
                    continue

                self.offers[i].remove(int(card_info['id']))
                await self.channel.send(content=f"{usr.mention} removed {card_info['name']} from the trade.")
        self.embeds[i].set_field_at(index=0,name='Offering:',value=self.get_string(i))
        await self.embed_messages[i].edit(embed=self.embeds[i])

    async def accept(self,usr):
        i = 0 if usr == self.usrs[0] else 1
        self.confirm[i] = True
        if self.confirm == [True,True]:
            id0 = self.usrs[0].id
            id1 = self.usrs[1].id
            balance0 = cards_db.get_balance(id0)
            balance1 = cards_db.get_balance(id1)
            cards_db.update_balance(id0,balance0 - self.money[0] + self.money[1]) #Updates balance
            cards_db.update_balance(id1,balance1 - self.money[1] + self.money[0]) #Updates balance
            for card_id in self.offers[0]:
                cards_db.remove_card(id0,card_id)
            for card_id in self.offers[1]:
                cards_db.remove_card(id1,card_id)
            cards_db.add_cards(id0,self.offers[1])
            cards_db.add_cards(id1,self.offers[0])
            return True
        await self.channel.send(content=f"{usr.mention} has accepted the current trade.")

def setup(bot):
    bot.add_cog(CardGame(bot))
