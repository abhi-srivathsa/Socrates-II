import discord
import markovify
import openai
import pandas as pd
from decouple import config

openai.api_key = config('openai.api_key')
TOKEN = config('TOKEN')

#handling the txt files for markovify
filename_m = "meanings.txt"
filename_w = "words.txt"
filename_q = "question.txt"
input = pd.read_csv('philosophy_data.csv')

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
        elif user_message.lower() == 'thought':
            model_t = markovify.NewlineText(input.sentence_str, state_size = 2)
            thought = model_t.make_sentence()
            response = openai.Completion.create(
                engine="text-davinci-001",
                prompt="Correct this to standard English:\n\n" + thought,
                temperature=0,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            response2 = openai.Completion.create(
                engine="text-davinci-001",
                prompt="Summarize this for a second-grade student:\n\n" + response['choices'][0]['text'],
                temperature=0.7,
                max_tokens=64,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            response3 = openai.Completion.create(
                engine="text-davinci-001",
                prompt="Create an analogy for this phrase:\n\n" + response['choices'][0]['text'],
                temperature=0.5,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            await  message.channel.send("Here's an interesting thought")
            await message.channel.send(response['choices'][0]['text'])
            await message.channel.send(f'Let me further explain what I am talking about')
            await message.channel.send(response2['choices'][0]['text'])
            await message.channel.send(response3['choices'][0]['text'])

            return

        elif user_message.lower() == 'question':
            model_q = markovify.Text(text_q,state_size=2)
            text_new = model_q.make_sentence()
            print(text_new)
            response = openai.Completion.create(
                engine="text-davinci-001",
                prompt="Correct this to standard English:\n\n" + text_new,
                temperature=0,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            response2 = openai.Completion.create(
                engine="text-davinci-001",
                prompt="Create an analogy for this phrase:\n\n" + response['choices'][0]['text'],
                temperature=0.5,
                max_tokens=60,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            await message.channel.send(response['choices'][0]['text'])
            await message.channel.send(f'Let me further explain what I am talking about')
            await message.channel.send(response2['choices'][0]['text'])
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
        else:
            print(user_message.lower())
            start_sequence = "\nA: "
            restart_sequence = "\n\nQ: "
            response = openai.Completion.create(
                engine="text-davinci-001",
                prompt=restart_sequence + user_message + start_sequence,
                temperature=0,
                max_tokens=100,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["\t"]
            )
            if response['choices'][0]['text'] != '':
                await message.channel.send(response['choices'][0]['text'])
            return


client.run(TOKEN)
