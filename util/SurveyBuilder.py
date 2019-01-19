from discord.ext import commands
import discord

from util import dio

DIGITS = ['1⃣','2⃣','3⃣','4⃣','5⃣','6⃣','7⃣','8⃣','9⃣','0⃣']

class SurveyBuilder:
    '''A builder to create the survey'''
    def __init__(self,author,ctx,bot):
        self.author = author
        self.ctx = ctx
        self.bot = bot
        self.title = None
        self.content = None
        self.answers = []
        self.message = None



    async def gset_title(self):
        '''Sets the title of the survey'''
        garbage = []
        response = await dio.prompt(self.ctx,'**Title Of Survey?:**',garbage)
        if response.content[0] == '!':
            await self.ctx.channel.delete_messages(garbage)
            return False
        self.title = response.content
        await self.ctx.channel.delete_messages(garbage)
        if self.message == None:
            self.message = await self.ctx.send(embed = await self.format())
        else:
            await self.message.edit(embed=await self.format())
        return True
    async def gset_content(self):
        '''Fills the content of the survey'''
        garbage = []
        response = await dio.prompt(self.ctx,'**What is the question?:**',garbage)
        if response.content[0] == '!':
            await self.ctx.channel.delete_messages(garbage)
            return False
        while response.content.startswith('.fix'):
            fgarbage = []
            fresponse = await dio.prompt(self.ctx,'**What do you need to fix?** (title) or Type .nvm to stop fix',fgarbage)
            if fresponse.content[0] == '!':
                await self.ctx.channel.delete_messages(fgarbage)
                await self.ctx.channel.delete_messages(garbage)
                return False
            if fresponse.content == '.nvm':
                response = await dio.prompt(self.ctx,'**What is the question?:**',garbage)
            elif fresponse.content == 'title':
                await self.gset_title()
                response = await dio.prompt(self.ctx,'**What is the question?:**',garbage)
            await self.ctx.channel.delete_messages(fgarbage)
        if response.content[0] == '!':
            await self.ctx.channel.delete_messages(garbage)
            return False
        self.content = response.content
        await self.ctx.channel.delete_messages(garbage)
        await self.message.edit(embed=await self.format())
        return True
    async def gset_answers(self):
        '''Asks for the range of answers in the survey'''
        prompt = await self.ctx.send('**What are the answer choices?:**\n(Type .done when all choices are completed. MAX 10 answers)')
        num_ans = 0
        while True:
            if num_ans == 10:
                break
            garbage = []
            response = await dio.prompt(self.ctx,f'**Choice {num_ans+1}:**',garbage) #Prompts the user
            if response.content[0] == '!':
                await self.ctx.channel.delete_messages(garbage)
                return False
            while response.content.startswith('.fix'): #If they need to fix something else in the survey
                fgarbage = []
                fresponse = await dio.prompt(self.ctx,'**What do you need to fix?** (title,question,answers) or Type .nvm to stop fix',fgarbage) #Keep prompting them until they give valid response
                if fresponse.content[0] == '!':
                    await self.ctx.channel.delete_messages(fgarbage)
                    await self.ctx.channel.delete_messages(garbage)
                    return False
                await self.ctx.channel.delete_messages(fgarbage)
                if fresponse.content == '.nvm': #Cancel the fix
                    response = await dio.prompt(self.ctx,f'**Choice {num_ans+1}:**',garbage)
                elif fresponse.content == 'title': #Fix the title, then go back to original
                    await self.gset_title()
                    response = await dio.prompt(self.ctx,f'**Choice {num_ans+1}:**',garbage)
                elif fresponse.content == 'question': #Fix the question, then go back to original
                    await self.gset_content()
                    response = await dio.prompt(self.ctx,f'**Choice {num_ans+1}:**',garbage)
                elif fresponse.content == 'answers': #Fix the answer
                    qgarb = []
                    qresponse = await dio.prompt(self.ctx,f'**Which number do you need to fix?**',qgarb) #Forces them to select a valid number
                    await self.ctx.channel.delete_messages(qgarb)
                    regret = False
                    while (not qresponse.content.isdigit() or (int(qresponse.content) <= 0 or int(qresponse.content) > num_ans)) and not regret:
                        qresponse = await dio.prompt(self.ctx,f'**Which number do you need to fix?**',qgarb)
                        if qresponse.content[0] == '!':
                            await self.ctx.channel.delete_messages(qgarbage)
                            await self.ctx.channel.delete_messages(fgarbage)
                            await self.ctx.channel.delete_messages(garbage)
                            return False
                        if qresponse.content == '.nvm': #If they don't want to fix answers
                            regret = True
                        await self.ctx.channel.delete_messages(qgarb)
                    if not regret: #If they had an answer they wanted to fix
                        fixn = int(response.content)
                        response = await dio.prompt(self.ctx,f'**Choice {fixn}:**',garbage)
                        self.answers[fixn-1] = response.content
                    response = await dio.prompt(self.ctx,f'**Choice {num_ans+1}:**',garbage) #Go back to original
            await self.ctx.channel.delete_messages(garbage)
            if response.content[0] == '!':
                await self.ctx.channel.delete_messages(garbage)
                return False
            if response.content == '.done': #If they are done, break out of the loop
                break
            else:
                num_ans += 1
                self.answers += [response.content] #Else add their answer to aggregation
                await self.message.edit(embed=await self.format()) #Show updated preview of the survey
        await prompt.delete()
        return True

    async def format(self):
        '''Formats the string builder to the actual str sent'''
        embed = discord.Embed(title=f'**{self.title}**', color = 16744272)
        ans = ''
        for i in range(len(self.answers)):
            ans += DIGITS[i] + ' ' + self.answers[i] + '\n'
        if ans == '':
            ans = '_Leave your answers below_'
        if self.content != None:
            embed.add_field(name=self.content, value = ans + '\n')
        embed.set_footer(text=f'Requested by {self.author.name} | {self.author.id}')
        embed.set_thumbnail(url='https://imgur.com/huTrrHV.jpg')
        return embed

def setup(bot):
    pass
