import requests
import discord
import datetime
from discord.ext import commands
from dateutil import parser
import os
from dotenv import load_dotenv

load_dotenv()

APIKEY = os.getenv('VTGEMS_API_KEY')
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='!')

url = f'https://vtgems.com/api/EventOccurrences?access_token={APIKEY}&filter=%7B%22where%22%3A%7B%22and%22%3A%5B%7B%22approved%22%3Atrue%7D%2C%7B%22endTime%22%3A%7B%22gte%22%3A%22{datetime.datetime.now()}%22%7D%7D%2C%7B%22or%22%3A%5B%7B%22visibleAfter%22%3A%7B%22lte%22%3A%22{datetime.datetime.now()}%22%7D%7D%2C%7B%22visibleAfter%22%3A%7B%22eq%22%3Anull%7D%7D%5D%7D%5D%7D%2C%22include%22%3A%5B%7B%22event%22%3A%22committee%22%7D%2C%22signedUp%22%5D%2C%22order%22%3A%22startTime%20ASC%22%2C%22counts%22%3A%5B%22signedUp%22%2C%22waitlisted%22%5D%7D'
jsonResponse = requests.get(url).json()


class Friend:
    def __init__(self, firstName, lastName, email):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email


friendsList = [
    Friend('Jessica', 'Koka', 'jessicakoka@vt.edu'),
    Friend('Avicenne', 'Nasr', 'avicenne@vt.edu'),
    Friend('Shourov', 'Desai', 'shourovd@vt.edu'),
    Friend('Domenic', 'Martin', 'dmartin80@vt.edu'),
    Friend('Lily', 'Hartrich', 'lilyhartrich@vt.edu'),
    Friend('Ernesto', 'Garza', 'ernestog@vt.edu'),
    Friend('Benjamin', 'Boles', 'benboles@vt.edu'),
    Friend('Jessica', 'Seymour', 'Jessmseymour@vt.edu'),
    Friend('Emma', 'Duda', 'emmaduda@vt.edu'),
    Friend('Nina', 'Ruback', 'nina21@vt.edu'),
    Friend('Edward', 'Seltzner', 'Edward21@vt.edu'),
    Friend('Nick', 'Flammer', 'nickf55@vt.edu'),
    Friend('Damin', 'Mohsin', 'daminmohsin@vt.edu'),
    Friend('Gus', 'Von', 'gusvr@vt.edu')
]


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.command(brief='Returns all events')
async def events(ctx):
    for event in requests.get(url).json():
        if event['event']['committee']['committeeName'] != 'Studio Training':
            await ctx.send(
                '```' + 'Event: ' + event['event']['eventName']
                + '\nDate: ' + str(parser.parse(event['date']).strftime('%x'))
                + '\nType: ' + event['event']['committee']['committeeName']
                + '\nCap: ' + str(event['event']['attendanceCap']) + '\nSigned Up: ' + str(event['_signedUpCount'])
                + '\nAvailable: ' + str(event['_signedUpCount'] < event['event']['attendanceCap'])
                + '\nFriends Attending: ' + check_friends(event['signedUp'])
                + '```')


@client.command(brief='Returns all available events')
async def openevents(ctx):
    for event in requests.get(url).json():
        if event['_signedUpCount'] < event['event']['attendanceCap'] and \
                event['event']['committee']['committeeName'] != 'Studio Training':
            await ctx.send(
                '```' + 'Event: ' + event['event']['eventName']
                + '\nDate: ' + event['date']
                + '\nType: ' + event['event']['committee']['committeeName']
                + '\nCap: ' + str(event['event']['attendanceCap']) + '\nSigned Up: ' + str(event['_signedUpCount'])
                + '\nAvailable: ' + str(event['_signedUpCount'] < event['event']['attendanceCap'])
                + '\nFriends Attending: ' + check_friends(event['signedUp'])
                + '```')


@client.command(brief='Returns events by type', pass_context=True)
async def event(ctx, committee=''):
    for event in requests.get(url).json():
        if event['_signedUpCount'] < event['event']['attendanceCap'] and \
                event['event']['committee']['committeeName'] == committee:
            await ctx.send(
                '```' + 'Event: ' + event['event']['eventName']
                + '\nDate: ' + event['date']
                + '\nType: ' + event['event']['committee']['committeeName']
                + '\nCap: ' + str(event['event']['attendanceCap']) + '\nSigned Up: ' + str(event['_signedUpCount'])
                + '\nAvailable: ' + str(event['_signedUpCount'] < event['event']['attendanceCap']) + '```')


@client.command(brief='Returns available studio trainings', pass_context=True)
async def trainings(ctx):
    for event in requests.get(url).json():
        if event['_signedUpCount'] < event['event']['attendanceCap'] and \
                event['event']['committee']['committeeName'] == 'Studio Training':
            await ctx.send(
                '```' + 'Event: ' + event['event']['eventName']
                + '\nDate: ' + event['date']
                + '\nType: ' + event['event']['committee']['committeeName']
                + '\nCap: ' + str(event['event']['attendanceCap']) + '\nSigned Up: ' + str(event['_signedUpCount'])
                + '\nAvailable: ' + str(event['_signedUpCount'] < event['event']['attendanceCap']) + '```')


@client.command(brief='Returns all studio trainings', pass_context=True)
async def alltrainings(ctx):
    for event in requests.get(url).json():
        if event['event']['committee']['committeeName'] == 'Studio Training':
            await ctx.send(
                '```' + 'Event: ' + event['event']['eventName']
                + '\nDate: ' + event['date']
                + '\nType: ' + event['event']['committee']['committeeName']
                + '\nCap: ' + str(event['event']['attendanceCap']) + '\nSigned Up: ' + str(event['_signedUpCount'])
                + '\nAvailable: ' + str(event['_signedUpCount'] < event['event']['attendanceCap']) + '```')


@client.command(brief='Returns events by type', pass_context=True)
async def person(ctx, email=''):
    for event in requests.get(url).json():
        for attendee in event['signedUp']:
            if attendee['email'] == email:
                await ctx.send(
                    '```' + 'Event: ' + event['event']['eventName']
                    + '\nDate: ' + event['date']
                    + '\nType: ' + event['event']['committee']['committeeName']
                    + '\nCap: ' + str(event['event']['attendanceCap']) + '\nSigned Up: ' + str(event['_signedUpCount'])
                    + '\nAvailable: ' + str(event['_signedUpCount'] < event['event']['attendanceCap']) + '```')


@client.command(brief='Returns api URL', pass_context=True)
async def link(ctx):
    await ctx.send(
        '```' + 'URL: ' + url + '```')


@client.command(brief='Clears the last 10 messages', pass_context=True)
async def clear(ctx, amount=10):
    channel = ctx.message.channel
    messages = await channel.history(limit=int(amount)).flatten()
    await channel.delete_messages(messages)


def check_friends(attending):
    friends_attending = []
    for attendee in attending:
        for friend in friendsList:
            if attendee['email'] == friend.email:
                friends_attending.append(friend.firstName + ' ' + friend.lastName)
    return ', '.join(friends_attending)


client.run(TOKEN)
