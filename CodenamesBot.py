import discord
from discord.ext import commands
from discord.ui import Button, View
import random

english_words = [
    "apple", "book", "car", "dog", "elephant", "fish", "goat", "house", "igloo", "juice",
    "kite", "lamp", "mouse", "nest", "orange", "pencil", "queen", "rabbit", "sun", "tree",
    "umbrella", "vase", "watch", "xylophone", "yak", "zebra", "airplane", "banana", "cookie", "duck",
    "egg", "frog", "giraffe", "hat", "ice cream", "jacket", "key", "lion", "moon", "notebook",
    "ocean", "pizza", "quilt", "rose", "snake", "table", "unicorn", "volcano", "watermelon", "xylophone",
    "yo-yo", "zeppelin", "ant", "ball", "cat", "desk", "elephant", "feather", "guitar", "hat",
    "ink", "jelly", "kangaroo", "lemon", "mango", "nail", "ocean", "pear", "quilt", "rabbit",
    "star", "train", "umbrella", "violin", "water", "xylophone", "yacht", "zebra", "apple", "bag",
    "cup", "door", "elephant", "fan", "grapes", "hat", "ice", "jacket", "kite", "lemonade",
    "milk", "notebook", "orange", "piano", "quilt", "rose", "sun", "table", "umbrella", "violin",
    "watermelon", "xylophone", "yogurt", "zebra", "antelope", "butterfly", "cat", "dog", "elephant", "flower",
    "guitar", "horse", "ice cream", "jellyfish", "kite", "lion", "monkey", "nest", "owl", "peach",
    "queen", "rose", "sun", "tree", "unicorn", "vase", "water", "xylophone", "yak", "zeppelin",
    "apple", "bear", "cat", "dog", "elephant", "frog", "giraffe", "horse", "ice cream", "jacket",
    "kite", "lion", "monkey", "nest", "owl", "pear", "queen", "rose", "sun", "tree", "umbrella",
    "volcano", "watermelon", "xylophone", "yogurt", "zebra", "airplane", "banana", "cookie", "dog", "elephant",
    "fish", "giraffe", "hat", "ice cream", "jacket", "key", "lemon", "moon", "nest", "orange",
    "pizza", "queen", "rose", "sun", "tree", "umbrella", "volcano", "watermelon", "xylophone", "yak",
    "zebra", "apple", "ball", "cat", "dog", "elephant", "feather", "guitar", "hat", "ice cream",
    "jacket", "key", "lemon", "mango", "notebook", "orange", "pizza", "queen", "rose", "sun",
    "tree", "umbrella", "volcano", "watermelon", "xylophone", "yogurt", "zebra", "antelope", "butterfly", "cat",
    "dog", "elephant", "flower", "guitar", "horse", "ice cream", "jellyfish", "kite", "lion", "monkey",
    "nest", "owl", "peach", "queen", "rose", "sun", "tree", "umbrella", "volcano", "watermelon",
    "xylophone", "yogurt", "zebra", "apple", "bear", "cat", "dog", "elephant", "frog", "giraffe",
    "horse", "ice cream", "jacket", "kite", "lion", "monkey", "nest", "owl", "pear", "queen",
    "rose", "sun", "tree", "umbrella", "volcano", "watermelon", "xylophone", "yogurt", "zebra", "antelope",
    "butterfly", "cat", "dog", "elephant", "flower", "guitar", "horse", "ice cream", "jellyfish", "kite",
    "lion", "monkey", "nest", "owl", "peach", "queen", "rose", "sun", "tree", "umbrella",
    "volcano", "watermelon", "xylophone", "yogurt", "zebra"
]


players={'BlueTeam':[],'RedTeam':[],'RedSpy':[],'BlueSpy':[]}
game_status={'started':False,'whostarted':'',"words":[],'players_ready':[],'total':0,'confirmed':False,'players':[],
             'redwords':[],'bluewords':[],'blackword':None,"turn":'red',"words_guessed":[],'hint_given':False}


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

class StartView(View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(label="Join Blue Team", style=discord.ButtonStyle.primary, custom_id="btn_BlueTeam"))
        self.add_item(Button(label="Join Red Team", style=discord.ButtonStyle.danger, custom_id="btn_RedTeam"))
        self.add_item(Button(label="Join Blue Spymaster", style=discord.ButtonStyle.primary, custom_id="btn_BlueSpy",emoji='🕵️'))
        self.add_item(Button(label="Join Red Spymaster", style=discord.ButtonStyle.danger, custom_id="btn_RedSpy",emoji='🕵️'))
        self.add_item(Button(label="Exit", style=discord.ButtonStyle.gray, custom_id="btn_exit",emoji='❌'))


class BoardView(View):
    def __init__(self):
        super().__init__()

        j=0
        for i in range(1, 21):

            if game_status["words"][i-1] in game_status["words_guessed"]:

                if game_status["words"][i-1] in game_status["redwords"]:
                    button = Button(
                        label=game_status["words"][i-1], 
                        style=discord.ButtonStyle.red, 
                        custom_id=game_status["words"][i-1], 
                        row=j
                    )
                elif game_status["words"][i-1] in game_status["bluewords"]:

                    button = Button(
                        label=game_status["words"][i-1], 
                        style=discord.ButtonStyle.blurple, 
                        custom_id=game_status["words"][i-1], 
                        row=j
                    )
                else:
                    button = Button(
                        label=game_status["words"][i-1], 
                        style=discord.ButtonStyle.gray, 
                        custom_id=game_status["words"][i-1], 
                        row=j
                    )
            else:
                button = Button(
                        label=game_status["words"][i-1], 
                        style=discord.ButtonStyle.gray, 
                        custom_id=game_status["words"][i-1], 
                        row=j
                    )


            if i%4==0:
                j+=1
            self.add_item(button)


class SpyMasterView(View):
    def __init__(self):
        super().__init__()
        j=0
        k=0
        for i in game_status['words']:

            if i in game_status["redwords"]:
                self.add_item(Button(label=i, style=discord.ButtonStyle.danger, custom_id=f"spy_{i}",row=j))
            elif i in game_status["bluewords"]:
                self.add_item(Button(label=i, style=discord.ButtonStyle.blurple, custom_id=f"spy_{i}",row=j))
            elif i == game_status["blackword"]:
                self.add_item(Button(label=i, style=discord.ButtonStyle.green, custom_id=f"spy_{i}",row=j))
            else:
                self.add_item(Button(label=i, style=discord.ButtonStyle.grey, custom_id=f"spy_{i}",row=j))
            
            k+=1
            if k%4==0:
                j+=1            




class ReadyView(View):
    def __init__(self):
        super().__init__()

        if not(len(game_status["words"])>0):
            while True:
                randomword=random.choice(english_words)
                if not(randomword in game_status["words"]):
                    game_status["words"].append(randomword)
                if len(game_status["words"])==20:
                    break    

        if not(len(game_status["redwords"])>0):
            while True:
                randomword=random.choice(game_status["words"])
                if not((randomword in game_status["redwords"])) and (not(randomword in game_status["bluewords"])):
                    game_status["redwords"].append(randomword)
                if len(game_status["redwords"])==7:
                    break     

        if not(len(game_status["bluewords"])>0):
            while True:
                randomword=random.choice(game_status["words"])
                if not((randomword in game_status["redwords"])) and (not(randomword in game_status["bluewords"])):
                    game_status["bluewords"].append(randomword)
                if len(game_status["bluewords"])==6:
                    break        

    
        while True:
            randomword=random.choice(game_status["words"])
            if not((randomword in game_status["redwords"])) and (not(randomword in game_status["bluewords"])):
                game_status["blackword"]=randomword
            if game_status["blackword"]:
                break                


        print(game_status["blackword"])
        print(game_status["redwords"])
        print(game_status["bluewords"])
        self.add_item(Button(label="Ready ✅", style=discord.ButtonStyle.success, custom_id="btn_Ready"))    


class OptionView(View):
    def __init__(self):
        super().__init__()

        self.add_item(Button(label="SpyMaster View", style=discord.ButtonStyle.green, custom_id="btn_SpyMasterView"))
        
        self.add_item(Button(label="EndGuessing", style=discord.ButtonStyle.success, custom_id="btn_EndGuessing"))










@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user} (ID: {bot.user.id})')


@bot.command(name='board')
async def board(ctx):
    view=BoardView()
    await ctx.send("board:",view=view)
    view=OptionView()
    await ctx.send('Options: ',view=view)

@bot.command(name="confirm")
async def confirm(ctx):
    if (game_status["started"]==True):
        if ctx.author.mention==game_status["whostarted"]:
            game_status["confirmed"]=True
            game_status['players']=players["BlueSpy"]+players["BlueTeam"]+players["RedSpy"]+players["RedTeam"]
            game_status["total"]=len(players["BlueSpy"])+len(players["RedSpy"])+len(players["RedTeam"])+len(players["BlueTeam"])
            view=ReadyView()
            msg=f"Number of Players Ready:{len(game_status['players_ready'])} / {game_status["total"]}"
            await ctx.send(msg,view=view)
        else:
            await ctx.send("Only the Host can confirm the teams")    
    else:
        await ctx.send('Start the game first')

@bot.command(name='start')
async def button(ctx):
    if game_status['started']==False:
        game_status["whostarted"]=ctx.author.mention
        game_status["started"]=True
       
        view =StartView()
        msg=f"RedTeam:{ players["RedTeam"]} \n BlueTeam:{ players["BlueTeam"]} \n Blue Spymaster::{ players["BlueSpy"]}  \n Red Spymaster::{ players["RedSpy"]} "
        
        await ctx.send(msg, view=view)
    else:
        await ctx.send ("Game has already been Started")


@bot.command(name='hint')
async def hintfucntion(ctx):
    if ctx.author.mention in players["RedSpy"] and game_status["turn"]=='red' and game_status["started"] and game_status["confirmed"]: 
        game_status["hint_given"]=True
        await ctx.send("Red Team can guess now")
    if ctx.author.mention in players["BlueSpy"] and game_status["turn"]=='blue' and game_status["started"] and game_status["confirmed"]: 
        game_status["hint_given"]=True
        await ctx.send("Blue Team can guess now")    







@bot.command(name='stop')
async def stopfucntion(ctx):
    if ctx.author.mention == game_status["whostarted"]: 
        players["BlueSpy"]=[]
        players["RedSpy"]=[]
        players["BlueTeam"]=[]
        players["RedTeam"]=[]
        game_status["started"]=False
        game_status["whostarted"]=""
        game_status["words"]=[]
        game_status["confirmed"]=False
        game_status["total"]=0
        game_status["players_ready"]=[]
        game_status["blackword"]=None
        game_status["bluewords"]=[]
        game_status["redwords"]=[]
        game_status["words_guessed"]=[]
        game_status["turn"]='red'

        
        await ctx.send("Game Ended! You Can Start a New Game Now.")
    else:
        await ctx.send('Only the person who started the game can end.')    
     

@bot.event
async def on_interaction(interaction: discord.Interaction):
    
    # print (dir(interaction))
    # print(interaction.user.mention)
    # print(dir(interaction.response))

    if interaction.data["custom_id"] in ['btn_RedSpy','btn_BlueSpy','btn_RedTeam','btn_BlueTeam','btn_exit']:
        print(69)
        await startviewfunction(inter=interaction)

    if interaction.data["custom_id"]=='btn_Ready'   :
         await readyviewfucntion(inter=interaction) 

    if interaction.data["custom_id"]=="btn_SpyMasterView" :
        await spymasterviewfunction(inter=interaction)

    if interaction.data["custom_id"] in game_status["words"]:
        await wordguessedfunction(inter=interaction)


async def wordguessedfunction(inter):
    if inter.user.mention in game_status['players'] and game_status["hint_given"]:
        print('inside 1')
        if inter.data['custom_id'] == game_status["blackword"]:
            players["BlueSpy"]=[]
            players["RedSpy"]=[]
            players["BlueTeam"]=[]
            players["RedTeam"]=[]
            game_status["started"]=False
            game_status["whostarted"]=""
            game_status["words"]=[]
            game_status["confirmed"]=False
            game_status["total"]=0
            game_status["players_ready"]=[]
            game_status["blackword"]=None
            game_status["bluewords"]=[]
            game_status["redwords"]=[]
            game_status["words_guessed"]=[]
            game_status["turn"]='red'
            await inter.response.send_message('Game Over , It was a black Word !!')
        
        else:    
            print('inside 2')   
            if inter.user.mention in players["RedTeam"] and game_status["turn"]=='red':
                print('inside 3')
                if not(inter.data['custom_id'] in game_status["redwords"]):
                    game_status["turn"]='blue'
                    game_status["hint_given"]=False
                    await inter.channel.send("Wrong Guess , Blue Team's Turn now")

    

                
                game_status["words_guessed"].append(inter.data['custom_id'])
                view=BoardView()
                await inter.response.edit_message(content="Board:",view=view)


            elif  inter.user.mention in players["BlueTeam"] and game_status["turn"]=='blue':  

                if not(inter.data['custom_id'] in game_status["bluewords"]):
                    game_status["turn"]='red'
                    game_status["hint_given"]=False
                    await inter.channel.send("Wrong Guess , Red Team's Turn now")

                game_status["words_guessed"].append(inter.data['custom_id'])
                view=BoardView()
                await inter.response.edit_message(content="Board:",view=view)
            
            else:
                await inter.response.send_message("Not Your Turn !",ephemeral=True)    

            


async def spymasterviewfunction(inter):
    if (inter.user.mention in players["RedSpy"] or inter.user.mention in players["BlueSpy"]) :
        view= SpyMasterView()
        await inter.response.send_message("SpymasterBoardView:",view=view,ephemeral=True)
    else:
         await inter.response.send_message("You are not a SpyMaster",ephemeral=True)

async def readyviewfucntion(inter):
    if game_status["confirmed"]==True and game_status["started"]==True:

        print(game_status['players'])
        print(game_status['players_ready'])
        print(game_status['total'])

        if inter.user.mention in game_status["players_ready"]:
            await inter.response.send_message("You Have already clicked on Ready!",  ephemeral=True)
        
        elif inter.user.mention in game_status["players"]:
            
            
            game_status["players_ready"].append(inter.user.mention)
            
            
            if len(game_status["players_ready"])==game_status["total"]:
                msg=f"Number of Players Ready:{len(game_status['players_ready'])} / {game_status['total']}"
                await inter.response.edit_message(content=msg)
                view=BoardView()
                await inter.channel.send("board:",view=view)
                view=OptionView()
                await inter.channel.send("Options:",view=view)

            else:    
                msg=f"Number of Players Ready:{len(game_status['players_ready'])} / {game_status['total']}"
                await inter.response.edit_message(content=msg)




async def startviewfunction(inter):

    if game_status["confirmed"]==False:
        print('6969')
        if inter.data["custom_id"] == "btn_BlueTeam" and not((inter.user.mention in players["BlueTeam"]) ):
            if inter.user.mention in players["RedTeam"]:
                (players['RedTeam']).remove(inter.user.mention)
            if inter.user.mention in players["RedSpy"]:
                (players['RedSpy']).remove(inter.user.mention)   
            if inter.user.mention in players["BlueSpy"]:
                (players['BlueSpy']).remove(inter.user.mention)
            if inter.user.mention in players["BlueTeam"]:
                (players['BlueTeam']).remove(inter.user.mention)       

            players["BlueTeam"].append(inter.user.mention)
            msg=f"RedTeam:{ players["RedTeam"]} \n BlueTeam:{ players["BlueTeam"]} \n Blue Spymaster::{ players["BlueSpy"]}  \n Red Spymaster::{ players["RedSpy"]} "
            await inter.response.edit_message(content=msg)
        


        elif inter.data["custom_id"] == "btn_RedTeam" and not((inter.user.mention in players["RedTeam"])):
            if inter.user.mention in players["RedTeam"]:
                (players['RedTeam']).remove(inter.user.mention)
            if inter.user.mention in players["RedSpy"]:
                (players['RedSpy']).remove(inter.user.mention)   
            if inter.user.mention in players["BlueSpy"]:
                (players['BlueSpy']).remove(inter.user.mention)
            if inter.user.mention in players["BlueTeam"]:
                (players['BlueTeam']).remove(inter.user.mention)     
        
            players["RedTeam"].append(inter.user.mention)
            msg=f"RedTeam:{ players["RedTeam"]} \n BlueTeam:{ players["BlueTeam"]} \n Blue Spymaster::{ players["BlueSpy"]}  \n Red Spymaster::{ players["RedSpy"]} "
            await inter.response.edit_message(content=msg)





        elif inter.data["custom_id"] == "btn_RedSpy" and not((inter.user.mention in players["RedSpy"])):
            if inter.user.mention in players["RedTeam"]:
                (players['RedTeam']).remove(inter.user.mention)
            if inter.user.mention in players["RedSpy"]:
                (players['RedSpy']).remove(inter.user.mention)   
            if inter.user.mention in players["BlueSpy"]:
                (players['BlueSpy']).remove(inter.user.mention)
            if inter.user.mention in players["BlueTeam"]:
                (players['BlueTeam']).remove(inter.user.mention)
            players["RedSpy"].append(inter.user.mention)
            msg=f"RedTeam:{ players["RedTeam"]} \n BlueTeam:{ players["BlueTeam"]} \n Blue Spymaster::{ players["BlueSpy"]}  \n Red Spymaster::{ players["RedSpy"]} "
            await inter.response.edit_message(content=msg)    
    
        



        elif inter.data["custom_id"] == "btn_BlueSpy" and not((inter.user.mention in players["BlueSpy"])):
            if inter.user.mention in players["RedTeam"]:
                (players['RedTeam']).remove(inter.user.mention)
            if inter.user.mention in players["RedSpy"]:
                (players['RedSpy']).remove(inter.user.mention)   
            if inter.user.mention in players["BlueSpy"]:
                (players['BlueSpy']).remove(inter.user.mention)
            if inter.user.mention in players["BlueTeam"]:
                (players['BlueTeam']).remove(inter.user.mention) 
            players["BlueSpy"].append(inter.user.mention)
            msg=f"RedTeam:{ players["RedTeam"]} \n BlueTeam:{ players["BlueTeam"]} \n Blue Spymaster::{ players["BlueSpy"]}  \n Red Spymaster::{ players["RedSpy"]} "
            await inter.response.edit_message(content=msg)    
        
        elif inter.data["custom_id"] == "btn_exit":
            if inter.user.mention in players["RedTeam"]:
                (players['RedTeam']).remove(inter.user.mention)
            if inter.user.mention in players["RedSpy"]:
                (players['RedSpy']).remove(inter.user.mention)   
            if inter.user.mention in players["BlueSpy"]:
                (players['BlueSpy']).remove(inter.user.mention)
            if inter.user.mention in players["BlueTeam"]:
                (players['BlueTeam']).remove(inter.user.mention) 
            
            msg=f"RedTeam:{ players["RedTeam"]} \n BlueTeam:{ players["BlueTeam"]} \n Blue Spymaster::{ players["BlueSpy"]}  \n Red Spymaster::{ players["RedSpy"]} "
            await inter.response.edit_message(content=msg)  



        else:
            await inter.response.send_message("you are already in one of the teams")

        print(players)   

    else:
        await inter.response.send_message("Teams have been confirmed!")    





bot.run('MTI1MjI5NDU0MjMwNTI2MzczOA.G-0NfN.XRcxsKeAV9hA0mIaU3yvGdlmWAEjuKur6I-YBY')