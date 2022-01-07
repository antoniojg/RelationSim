import discord
import os
from dotenv import load_dotenv
import sqlite3
from sqlite3 import Error

load_dotenv()

MY_ENV_VAR = os.getenv('MY_ENV_VAR')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user})".format(client))

def relationship_status_calculator(points):
    status = ''
    if -100 <= points <= -50:
        status = 'enemies'
    elif -51 <= points <= -31:
        status = 'cold'
    elif -31 <= points <= 31:
        status = 'acquaintances'
    elif 31 <= points <= 51:
        status = 'warm'
    elif 51 <= points <= 81:
        status = 'friends'
    elif 81 <= points <= 101:
        status = 'crushes'
    elif 101 <= points <= 111:
        status = 'lovers'

    return status

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('Connected to db | version {}'.format(sqlite3.version))
    except Error as e:
        print(e)

    return conn

def insert_new_user(conn, user):

    sql = ''' INSERT INTO users(id, name)
              VALUES(?, ?) '''

    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def create_relationship(conn, user1, user2):
    try:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM relationships WHERE (user_id_1=? AND user_id_2=?)''', (user1, user2))
        entry = cur.fetchone()

        if entry is None:
            cur.execute('''INSERT INTO relationships (user_id_1, user_id_2, points)
                            VALUES(?, ?, ?)''', (user1, user2, 0))
        else:
            print ('Entry found')
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(e)

conn = create_connection('relationsim.db')

def positive_relationship(conn, user1, user2):
    status = ''
    try:
        cur = conn.cursor()
        point_data = cur.execute('''SELECT points
                       FROM relationships
                       WHERE user_id_1 = ? AND user_id_2 = ?''', (user1, user2)).fetchone()
        points = point_data[0]
        if points == 110:
            status = ', Cannot be more than lovers'
        else:
            cur.execute('''UPDATE relationships
                        SET points = points + 10
                        WHERE user_id_1 = ? AND user_id_2 = ?''', (user1, user2))
            conn.commit()
            status = ''
        return status
    except Error as e:
        print(e)

def negative_relationship(conn, user1, user2):
    status = ''
    try:
        cur = conn.cursor()
        point_data = cur.execute('''SELECT points
                       FROM relationships
                       WHERE user_id_1 = ? AND user_id_2 = ?''', (user1, user2)).fetchone()
        points = point_data[0]
        if points == -100:
            status = ', Cannot be more than enemies'
        else:
            cur.execute('''UPDATE relationships
                        SET points = points - 10
                        WHERE user_id_1 = ? AND user_id_2 = ?''', (user1, user2))
            conn.commit()
            status = ''
        return status
    except Error as e:
        print(e)

def relationship_status(conn, user1, user2):
    try:
        cur = conn.cursor()
        point_data = cur.execute('''SELECT points
                       FROM relationships
                       WHERE user_id_1 = ? AND user_id_2 = ?''', (user1, user2)).fetchone()
        
        points = point_data[0]
        return relationship_status_calculator(points)
    except Error as e:
        print(e)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$join'):
        try:
            user = (message.author.id, message.author.name)
            user_id = insert_new_user(conn, user)
            await message.channel.send('>>> Welcome to **RelationSim**,\n\nYou will be able to meet and have a relationship\nindicator in your server similar to relationships\nin the sims!\n__Commands are as follow:__\n**$meet** *@user* - `Allows you to start a friendship with another user`\n**$up** *@user* - `Adds relationship points`\n**$down** *@user* - `Subtracts relationship points`\n**$relationship** *@user* - `Allows you to check your status with another user`')
        except:
            await message.channel.send('Looks like you already joined!')

    if message.content.startswith('$meet'):
        try:
            if message.mentions[0].id:
                mentionedUserID = message.mentions[0].id
                create_relationship(conn, message.author.id,  mentionedUserID)
                await message.channel.send('@{} and {} have **met!**'.format(message.author, message.mentions[0].mention))
        except:
            await message.channel.send('> @{}, Please mention a user'.format(message.author))

    if message.content.startswith('$up'):
        try:
            if message.mentions[0].id:
                mentionedUserID = message.mentions[0].id
                status = positive_relationship(conn, message.author.id, mentionedUserID)
                await message.channel.send('> @{} and {}: **positive relationship{}**'.format(message.author, message.mentions[0].mention, status))
        except:
            await message.channel.send('> @{}, Please mention a user'.format(message.author))

    if message.content.startswith('$down'):
        try:
            if message.mentions[0].id:
                mentionedUserID = message.mentions[0].id
                status = negative_relationship(conn, message.author.id, mentionedUserID)
                await message.channel.send('> @{} and {}: **negative relationship{}**'.format(message.author, message.mentions[0].mention, status))
        except:
            await message.channel.send('> @{}, Please mention a user'.format(message.author))

    if message.content.startswith('$relationship'):
        try:
            if message.mentions[0].id:
                mentionedUserID = message.mentions[0].id
                status = relationship_status(conn, message.author.id, mentionedUserID)
                await message.channel.send('> @{} and {} are **{}**'.format(message.author, message.mentions[0].mention, status))
        except:
            await message.channel.send('> @{}, Please mention a user'.format(message.author))

client.run(os.getenv('TOKEN'))
