import discord
import markovify


#handling the txt files for markovify
filename_m = "meanings.txt"
filename_w = "words.txt"
filename_q = "question.txt"

file_m = open(filename_m)
file_w = open(filename_w)
file_q = open(filename_q)

text_m = file_m.read()
text_w = file_w.read()
text_q = file_q.read()

word_list = ['word']
meaning_list = ['meaning']

#connecting to Discord
client = discord.Client()


#Event to come online
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#Event to handle any message on the server
@client.event
async def on_message(message):
    #to extract username, message and channel that is input on the server
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    #to stop bot from infinitely responding to its own message
    if message.author == client.user:
        return

    if message.channel.name == 'word-generator':
        if user_message.lower() =='hi' or user_message.lower() == 'hello':
            await message.channel.send(f'Hi {username}!')
            return
        elif user_message.lower() == 'question':
            model_q = markovify.Text(text_q,state_size=2)
            await message.channel.send(f'The question :   {model_q.make_sentence()}')
            return

        elif user_message.lower() == 'word please':
            model_m = markovify.Text(text_m,state_size=2)
            model_w = markovify.Text(text_w,state_size=1)
            word = model_w.make_sentence()[0:12]
            meaning = model_m.make_sentence()

            while(word in word_list or not word):
                word = model_w.make_sentence()[0:12]
            word_list.append(word)

            while(meaning in meaning_list or not meaning):
                meaning = model_m.make_sentence()

            meaning_list.append(meaning)


            await message.channel.send(f'The new word I created is :   {word}\nAnd it means :   {meaning}')
            return

        elif user_message.lower() == 'bye':
            await message.channel.send(f'See ya {username}!')
            return


client.run(TOKEN)