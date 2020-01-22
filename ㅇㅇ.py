import discord
from discord.ext import commands
import asyncio
import youtube_dl
import os
from discord.utils import get

client = commands.Bot(command_prefix = ',')

@client.event
async def on_ready():
    print('command bot online')

@client.command()
@commands.has_permissions(manage_messages=True)
async def 청소(ctx, amount=99):
    await ctx.channel.purge(limit=amount)
    await ctx.send('청소 완료 @_@')

@client.event
async def on_message(message):
    filter = ["전언영", "ㄴㄱㅁ", "느금마"]
    user = message.author

    for word in filter:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)
            await message.channel.send(f'{user.mention} 님 욕설은 나빠요 ㅜㅜ 그런 말은 삼가해주세요 ..')
        await client.process_commands(message)


@client.event
async def on_message(message):
    filter = ["식량귀여워"]
    user = message.author

    for word in filter:
        if message.content.count(word) > 0:
            await message.channel.send(f'{user.mention} 님 ㅋ 저도 알아여 ^~^')
        await client.process_commands(message)

@client.command(pass_context=True)
async def 입장(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"{channel}에 입장했습니다.")

@client.command(pass_context=True)
async def 퇴장(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"{channel}에서 퇴장했습니다.")

@client.command(pass_context=True, aliases=['p', '노래'])
async def 재생(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("해당 큐에 더 이상 곡이 없습니다.\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("해당 노래가 등록되었습니다.")
                print(f"해당 노래는 {still_q} 번째 노래 입니다.")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No Songs were queued before the ending of the last song\n")


    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("오래된 song.mp3 파일을 삭제 했습니다.")
    except PermissionError:
        print("노래가 재생되고 있거나 파일을 지울 권한이 없어 노래를 지울 수 없습니다.")
        await ctx.send("오류 : 이미 노래가 플레이되고 있습니다.")
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("오래된 폴더를 삭제했습니다.")
            shutil.rmtree(Queue_folder)
    except:
        print("더 이상 오래된 폴더가 없습니다.")

    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("노래를 다운 받는 중 입니다.")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"{nname[0]} 곡을 재생합니다.")
    print("playing\n")


@client.command(pass_context=True, aliases=['pause'])
async def 멈춤(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("음악을 멈췄습니다.")
        voice.pause()
        await ctx.send("음악 재생을 멈추었습니다.")
    else:
        print("음악이 플레이 되고 있지 않습니다.")
        await ctx.send("음악이 플레이 되고 있지 않습니다.")

@client.comamnd(pass_context=True, aliases=['resume'])
async def 재생(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("음악을 재생합니다.")
        voice.resume()
        await ctx.send("음악을 다시 재생합니다.")
    else:
        print("음악이 플레이 되고 있지 않습니다.")
        await ctx.send("음악이 플레이 되고 있지 않습니다.")

@client.comamnd(pass_context=True, aliases=['skip', 's', 'ㄴ'])
async def 스킵(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    user = message.author

    queues.clear()

    if voice and voice.is_playing():
        print("음악을 스킵했습니다.")
        voice.stop()
        await ctx.send(f"{user.mention} 님이 음악을 스킵했습니다.")
    else:
        print("음악이 플레이 되고 있지 않습니다.")
        await ctx.send("음악이 플레이 되고 있지 않습니다.")


queues = {}

@client.comamnd(pass_context=True, aliases=['queue', 'q'])
async def 재생목록(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queue[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song(q_num).%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youyube_dl.YouyubeDL(ydl_opts) as ydl:
        print("오디오를 다운 중 입니다.\n")
        ydl.download([url])
    await ctx.send("해당 노래를 " + " " + str(q_num) + " " + "번으로 추가하였습니다.")

    print("노래가 추가되었습니다.\n")

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
