from discord.ext import commands
import discord

from util import cards_db,cards

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
        #Setup the prompting message and the realtime trade viewer
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
        #Formats the offers
        s = ''
        if self.money[i] != 0:
            s += f'{self.money[i]} Big Bucks\n'
        offers = cards.format(self.offers[i])
        s += '\n'.join(offers)
        if s == '':
            s = 'Not offering anything currently'
        return s

    async def add(self,usr,args):
        #For each item listed
        i = 0 if usr == self.usrs[0] else 1
        self.confirm = [False,False]
        for arg in args:
            #If it is an int (want to add bigbucks)
            if arg.strip().isdigit():
                val = int(arg)
                balance = cards_db.get_balance(usr.id)
                if val + self.money[i] > balance:
                    await self.channel.send(content=f"You can not afford that! Your current balance is {balance}")
                    continue
                self.money[i] += val
                await self.channel.send(content=f"{usr.mention} added {val} Big Bucks to the trade.")
            else:
            #If it is a card
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
        #Almost the same as add
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
        await self.channel.send(content=f"{usr.mention} has accepted the current trade. {self.usrs[i*-1+1].mention}, type !trade-accept to accept!")
