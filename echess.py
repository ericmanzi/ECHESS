#open_analysis
#v1.5


import subprocess, time, argparse, datetime, re



#argument parser
parser=argparse.ArgumentParser(description="to analyse game, cd to location of game")
parser.add_argument('--engine',default='stockfish', help='Select analysis engine. Options are \
komodo, stockfish(default), houdini or rybka')
parser.add_argument('--hashValue', help='Set the value in MB as memory for \
hash tables. Default value is 32')
parser.add_argument('--multiPV', help='Set the number of best lines that the \
engine is considering. This slows down the chess engine a lot so it is not \
advisable to change it if you want it at full strength. Default value is 1')
parser.add_argument('--time', help='Set the time (in seconds) that the engine \
spends searching on a single move')
parser.add_argument('--game', help='game takes the name of the pgn file you \
want to be analysed. File has to be in the same directory')
parser.add_argument('-analyse', action='store_true', help='takes no arguments. \
set this argument to begin analysis')

#set class to receive parameters from command line as namespace
class x:
    hashValue='32'
    multiPV='1'
    time='1'
    engine='stockfish'
    game='onegame.pgn'
args=parser.parse_args(args=None, namespace=x)


#set engine
engine_loc='komodo-5-64bit.exe'
if x.engine=='komodo':
    engine_loc='komodo-5-64bit.exe'
elif x.engine=='stockfish':
    engine_loc='stockfish_14053109_x64.exe'
elif x.engine=='gull':
    engine_loc='Gull 3 x64.exe'
elif x.engine=='houdini':
    engine_loc='Houdini_15a_x64.exe'

#initialize stdin and stdout PIPEs
engine = subprocess.Popen(
    engine_loc,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)
#init loggy to receive text to be written to log.txt
loggy=''

#write @param command + \n to stdin
def put(command):
    global loggy
    print command
    putlog='\n\nOpen_Analysis: \n'+command
    log.write(putlog)
    engine.stdin.write(command+'\n')

#receive stdout/ output from engine
def get():
    global loggy
    engine.stdin.write('isready\n')
    print('\nengine:')
    getlog='\n\nengine:\n'
    while True:
        text=engine.stdout.readline().strip()
        if text=='readyok':
            break
        if text!='':
            print '\t'+text
            getlog+=text+'\n'
    log.write(getlog)

#Create analysis log file
log=open('log.txt', 'w+',)
log.write("Analysis of "+x.game+"\n"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+'\n')
loggytags='\n\n'

game_file=open(x.game, 'r') #open game
game_string=''.join(game_file.readlines())  #join lines in game to form 1 string
game_list=game_string.split('[Event ')  #split game string into individual games
new_game_list=[]
for i in game_list[1:]: #add back '[event ' which was deleted during split
    j='[Event '+i
    new_game_list.append(j)
num_games=0  #initiate count of number of games in file
num_games=len(new_game_list)
games=[]
if num_games<2: #if we're dealing with only one game
    moves_string=''    #initialise movs_string
    for line in game_string.splitlines():  #separate moves and game info
        if line!='':
            if line[0]!='[' and line[0]!='\n':
                moves_string+=line
                moves=moves_string.split(' ')
            elif line[0]=='[' or line[0]=='\n':
                loggytags+=line+'\n'    #write tags to log

    #create moves_list from moves_string by splitting at space
    games=[moves]

else: #if we have more than one game
    moves_string='' #initialise moves string
    for game in new_game_list:  #loop through new_game_list, 
        loggytags='\n\n'
        for line in game.splitlines():   #for each game, separate moves and game info
            if line!='':
                if line[0]!='[' and line[:2]!='\n':
                    moves_string+=line  #add moves to moves_string
                    moves=moves_string.split(' ')#create moves lists from moves_string
                elif line[0]=='[' or line[:2]=='\n':
                    loggytags+=line+'\n'
               
        moves_string=''
        games.append(moves) #append moves lists to games

#analyze a game; start new game, and analyze each position in game
def Analyze_game(moves):
    get()
    put('uci')
    get()
    put('setoption name Hash value %s'%x.hashValue)
##    get()
##    put('setoption name UCI_AnalyseMode value true')
##    get()
    put('setoption name MultiPV value %s'%x.multiPV)
    get()
    put('ucinewgame')
    get()
    put_statement='position startpos moves '
    searchmoves=''
    for move in moves:
        put('setoption name Clear Hash')
        put(put_statement+move)
        get()
        put('go movetime '+str(int(x.time)*1000))
        time.sleep(int(x.time)+0.1)
        get()
        if moves.index(move)!=len(moves)-1:
            put('go movetime '+str(int(x.time)*1000)+' searchmoves '+moves[moves.index(move)+1])
            time.sleep(int(x.time)+0.1)
            get()

        put_statement+=move+' '



#re-formats the output log file to a format that facilitates analysis

def log2echess():
    af=open('log.echess', 'w+')
    af.write('oaChess 1.0 by Eric Manzi\nechess format\n')

    def hr():
        af.write('\n'+'-'*50+'\n\n')
        pass

    log2=open('log.txt', 'r',)
    log2tagsstring=''.join(log2.readlines())
    game_list=log2tagsstring.split('[Event ')
    af.write(game_list[0]+'\n\n')

    game_list_plus=[]
    for i in game_list[1:]:
        j='[Event '+i
        game_list_plus.append(j)




    for game in game_list_plus:
        p2=re.compile(r'(\[.*\])')
        tags=p2.split(game)
        for line in tags[:-1]:
            af.write(line)
        #get engine id
        engineid=re.search(r'id name.*\b', tags[-1]).group()[8:]

        af.write('\n[Plycount "16"]')
        af.write('\n[EngineID "'+engineid+'"]\n')

        hr()

        #get list of moves in game
        startposreg=re.compile(r'(position startpos moves.*\b)')
        startposes=re.findall(startposreg, tags[-1])



        #split game into positions
        splitsville=startposreg.split(game)[:-1]
        bestmovereg=re.compile(r'\bbestmove.*\b')
        p1=re.compile(r"\bcp [+-]?\d+(?:\.\d+)? nodes\b") #get the string, s containing score
##        p2=re.compile(r"[+-]?\d+(?:\.\d+)?") #get the score from string s
##        pgull=re.compile(r"\bcp [+-]?\d+\b")
        phoud=re.compile(r"\bcp [+-]?\d+  time\b")
        p2=re.compile(r"[+-]?\d+\b")
        pd1=re.compile(r"\bdepth \d+\b") #get the string d, containing depth
        pd2=re.compile(r"\d+") #get the depth from string d
        tuplist=[] #init list of tuple with position and info on that position


        for item in splitsville:
            position, bestmove, bmscore, bmdepth, playermove, pmscore, pmdepth='','','0.0','0','','0.0','0'
            if item[:23]=='position startpos moves' and splitsville.index(item)<len(splitsville)-1:
                position=item[24:]
                innext=splitsville[splitsville.index(item)+1]
                bestmoves=bestmovereg.findall(innext)
                if len(bestmoves)>1:
                    bestmove=bestmoves[0][9:13]
                    playermove=bestmoves[1][9:13]

                lines=innext.splitlines()
                if x.engine=='houdini':
                    info1=lines[lines.index(bestmoves[0])-1]
                    bestscoretxt=phoud.search(info1)
                    
                elif x.engine=='stockfish':
                    info1=lines[lines.index(bestmoves[0])-2]
                    bestscoretxt=p1.search(info1)
                if bestscoretxt==None:
                    pass
                else:
                    bestscore=p2.search(bestscoretxt.group())
                    bmscore=bestscore.group()
                bestdepthtxt=pd1.search(info1)
                if bestdepthtxt==None:
                    pass
                else:
                    bestdepth=p2.search(bestdepthtxt.group())
                    bmdepth=bestdepth.group()
                
                if len(bestmoves)<2:
                    pass
                else:
                    if x.engine=='houdini':
                        info2=lines[lines.index(bestmoves[1])-1]
                        pscoretxt=phoud.search(info2)
                    elif x.engine=='stockfish':
                        info2=lines[lines.index(bestmoves[1])-2]
                        pscoretxt=p1.search(info2)
                        
                    if pscoretxt==None:
                        pass
                    else:                    
                        pscore=p2.search(pscoretxt.group())
                        pmscore=pscore.group()
                    pdepthtxt=pd1.search(info2)
                    if pdepthtxt==None:
                        pass
                    else:
                        pdepth=p2.search(pdepthtxt.group())
                        pmdepth=pdepth.group()
                
                tuplist.append((position,bestmove,bmscore,bmdepth,playermove,pmscore,pmdepth))


        playermoves="1."+tuplist[0][0]+"<>{}  "
        enginemoves="1. -- <>{}  "
        tupcount=2
        for i in tuplist:
            playermoves+=str(tupcount)+"."+i[4]+"<"+i[5]+">{"+i[6]+"}  "
            enginemoves+=str(tupcount)+"."+i[1]+"<"+i[2]+">{"+i[3]+"}  "
            tupcount+=1


        af.write('Move chosen by player <score> {depth}: '+playermoves)
        af.write('\nEngine\'s best move    <score> {depth}: '+enginemoves)
            

        hr()

    af.close()

#call Analyze_game repetitively on games in batch
def Analyze_batch():
    for game in games:
        log.write(loggytags)
        Analyze_game(game)

def run():
    Analyze_batch()
    put('quit')
    log2echess()
    subprocess.call(["notepad.exe", "log.txt"])

if args.analyse:
    run()

