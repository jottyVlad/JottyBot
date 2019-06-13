import discord
import random
import MySQLdb
from discord.utils import get

conn = MySQLdb.connect('localhost', 'root', 'KaliLinuxHome', 'pythonbot')
cursor = conn.cursor()


TOKEN = 'NTU3NjE1NDcyNDI2NjE0Nzg2.XPYgJA.--FnAbRSY__p2u8UslAxg2lQ9Zk'

client = discord.Client()

filthy = ["хуй", "хуйня", "хер", "херня", "пизда", "пиздец", "пздц", "бля", "блять", "ебать", "еба", "трахать", "ебу", "ебал", "трахал", "трахаю"]

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if (message.content.lower() in filthy) and (message.author.server_permissions.administrator == False):
        await client.send_message(message.channel, f"{message.author.mention}, материться плохо! Если Вы выполнили команду, дописав еще и мат, то повторите команду, ибо общаться с ботом надо с уважением! =)")
        print(f"Пользователь {message.author.name} нарушил правила использования мата на сервере.")
        return
    elif (message.content.lower() in filthy) and (message.author.server_permissions.administrator == True):
        print(f"Администратор {message.author.name} нарушил правила использования мата на сервере.")

    if message.content.startswith('!reg'):
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE discord_id = {0.author.id}'.format(message))
        row = cursor.fetchone()
        if row == None:
            cursor.execute('INSERT INTO users(id, discord_id, money, warn) VALUES(null, {0.author.id} , 100, 0)'.format(message))
            conn.commit()
            msg = f"{message.author.mention}, Вы успешно зарегистрировались!"
            await client.send_message(message.channel, msg)
        else:
            msg = f"{message.author.mention}, Вы и так уже зарегистрированы!"
            await client.send_message(message.channel, msg)

    elif message.content.startswith('!hello'):
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE discord_id = {0.author.id}'.format(message))
        row = cursor.fetchone()
        if row == None:
            msg = f"{message.author.mention}, привет!"
            await client.send_message(message.channel, msg)
            msg = f"{message.author.mention}, у Вас нет аккаунта в боте, но Вы можете зарегистрироваться командой !reg"
            await client.send_message(message.channel, msg)
        else:
            msg = f"{message.author.mention}, привет!"
            await client.send_message(message.channel, msg)

    elif message.content.startswith('!kazino'):
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE discord_id = {0.author.id}'.format(message))
        row = cursor.fetchone()
        if row == None:
            msg = f"{message.author.mention}, Вы не зарегистрированы в боте, регистрация командой !reg";
            await client.send_message(message.channel, msg)
        else:
            message_array = message.content.split()
            try:
                amount = int(message_array[1])
            except:
                msg = f"{message.author.mention}, сумма может быть только числом!";
                await client.send_message(message.channel, msg)
                return
            cursor.execute('SELECT money FROM users WHERE discord_id = {0.author.id}'.format(message))
            row = cursor.fetchone()
            his_money = row[0]
            if amount <= his_money:
                number = random.randint(0, 5)
                if number < 3:
                    the_sum = his_money + amount
                    cursor.execute('UPDATE users SET money={0} WHERE discord_id = {1.author.id}'.format(the_sum, message))
                    conn.commit()
                    msg = f"{message.author.mention}, Вы победили и получили сумму ставки!";
                    await client.send_message(message.channel, msg)
                else:
                    the_sum = his_money - amount
                    cursor.execute('UPDATE users SET money={0} WHERE discord_id = {1.author.id}'.format(the_sum, message))
                    conn.commit()
                    msg = f"{message.author.mention}, Вы проиграли сумму ставки";
                    await client.send_message(message.channel, msg)
            elif amount > his_money:
                msg = f"{message.author.mention}, Вы поставили в казино больше, чем у Вас есть!";
                await client.send_message(message.channel, msg)

    elif message.content.startswith('!setrole'):
        if message.author.server_permissions.manage_roles:
            for i in message.mentions:
                all_command = message.content.split()
                role = get(i.server.roles, name=all_command[2])
                if role:
                    await client.add_roles(i, role)
                    await client.send_message(message.channel, f"{message.author.mention}, роль была успешно выдана!")
                    return
                else:
                    await client.send_message(message.channel, f"{message.author.mention}, такой роли не существует!")
                    return
            await client.send_message(message.channel, f"{message.author.mention}, надо упомянуть человека, которомы Вы хотите выдать роль!")
            return
        else:
            await client.send_message(message.channel, f"{message.author.mention}, у Вас нет прав на выполнение этой команды!")

    elif message.content.startswith('!ban'):
    	if message.author.server_permissions.ban_members:
    		for i in message.mentions:
    			if i != message.author and i != client.user:
    				await client.ban(i)
    				await client.send_message(message.channel, f"{message.author.mention}, пользователь забанен!")
    			elif i == message.author:
    				await client.send_message(message.channel, f"{message.author.mention}, Вы не можете забанить самого себя!")
    			elif i == client.user:
    				await client.send_message(message.channel, f"{message.author.mention}, Вы не можете забанить бота!")
    	else:
    		await client.send_message(message.channel, f"{message.author.mention}, у Вас нет полномочий банить пользователей!")

    elif message.content.startswith('!kick'):
    	if message.author.server_permissions.kick_members:
    		for i in message.mentions:
    			if i != message.author and i != client.user:
    				await client.kick(i)
    				await client.send_message(message.channel, f"{message.author.mention}, пользователь кикнут!")
    			elif i == message.author:
    				await client.send_message(message.channel, f"{message.author.mention}, Вы не можете кикнуть самого себя!")
    			elif i == client.user:
    				await client.send_message(message.channel, f"{message.author.mention}, Вы не можете кикнуть бота!")
    	else:
    		await client.send_message(message.channel, f"{message.author.mention}, у Вас нет полномочий кикать пользователей!")

    elif message.content.startswith('!warn'):
        if message.author.server_permissions.administrator:
            for i in message.mentions:
                if i != message.author and i != client.user:
                    conn.commit()
                    cursor.execute('SELECT * FROM users WHERE discord_id = {0.author.id}'.format(message))
                    row = cursor.fetchone()
                    if row == None:
                        cursor.execute('INSERT INTO users(id, discord_id, money, warn) VALUES(null, {0.author.id} , 100, 1)'.format(message))
                        conn.commit()
                        await client.send_message(message.channel, f"{message.author.mention}, пользователь зарегистрирован и ему выдано предупреждение!")
                    else:
                        cursor.execute('SELECT warn FROM users WHERE discord_id = {0.author.id}'.format(message))
                        warns_tuple = cursor.fetchone()
                        warns = warns_tuple[0]
                        warns += 1
                        if warns < 3:
                            cursor.execute('UPDATE users SET warn={0} WHERE discord_id = {1.author.id}'.format(warns, message))
                            conn.commit()
                            await client.send_message(message.channel, f"{message.author.mention}, пользователю выдано предупреждение!")
                        elif warns == 3:
                            await client.ban(i)
                            await client.send_message(message.channel, f"{message.author.mention}, пользователь забанен за достижение им 3-х предупреждений!")

    elif message.content.startswith('!unwarn'):
        if message.author.server_permissions.administrator:
            for i in message.mentions:
                if i != message.author and i != client.user:
                    conn.commit()
                    cursor.execute('SELECT * FROM users WHERE discord_id = {0.author.id}'.format(message))
                    row = cursor.fetchone()
                    if row == None:
                        await client.send_message(message.channel, f"{message.author.mention}, пользователь не зарегистрирован и у него нет предупреждений!")
                    else:
                        cursor.execute('SELECT warn FROM users WHERE discord_id = {0.author.id}'.format(message))
                        warns_tuple = cursor.fetchone()
                        warns = warns_tuple[0]
                        if warns == 0:
                            await client.send_message(message.channel, f"{message.author.mention}, у пользователя и так отсутствуют предупреждения!")
                        else:
                            warns -= 1;
                            cursor.execute('UPDATE users SET warn={0} WHERE discord_id={1.author.id}'.format(warns, message))
                            conn.commit()
                            await client.send_message(message.channel, f"{message.author.mention}, вы сняли предупреждение у пользователя!")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
