from discord.ext import commands
import discord

DIGITS = ['1⃣','2⃣','3⃣','4⃣','5⃣','6⃣','7⃣','8⃣','9⃣','0⃣']
REVERSE_DIGITS = {
    '1⃣' : 0,
    '2⃣' : 1,
    '3⃣' : 2,
    '4⃣' : 3,
    '5⃣' : 4,
    '6⃣' : 5,
    '7⃣' : 6,
    '8⃣' : 7,
    '9⃣' : 8,
    '0⃣' : 9
}

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = dict() #Key is the "interactive message" Value is the actual game


    @commands.command(name='connect-four',)
    async def _connectfour(self,ctx):
        '''Play a game of Connect Four!'''
        a = Connect_Four(self.bot, ctx,self)
        await a.setup()
        self.games[a.io.id] = a

    async def on_reaction_add(self,reaction,user):
        message = reaction.message
        if user.bot or message.id not in self.games:
            return
        await self.games[message.id].next(reaction)
        await reaction.remove(user)



PIECE = {
    'blue' : '🔵',
    'red' : '🔴',
    'empty' : '⚪'
}
# 0 -> Empty
# 1 -> Blue
# 2 -> Red
BASIS_VECTORS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

class Connect_Four:
    def __init__(self,bot,ctx,games):
        self.bot = bot
        self.ctx = ctx
        self.games = games
        self.messages = [] #index 0 is the top
        self.board = []
        self.io = None
        self.embed = None
        self.embed_message = None
        self.turn = True #True is blue, False is red

    async def setup(self):
        ctx = self.ctx
        for i in range(6):
            #Add the six rows of 7 pieces
            row = [0,0,0,0,0,0,0]
            self.board.append(row)
            to_send = self.format_list(row)
        for i in range(2):
            to_send = ''
            #Store the messages
            for j in range(3):
                to_send += self.format_list(self.board[i * 3 + j]) + '\n'
            self.messages.append(await ctx.send(to_send))
        self.io = self.messages[-1]
        for i in range(7):
            await self.io.add_reaction(DIGITS[i])

        #Embed for the UX
        embed = discord.Embed(title="**Connect Four: Blue's Turn**", color = 16744272)
        embed.set_author(name=self.bot.user.name, icon_url = self.bot.user.avatar_url)
        embed.description = f"[Rules](http://www.boardgamecapital.com/connect-four-rules.htm) To place a piece, add a reaction to the corresponding column."
        embed.set_thumbnail(url='https://i.imgur.com/SIzZAzP.jpg')
        self.embed = embed
        self.embed_message = await ctx.send(embed=embed)

    async def next(self,reaction):
        '''A reaction is added to the interactive message'''
        n = REVERSE_DIGITS[reaction.emoji] #The number represented by the rxn
        place = None #Figure out which place the new piece should go
        for i in range(6):
            if self.board[5-i][n] == 0:
                place = 5-i
                break
        if place == None:
            return None

        if self.turn:
            self.board[place][n] = 1
            self.embed.title = "**Connect Four: Red's Turn!**"
        else:
            self.board[place][n] = 2
            self.embed.title = "**Connect Four: Blue's Turn!**"

        self.turn = not self.turn #Flip the turns

        to_send = ''
        for i in range(3):
            to_send += self.format_list(self.board[((place // 3) * 3 + i)]) + '\n'
        await self.messages[place // 3].edit(content=to_send) #Edit the board shown

        check = await self.check_win() #Check to see if anyone has won
        if check == 1:
            self.embed.title = "**Connect Four: Blue Wins!**"
            del self.games.games[self.io.id]
        if check == 2:
            self.embed.title = "**Connect Four: Red Wins!**"
            del self.games.games[self.io.id]
        if check == -1:
            self.embed.title = "**Connect Four: Draw!**"
            del self.games.games[self.io.id]
        await self.embed_message.edit(embed=self.embed)

    async def check_win(self):
        #Checks for wins by iterating through every direction for every piece
        count = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                v = self.board[i][j]
                if v == 0:
                    continue
                count += 1
                for vector in BASIS_VECTORS:
                    m = 1
                    dr = vector[0]
                    dc = vector[1]
                    newr = i + dr * m
                    newc = j + dc * m
                    while newr >= 0 and newr < len(self.board) and newc >= 0 and newc < len(self.board[i]) and self.board[newr][newc] == v:
                        m += 1
                        newr = i + dr * m
                        newc = j + dc * m
                        if m == 4:
                            return v
        if count == 42:
            return -1

    def format_list(self,row):
        #Returns a string used for displaying to users
        row = [str(i) for i in row]
        s = '    '.join(row)
        return s.replace('2',PIECE['red']).replace('1',PIECE['blue']).replace('0',PIECE['empty'])

    def print_board(self):
        l = [str(e) for e in self.board]
        print('\n'.join(l) + '\n')













def setup(bot):
    bot.add_cog(Games(bot))
