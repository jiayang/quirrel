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
            response = await self.bot.wait_for('message', check=self.author_check, timeout = 30)
            self.title = response.content
            await sent.delete()
            await response.delete()
            self.message = await self.ctx.send('━━━━━━━━━━━━━━━━\n'  + await self.format() + '\n━━━━━━━━━━━━━━━━')

        async def gset_content(self):
            '''Fills the content of the survey'''
            sent = await self.ctx.send('**What is the question?:**')
            response = await self.bot.wait_for('message', check=self.author_check, timeout = 30)
            self.content = response.content
            await sent.delete()
            await response.delete()
            await self.message.edit(content= '━━━━━━━━━━━━━━━━\n'  + await self.format() + '\n━━━━━━━━━━━━━━━━')

        async def gset_answers(self):
            '''Asks for the range of answers in the survey'''
            prompt = await self.ctx.send('**What are the answer choices?:**\n(Type .done when all choices are completed. MAX 10 answers)')
            num_ans = 0
            while True:
                if num_ans == 10:
                    break
                sent = await self.ctx.send(f'**Choice {num_ans+1}:**') #Prompts the user
                response = await self.bot.wait_for('message', check=self.author_check, timeout = 30) #Waits for response
                if response.content == '.done': #If they are done, break out of the loop
                    await sent.delete()
                    await response.delete()
                    break
                else:
                    num_ans += 1
                    self.answers += [response.content] #Else add their answer to aggregation
                    await self.message.edit(content='━━━━━━━━━━━━━━━━\n'  + await self.format() + '\n━━━━━━━━━━━━━━━━') #Show updated preview of the survey
                    await sent.delete()
                    await response.delete()
            await prompt.delete()

        def author_check(self,message):
            return message.author == self.author

        async def format(self):
            '''Formats the string builder to the actual str sent'''
            survey_role = discord.utils.get(self.ctx.guild.roles, name='survey')
            survey_tag = ''
            if survey_role != None:
                survey_tag = survey_role.mention
            msg = ''
            msg += f'**{self.title}**\n'
            if self.content != None:
                msg += self.content + survey_tag + '\n\n'
            for i in range(len(self.answers)):
                msg += DIGITS[i] + ' ' + self.answers[i] + '\n'
            return msg

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
        msg = await ctx.send(await survey.format())
        #Add reacs
        for i in range(len(survey.answers)):
            await msg.add_reaction(DIGITS[i])


def setup(bot):
    bot.add_cog(Survey(bot))
