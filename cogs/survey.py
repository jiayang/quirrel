from discord.ext import commands
import discord

from util import SurveyBuilder

DIGITS = ['1⃣','2⃣','3⃣','4⃣','5⃣','6⃣','7⃣','8⃣','9⃣','0⃣']
VERIFIED = ['default','halloween']
class Survey(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.images = {}
        f = open('data/surveyimages.csv')
        for line in f.read().strip().split():
            data = line.strip().split(',')
#            print(data)
            self.images[data[0]] = data[1]
#        print(self.images)
        self.update_image("default")
    


    @commands.command(name='survey')
    async def _create_survey(self,ctx):
        '''Creates a survey with prompts'''
        user = ctx.author
        survey = SurveyBuilder.SurveyBuilder(user,ctx,self.bot,self.image)
        sent = await ctx.send(f'**Now creating survey** {user.mention}')
        #Fills in each entry of the survey
        await survey.gset_title()
        await survey.gset_content()
        # await survey.gset_image()
        await survey.gset_answers()
        await survey.gset_image()
        #Cleanup
        await survey.message.delete()
        await sent.delete()
        await ctx.message.delete()
        survey_role = discord.utils.get(ctx.guild.roles, name='survey')
        survey_tag = ''
        if survey_role != None:
            # pass                
            survey_tag = survey_role.mention
        msg = await ctx.send(embed=await survey.format(), content = survey_tag)
        #Add reacs
        for i in range(len(survey.answers)):
            await msg.add_reaction(DIGITS[i])


    @commands.command(name='seticon', hidden=True)
    async def _changeicon(self,ctx, *args):
        '''Changes the icon in the survey'''
        user = ctx.author
        if user.id not in {166573846642688001: "Pyro", 208353857992916992: "Sound", 178663053171228674: "gbt"}:
            return
        self.update_image(args[0])
        await ctx.send('Changed the icon to **' + args[0] + '**') 
        await ctx.message.delete()
    @commands.command(name='addicon', hidden=True)
    async def _addicon(self,ctx, *args):
        '''Adds an icon to the library'''
        user = ctx.author
        if user.id not in {166573846642688001: "Pyro", 208353857992916992: "Sound", 178663053171228674: "gbt"}:
            return
        if args[0] in self.images:
            await ctx.message.delete()
            await ctx.send("That already exists!")
        self.images[args[0]] = args[1]
        s = ','.join(args) + '\n'
        f = open('data/surveyimages.csv','a')
        f.write(s)
        f.close()
        await ctx.message.delete()
        await ctx.send(f'Added icon **{args[0]}** to the library of icons. It looks like this {args[1]}.')

    @commands.command(name='icons', hidden=True)
    async def _icons(self,ctx):
        '''Displays all the icons'''
        user = ctx.author
        if user.id not in {166573846642688001: "Pyro", 208353857992916992: "Sound", 178663053171228674: "gbt"}:
            return
        ans = ''
        #print(self.images)
        for iconname in self.images.keys():
            #print(iconname)
            s = '\n'.join([iconname, self.images[iconname]]) + '\n'
            ans += s
        await ctx.message.delete()
        await ctx.send(ans) 

    @commands.command(name='delicon', hidden=True)
    async def _deleteicon(self,ctx,arg):
        if arg in VERIFIED:
            await ctx.message.delete()
            await ctx.send("You can not remove that! That image is gameboytre certified")
            return
        del self.images[arg]
        ans = ''
        for iconname in self.images.keys():
            s = ''.join([iconname, self.images[iconname]]) + '\n'
            ans += s
        f = open('data/surveybuilder.csv','w')
        f.write(ans)
        f.close()
        await ctx.message.delete()
        await ctx.send(f'Removed icon {arg}')

        
    def update_image(self,name):
        self.image = self.images[name]
                    
def setup(bot):
    bot.add_cog(Survey(bot))
