from discord.ext import commands
import discord

from util import SurveyBuilder

DIGITS = ['1⃣','2⃣','3⃣','4⃣','5⃣','6⃣','7⃣','8⃣','9⃣','0⃣']
class Survey:

    def __init__(self, bot):
        self.bot = bot




    @commands.command(name='survey')
    async def _create_survey(self,ctx):
        '''Creates a survey with prompts'''
        user = ctx.author
        survey = SurveyBuilder.SurveyBuilder(user,ctx,self.bot)
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
