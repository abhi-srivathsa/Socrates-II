import discord
import markovify
import openai
import pandas as pd
from decouple import config
import re
import random


openai.api_key = config('openai.api_key')
TOKEN = config('TOKEN')

#handling the txt files for markovify
filename_m = "meanings.txt"
filename_w = "words.txt"
filename_q = "question.txt"
filename_s = "socratesQuotes.txt"
#input = pd.read_csv('philosophy_data.csv')

#opening the txt files
file_m = open(filename_m)
file_w = open(filename_w)
file_q = open(filename_q)
file_s = open(filename_s)

#reading the txt files
text_m = file_m.read()
text_w = file_w.read()
text_q = file_q.read()
text_s = file_s.read()

#maintaining unique word and meaning list to ensure no duplication occurs during any session
word_list = ['word']
meaning_list = ['meaning']

#connecting to Discord
intents = discord.Intents.all()

client = discord.Client(intents=intents)

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

    if message.channel.name == 'conversation-with-socrates':
        if user_message.lower() =='hi' or user_message.lower() == 'hello':
            await message.channel.send(f'Hi {username}, I am **Socrates II** or **S2** for short. \n\n I am named after Socrates who is credited to be the first human philosopher. I am learning as much as possible to be the first Computer philosopher. \n\n *Do you have any questions for me or could I interest you in a philosophical thought or a question I am wondering about?*')
            return
        elif 'historical philosophy' in user_message.lower():
            # model_t = markovify.NewlineText(input.sentence_str, state_size = 2)
            # thought = model_t.make_sentence()
            # response = openai.Completion.create(
            #     engine="text-davinci-001",
            #     prompt="Correct this to standard English:\n\n" + thought,
            #     temperature=0,
            #     max_tokens=60,
            #     top_p=1.0,
            #     frequency_penalty=0.0,
            #     presence_penalty=0.0
            # )
            # response2 = openai.Completion.create(
            #     engine="text-davinci-001",
            #     prompt="Summarize this for a second-grade student:\n\n" + response['choices'][0]['text'],
            #     temperature=0.7,
            #     max_tokens=64,
            #     top_p=1.0,
            #     frequency_penalty=0.0,
            #     presence_penalty=0.0
            # )
            # response3 = openai.Completion.create(
            #     engine="text-davinci-001",
            #     prompt="Create an analogy for this phrase:\n\n" + response['choices'][0]['text'],
            #     temperature=0.5,
            #     max_tokens=60,
            #     top_p=1.0,
            #     frequency_penalty=0.0,
            #     presence_penalty=0.0
            # )
            #
            # await  message.channel.send("Here's an interesting thought")
            # await message.channel.send(response['choices'][0]['text'])
            # await message.channel.send(f'Let me further explain what I am talking about')
            # await message.channel.send(response2['choices'][0]['text'])
            # await message.channel.send(response3['choices'][0]['text'])
            #print(input.index)

            #index = random.randint(1,360000)
            #await message.channel.send("Here's a statement from **" + input.loc[index].title + "** written by **" + input.loc[index].author + "**")
            #await message.channel.send("*" + input.loc[index].sentence_str + "*")

            return

        elif  'question' in user_message.lower():
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
                prompt="Summarize this for a second-grade student:\n\n" + response['choices'][0]['text'],
                temperature=0.7,
                max_tokens=64,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            await message.channel.send(f'Here is a compelling question \n'+"**"+response['choices'][0]['text']+"**")
            await message.channel.send(f'\n\nLet me further explain what I am talking about\n')
            await message.channel.send(response2['choices'][0]['text'])
            return

        elif 'new word' in user_message.lower():
            model_m = markovify.Text(text_m,state_size=2)
            model_w = markovify.Text(text_w,state_size=1)

            # removing white spaces and periods
            text2 = re.sub(r"\s+", "", text_w)
            text3 = re.sub(r"[\.]", "", text2)
             # getting a random starting letter
            starting = random.choice(text3)
            # generating a word with the random starting letter
            word = model_w.make_sentence_with_start(starting)[0:12]
            meaning = model_m.make_sentence()
            word2 = re.sub(r"\s+", "", word)
            word3 = re.sub(r"[\.]", "", word2)

            while(word in word_list or not word):
                word = model_w.make_sentence_with_start(starting)()[0:12]
            word_list.append(word)

            while(meaning in meaning_list or not meaning):
                meaning = model_m.make_sentence()

            meaning_list.append(meaning)
            await message.channel.send(f'The new word I created is **{word3}**.\n The definition of *{word3}* is \n **{meaning}**')
            return

        elif 'thought' in user_message.lower():
            model_s = markovify.Text(text_s,state_size=2)
            socratesThought = model_s.make_sentence()
            response = openai.Completion.create(
                engine="text-davinci-001",
                prompt="Correct this to standard English:\n\n" + socratesThought,
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
            await message.channel.send("Here's an interesting thought :: "+"**"+response['choices'][0]['text']+"**")
            await message.channel.send(f'Let me further explain what I am talking about')
            await message.channel.send(response2['choices'][0]['text'])
            return

        elif user_message.lower() == 'bye':
            await message.channel.send(f'See ya {username}!')
            return
        else:
            print(user_message.lower())
            start_sequence = "\nA: "
            restart_sequence = "\n\nQ: "
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=restart_sequence + user_message + start_sequence,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            if response['choices'][0]['text'] != '':
                await message.channel.send(response['choices'][0]['text'])
            return


client.run(TOKEN)
