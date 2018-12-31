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

        async def gset_title(self):
            '''Sets the title of the survey'''
            sent = await self.ctx.send('**Title Of Survey?:**')
            response = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
            self.title = response.content
            await sent.delete()
            await response.delete()
            if self.message == None:
                self.message = await self.ctx.send(embed = await self.format())
            else:
                await self.message.edit(embed=await self.format())

        async def gset_content(self):
            '''Fills the content of the survey'''
            sents = [await self.ctx.send('**What is the question?:**')]
            response = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
            responses = [response]
            while response.content.startswith('.fix'):
                fix = await self.ctx.send('**What do you need to fix?** (title) or Type .nvm to stop fix')
                fresponse = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
                if fresponse.content == '.nvm':
                    sent = await self.ctx.send('**What is the question?:**')
                    sents.append(sent)
                    response = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
                    responses.append(response)
                elif fresponse.content == 'title':
                    await self.gset_title()
                    sent = await self.ctx.send('**What is the question?:**')
                    sents.append(sent)
                    response = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
                    responses.append(response)
                await fix.delete()
                await fresponse.delete()
            self.content = response.content
            await self.ctx.channel.delete_messages(sents + responses)
            await self.message.edit(embed=await self.format())

        async def gset_answers(self):
            '''Asks for the range of answers in the survey'''
            prompt = await self.ctx.send('**What are the answer choices?:**\n(Type .done when all choices are completed. MAX 10 answers)')
            num_ans = 0
            while True:
                if num_ans == 10:
                    break
                sent = await self.ctx.send(f'**Choice {num_ans+1}:**') #Prompts the user
                response = await self.bot.wait_for('message', check=self.author_check, timeout = 120) #Waits for response
                sents = [sent]
                responses = [response]
                while response.content.startswith('.fix'):
                    fix = await self.ctx.send('**What do you need to fix?** (title,question,answers) or Type .nvm to stop fix')
                    fresponse = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
                    if fresponse.content == '.nvm':
                        sent = await self.ctx.send(f'**Choice {num_ans+1}:**')
                        sents.append(sent)
                        response = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
                        responses.append(response)
                    elif fresponse.content == 'title':
                        await self.gset_title()
                        sent = await self.ctx.send(f'**Choice {num_ans+1}:**')
                        sents.append(sent)
                        response = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
                        responses.append(response)
                    elif fresponse.content == 'question':
                        await self.gset_content()
                        sent = await self.ctx.send(f'**Choice {num_ans+1}:**')
                        sents.append(sent)
                        response = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
                        responses.append(response)
                    elif fresponse.content == 'answers':
                        sent = await self.ctx.send('**Which number do you need to fix?**')
                        sents.append(sent)
                        response = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
                        responses.append(response)
                        regret = False
                        while (not response.content.isdigit() or (int(response.content) <= 0 or int(response.content) > num_ans)) and not regret:
                            sent = await self.ctx.send('**Which number do you need to fix?**')
                            response = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
                            if response.content == '.nvm':
                                regret = True
                        if not regret:
                            await sent.delete()
                            await response.delete()
                            fixn = int(response.content)
                            sent = await self.ctx.send(f'**Choice {fixn}:**')
                            response = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
                            self.answers[fixn-1] = response.content
                        await sent.delete()
                        await response.delete()
                        sent = await self.ctx.send(f'**Choice {num_ans+1}:**')
                        sents.append(sent)
                        response = await self.bot.wait_for('message', check=self.author_check, timeout = 120)
                        responses.append(response)
                    await fix.delete()
                    await fresponse.delete()
                if response.content == '.done': #If they are done, break out of the loop
                    await self.ctx.channel.delete_messages(sents + responses)
                    break
                else:
                    num_ans += 1
                    self.answers += [response.content] #Else add their answer to aggregation
                    await self.message.edit(embed=await self.format()) #Show updated preview of the survey
                    await self.ctx.channel.delete_messages(sents + responses)
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
                ans = ':one: Answer goes here'
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
