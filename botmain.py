import discord 
from discord.ext import commands
import asyncio
import random
import os
import json
from PIL import Image
import glob
import string

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

files = os.path.join(os.getcwd(), "bot/meme")

bot = commands.Bot(command_prefix='$', intents=intents)

class singlebutton(discord.ui.View):
      def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
      @discord.ui.button(label="this button will explode if clicked", style = discord.ButtonStyle.blurple, emoji=None)
      async def button_callback(self, interaction:discord.Interaction, button:discord.ui.Button):
          button.label = "bro pressed it"
          button.style = discord.ButtonStyle.danger
          await interaction.response.edit_message(content=f"i copied this somewhere", view=self)
          if button.style == discord.ButtonStyle.danger:
              button.disabled = True
              await interaction.message.delete()

class triobuttons(discord.ui.View): # class of buttons that let you choose between picture 1, same, picture 2 
      def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.decision = None

      @discord.ui.button(label="picture 1", style = discord.ButtonStyle.blurple, emoji=None)
      async def button1(self, interaction:discord.Interaction, button:discord.ui.Button):
          button.label = "pressed"
          for child in self.children:
            if type(child) == discord.ui.Button:
             child.disabled = True
            self.decision = 0
          await interaction.response.edit_message(view=self)
          self.stop()
          

      @discord.ui.button(label="same", style = discord.ButtonStyle.red, emoji=None)
      async def button2(self, interaction:discord.Interaction, button:discord.ui.Button):
          button.label = "pressed"
          for child in self.children:
            if type(child) == discord.ui.Button:
             child.disabled = True
            self.decision = 1
          await interaction.response.edit_message(view=self)
          self.stop()
          

      @discord.ui.button(label="picture 2", style = discord.ButtonStyle.green, emoji=None)
      async def button3(self, interaction:discord.Interaction, button:discord.ui.Button):
          button.label = "pressed"
          for child in self.children:
            if type(child) == discord.ui.Button:
             child.disabled = True
          self.decision = 2   
          await interaction.response.edit_message(view=self)
          self.stop()
          
def compareratings(image, image2):
    with open("bot/ratings.json") as r:
       rating = json.load(r)
       imager1 = str(*rating[image])
       imager2 = str(*rating[image2])

       if imager1 > imager2:
           return "0"
       if imager2 > imager1:
           return "2"
       else: 
           return "1"

@bot.event
async def on_ready(): #when bot logs in, change status and game played
     print(f'logged in as {bot.user}')
     await bot.change_presence(status=discord.Status.online, activity= discord.Game("evil ratings and the like"))

@bot.command()
async def lebutton(ctx): #spawns a button that is deleted upon click
     await ctx.send("do NOT touch this", view = singlebutton())

@bot.command() # random command that takes only one argument, anything fits
async def dollar(ctx, arg):
    await ctx.send("yeah" + " "+ arg + " " + "dollars" + " " + "what do you think of that")
    await asyncio.sleep(2.5)
    await ctx.send('https://tenor.com/view/bruh-swag-savage-burn-owned-gif-5251169') 

# returns jegs/bot/meme/randomimage.jpg  vvvv
def sortimages():
    randomfile = random.choice(os.listdir(files))
    yield os.path.join(files, randomfile)
    yield randomfile

@bot.command()
async def pleasework(ctx):
        file = sortimages()
        await ctx.send("ok", file=discord.File(next(file)))
        with open('bot/ratings.json') as r:
            awesomerating = json.load(r) 
            await ctx.send("your image is:" + " given a score of " + str(*awesomerating[next(file)]))
            #await ctx.send("type $scale if you wish to see criterion")

@bot.command()
async def scale(ctx):
     await ctx.send("SCALE: \n10 Very funny, can get many laughs when viewing, timeless classic\n 9  Funny for a while\n 8  Giggle upon viewing\n 7  Nose sniff\n 6 Smirk\n 5  Indifferent\n 4  Ok bro\n 3 a little annoying\n 2 upsetting\n 1 Disgust\n ps i am not you and these ratings dont matter" )

@bot.command()
async def embedtest(ctx): #send 2 embeds, each containing an image whith their own score
     
     file = sortimages()
     filepath1 = next(file)
     filename1 = next(file)

     embed1 = discord.Embed(title= 'img 1')

     e1m = discord.File(filepath1, filename = filename1) 

     embed1.set_image(url='attachment://' + filename1)
    
     with open('bot/ratings.json') as r:
      awesomerating = json.load(r) 
      embed1.set_footer(text= 'given a ' + str(*awesomerating[filename1]))
     
     await ctx.send(file = e1m, embed = embed1)
     
     #####

     file2 = sortimages()
     filepath2 = next(file2)
     filename2 = next(file2)

     embed2 = discord.Embed(title= 'img 2')

     e2m = discord.File(filepath2, filename = filename2) 

     embed2.set_image(url='attachment://' + filename2)

     with open('bot/ratings.json') as r:
      awesomerating = json.load(r) 
      embed2.set_footer(text= 'given a ' + str(*awesomerating[filename2]))

     await ctx.send(file = e2m, embed = embed2)

def namegenerator():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for n in range (5))

def tengen(im1, im2): #grabs name from generator, merges images, then saves
  
    name = namegenerator()

    oi = Image.open(im1)
    oi2 = Image.open(im2)
    oi3 = (name)
    size = 480, 270 

    oi.thumbnail(size=size)
    oi2.thumbnail(size=size)

    width = oi.size[0] + oi2.size[0]
    if oi.size[1] > oi2.size[1]:
        height = oi.size[1]
    else:
        height = oi2.size[1]
    newim = Image.new("RGBA", (width, height))

    newim.paste(oi)
    newim.paste(oi2, (oi.size[0], 0))

    newim.save(("C:/Users/HP/Documents/jegs/bot/picturebuffer"+ "/" + str(oi3) + ".png"))
    yield oi3
   

#grabs latest file in buffer folder
def tengengrabber():
    bufferlist = glob.glob("C:/Users/HP/Documents/jegs/bot/picturebuffer/*") #grab all names of files in this folder
    latest_file = max(bufferlist, key=os.path.getctime)   #sort until you get the one that has the earliest creation time 
    yield latest_file
    
    for files in os.walk("C:/Users/HP/Documents/jegs/bot/picturebuffer/"): #attempts to remove files from buffer
          os.remove(files)
    

@bot.command()
async def eldritch(ctx): #combines two images together with pillow
    await ctx.typing()
    img1 = sortimages()
    fp1 = next(img1)
    fn1 = next(img1)

    img2 = sortimages()
    fp2 = next(img2)
    fn2 = next(img2)
    
    creator = tengen(fp1, fp2)
    namegrabber = next(creator)
    picgrabber = tengengrabber()
    newpic = next(picgrabber)
    
    embed1 = discord.Embed(title= "which ones funnier according to me")
    embed1.set_image(url= "attachment://" + namegrabber + ".png")
    embed1.set_footer(text = "this took hours")

    view = triobuttons()

    await ctx.send(embed = embed1, file=discord.File(newpic), view = view)
    
    await view.wait()

    ratingget = compareratings(fn1, fn2)
    finalrating = ratingget
   
    await ctx.typing()

    if str(view.decision) == str(finalrating):
        await ctx.send("your right!!! :exploding_head:  :exploding_head:  :exploding_head:")
    elif view.decision == None:
        await ctx.send("you did not pick :hearts:")
    if str(view.decision) != str(finalrating):
        await ctx.send("wrong!!!! :scream: :scream:")

    embed2 = discord.Embed(title="Ratings")
   # embed2.set_image(url= "attachment://" + fn1 + ".png")
    
    with open('bot/ratings.json') as r:
      awesomerating = json.load(r) 
      embed2.add_field(name= "Image 1", value= 'given a ' + str(*awesomerating[fn1]))

    embed3 = discord.Embed(title="image 2")
   # embed3.set_image(url= "attachment://" + fn2 + ".png")

    with open('bot/ratings.json') as r:
      awesomerating = json.load(r) 
      embed2.add_field(name="Image 2", value= 'given a ' + str(*awesomerating[fn2]))

    await ctx.send(embed = embed2)

    print ("the image that was funnier was image" + str(finalrating) + " (1 means same)")





@bot.command()
@commands.is_owner()
async def updatenamelist(ctx):
     with open("bot/list.txt", "w", newline="") as list:
          for filenames in os.walk('bot/meme'):
               list.write(str(filenames)+ "\n")
     await ctx.send("will do i hope")




@bot.command()
async def pingstupidperson(ctx):
     person = random.choice(ctx.guild.members)
     print(ctx.guild.members)
     await ctx.send("yrour stupid" + " " + person.mention)
     await ctx.send("https://tenor.com/view/yakuza-3-kiryu-kazuma-heat-action-substory-like-a-dragon-3-gif-14088234543096594634")


bot.run("TOKEN")
 
