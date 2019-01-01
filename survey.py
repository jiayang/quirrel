from discord.ext import commands
import discord

DIGITS = ['1⃣','2⃣','3⃣','4⃣','5⃣','6⃣','7⃣','8⃣','9⃣','0⃣']
class Survey:

    def __init__(self, bot):
        self.bot = bot


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

        async def prompt(self,q,garbage):
            '''Helper to prompt user, returns response'''
            sent = await self.ctx.send(q)
            response = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
            garbage.append(sent)
            garbage.append(response)
            return response

        async def gset_title(self):
            '''Sets the title of the survey'''
            garbage = []
            response = await self.prompt('**Title Of Survey?:**',garbage)
            self.title = response.content
            await self.ctx.channel.delete_messages(garbage)
            if self.message == None:
                self.message = await self.ctx.send(embed = await self.format())
            else:
                await self.message.edit(embed=await self.format())

        async def gset_content(self):
            '''Fills the content of the survey'''
            garbage = []
            response = await self.prompt('**What is the question?:**',garbage)
            while response.content.startswith('.fix'):
                fgarbage = []
                fresponse = await self.prompt('**What do you need to fix?** (title) or Type .nvm to stop fix',fgarbage)
                if fresponse.content == '.nvm':
                    response = await self.prompt('**What is the question?:**',garbage)
                elif fresponse.content == 'title':
                    await self.gset_title()
                    response = await self.prompt('**What is the question?:**',garbage)
                await self.ctx.channel.delete_messages(fgarbage)
            self.content = response.content
            await self.ctx.channel.delete_messages(garbage)
            await self.message.edit(embed=await self.format())

        async def gset_answers(self):
            '''Asks for the range of answers in the survey'''
            prompt = await self.ctx.send('**What are the answer choices?:**\n(Type .done when all choices are completed. MAX 10 answers)')
            num_ans = 0
            while True:
                if num_ans == 10:
                    break
                garbage = []
                response = await self.prompt(f'**Choice {num_ans+1}:**',garbage) #Prompts the user
                while response.content.startswith('.fix'): #If they need to fix something else in the survey
                    fgarbage = []
                    fresponse = await self.prompt('**What do you need to fix?** (title,question,answers) or Type .nvm to stop fix',fgarbage) #Keep prompting them until they give valid response
                    await self.ctx.channel.delete_messages(fgarbage)
                    if fresponse.content == '.nvm': #Cancel the fix
                        response = await self.prompt(f'**Choice {num_ans+1}:**',garbage)
                    elif fresponse.content == 'title': #Fix the title, then go back to original
                        await self.gset_title()
                        response = await self.prompt(f'**Choice {num_ans+1}:**',garbage)
                    elif fresponse.content == 'question': #Fix the question, then go back to original
                        await self.gset_content()
                        response = await self.prompt(f'**Choice {num_ans+1}:**',garbage)
                    elif fresponse.content == 'answers': #Fix the answer
                        qgarb = []
                        response = await self.prompt(f'**Which number do you need to fix?**',qgarb) #Forces them to select a valid number
                        await self.ctx.channel.delete_messages(qgarb)
                        regret = False
                        while (not response.content.isdigit() or (int(response.content) <= 0 or int(response.content) > num_ans)) and not regret:
                            response = await self.prompt(f'**Which number do you need to fix?**',qgarb)
                            if response.content == '.nvm': #If they don't want to fix answers
                                regret = True
                            await self.ctx.channel.delete_messages(qgarb)
                        if not regret: #If they had an answer they wanted to fix
                            fixn = int(response.content)
                            response = await self.prompt(f'**Choice {fixn}:**',garbage)
                            self.answers[fixn-1] = response.content
                        response = await self.prompt(f'**Choice {num_ans+1}:**',garbage) #Go back to original
                await self.ctx.channel.delete_messages(garbage)
                if response.content == '.done': #If they are done, break out of the loop
                    break
                else:
                    num_ans += 1
                    self.answers += [response.content] #Else add their answer to aggregation
                    await self.message.edit(embed=await self.format()) #Show updated preview of the survey
            await prompt.delete()

        def author_check(self,message):
            return message.author == self.author

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

    @commands.command(name='survey')
    async def _create_survey(self,ctx):
        '''Creates a survey with prompts'''
        user = ctx.author
        survey = self.SurveyBuilder(user,ctx,self.bot)
        sent = await ctx.send(f'**Now creating survey** {user.mention}')
        #Fills in each entry of the survey
        await survey.gset_title()
        await survey.gset_content()
        await survey.gset_answers()
        #Cleanup
        await survey.message.delete()
        await sent.delete()
        await ctx.message.delete()
        survey_role = discord.utils.get(ctx.guild.roles, name='survey')
        survey_tag = ''
        if survey_role != None:
            survey_tag = survey_role.mention
        msg = await ctx.send(embed=await survey.format(), content = survey_tag)
        #Add reacs
        for i in range(len(survey.answers)):
            await msg.add_reaction(DIGITS[i])


def setup(bot):
    bot.add_cog(Survey(bot))
