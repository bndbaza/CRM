import asyncio
import aioari
from aioari import Client
from aioari.model import Channel
from contextlib import suppress
from typing import Dict
from models import *
import json
import threading
from datetime import datetime
from db import connection

number_redirect = {}
timer = {}
all_events = {}

async def on_dtmf(channel, event, outgoing, client, bridge, bc): # Обработка нажатия кнопок
    global timer
    digit = event['digit']
    id = event['channel']['id']
    try:
        timer[id].cancel()
    except:
        pass
    try:
        timer[id] = asyncio.create_task(dtmf_redirect(channel,bridge, outgoing, client, bc))
    except:
        pass
    if digit == '#':
        await channel.play(media='sound:call-forward')
        await outgoing.hold()
        number_redirect[id] = ''
    else:
        if id in number_redirect.keys():
            number_redirect[id] += digit

async def dtmf_redirect(channel_old,bridge,channel, client, bc): # Таймер срабатывания переадресации
    await asyncio.sleep(2)
    if channel.json['caller']['number'] == '':
        await channel.setChannelVar(variable='CALLERID(num)',value=await correct_number(channel_old.json['dialplan']['exten']))
        await asyncio.sleep(0.2)
    outgoing = await client.channels.originate(endpoint=f"SIP/{number_redirect[channel_old.id]}",app='bss',originator=channel.id)
    await event_create(outgoing)
    name = bridge.json.get('id')
    bc['date_out'] = datetime.today()
    CallList.create(inbound=bc['inbound'],date_in=bc['date_in'],outgoing=bc['outgoing'],date_out=bc['date_out'],record=name)
    await bridge.destroy()
    await channel_hangup(channel_old)
    await event_close(channel)
    del number_redirect[channel_old.id]
    await channel.ring()
    all_events[outgoing.id].append(outgoing.on_event('ChannelDestroyed', channel_destroy_in_in, channel))
    all_events[channel.id].append(channel.on_event('StasisEnd', channel_destroy_in_in, outgoing))
    all_events[outgoing.id].append(outgoing.on_event('StasisStart', bridge_start_out_in, channel, client))
    connection.close()


async def on_start(objs, event, client): # Определение входного канала
    channel = objs['channel']
    await event_create(channel)
    args = event['args']
    if len(args) == 0:
        return
    elif args[0] == 'in_in':
        print('in_in')
        await call_in_in(channel, event, client)
    elif args[0] == 'in_out':
        print('in_out')
        await call_in_out(channel, event, client)
    elif args[0] == 'out_in':
        print('out_in')
        await call_out_in(channel, event, client)
    elif args[0] == 'web_out':
        print('web_out')
        await call_web_out(channel, event, client)
    else:
        return

async def call_in_in(channel, event, client): # Обработка Внутреннего звонка
    outgoing = await client.channels.originate(endpoint=f"SIP/{await correct_number(channel.json['dialplan']['exten'])}",app='bss',originator=channel.id)
    await event_create(outgoing)
    await channel.ring()
    all_events[outgoing.id].append(outgoing.on_event('ChannelDestroyed', channel_destroy_in_in, channel))
    all_events[channel.id].append(channel.on_event('StasisEnd', channel_destroy_in_in, outgoing))
    all_events[outgoing.id].append(outgoing.on_event('StasisStart', bridge_start_in_in, channel, client))

async def bridge_start_in_in(outgoing, event, channel, client): # Создание моста in_in
    outgoing = outgoing['channel']
    await outgoing.answer()
    await channel.answer()
    await event_close(outgoing)
    await event_close(channel)
    bridge = await client.bridges.create(type='mixing,dtmf_events')
    await bridge.addChannel(channel=[channel.id,outgoing.id])
    all_events[outgoing.id].append(outgoing.on_event('StasisEnd', bridge_destroy_in_in, bridge, channel))
    all_events[channel.id].append(channel.on_event('StasisEnd', bridge_destroy_in_in, bridge, outgoing))
    # all_events[channel.id].append(channel.on_event('ChannelDtmfReceived',on_dtmf, outgoing, client, bridge))
    # all_events[outgoing.id].append(outgoing.on_event('ChannelDtmfReceived',on_dtmf, channel, client, bridge))

async def bridge_destroy_in_in(channel, event, bridge, outgoing): # Уничтожение Внутреннего моста
    try:    
        await bridge.destroy()
        await channel_hangup(outgoing)
    except:
        print('error Bridge')

async def call_in_out(channel, event, client): # Обработка Исходящего звонка
    outgoing = await client.channels.originate(endpoint=f"SIP/Director/{await correct_number(channel.json['dialplan']['exten'])}",app='bss',originator=channel.id)
    await event_create(outgoing)
    await channel.ring()
    all_events[outgoing.id].append(outgoing.on_event('ChannelDestroyed', channel_destroy_in_in, channel))
    all_events[channel.id].append(channel.on_event('StasisEnd', channel_destroy_in_in, outgoing))
    all_events[outgoing.id].append(outgoing.on_event('StasisEnd', channel_destroy_in_in, channel))
    all_events[outgoing.id].append(outgoing.on_event('StasisStart', bridge_start_in_out, channel, client))

async def bridge_start_in_out(outgoing, event, channel, client): # Создание Исходящего моста
    outgoing = outgoing['channel']
    await outgoing.answer()
    await channel.answer()
    await event_close(outgoing)
    await event_close(channel)
    bridge = await client.bridges.create(type='mixing,dtmf_events')
    await bridge.addChannel(channel=[channel.id,outgoing.id])
    name = bridge.json.get('id')
    recording = await bridge.record(name=name,format='wav')
    out = await correct_number(channel.json.get('dialplan').get('exten'))
    bridge_call = {'inbound':event['channel']['connected']['number'],
                   'date_in':datetime.today(),
                   'outgoing':out}
    all_events[outgoing.id].append(outgoing.on_event('StasisEnd', bridge_destroy_out_out, bridge, channel, bridge_call))
    all_events[channel.id].append(channel.on_event('StasisEnd', bridge_destroy_out_out, bridge, outgoing, bridge_call))
    all_events[channel.id].append(channel.on_event('ChannelDtmfReceived',on_dtmf, outgoing, client, bridge, bridge_call))
    # all_events[outgoing.id].append(outgoing.on_event('ChannelDtmfReceived',on_dtmf, channel, client, bridge))

async def call_out_in(channel, event, client): # Обработка Входящего звонка
    outgoing = await client.channels.originate(endpoint=f"SIP/{await correct_number(channel.json['dialplan']['exten'])}",app='bss',originator=channel.id)
    await event_create(outgoing)
    await channel.ring()
    all_events[outgoing.id].append(outgoing.on_event('ChannelDestroyed', channel_destroy_in_in, channel))
    all_events[channel.id].append(channel.on_event('StasisEnd', channel_destroy_in_in, outgoing))
    all_events[outgoing.id].append(outgoing.on_event('StasisEnd', channel_destroy_in_in, channel))
    all_events[outgoing.id].append(outgoing.on_event('StasisStart', bridge_start_out_in, channel, client))

async def bridge_start_out_in(outgoing, event, channel, client): # Создание Входящего моста
    outgoing = outgoing['channel']
    await outgoing.answer()
    await channel.answer()
    await event_close(outgoing)
    await event_close(channel)
    bridge = await client.bridges.create(type='mixing,dtmf_events')
    await bridge.addChannel(channel=[channel.id,outgoing.id])
    name = bridge.json.get('id')
    recording = await bridge.record(name=name,format='wav')
    out = event['channel']['caller']['number']
    bridge_call = {'inbound':event['channel']['connected']['number'],
                   'date_in':datetime.today(),
                   'outgoing':out}
    all_events[outgoing.id].append(outgoing.on_event('StasisEnd', bridge_destroy_out_out, bridge, channel, bridge_call))
    all_events[channel.id].append(channel.on_event('StasisEnd', bridge_destroy_out_out, bridge, outgoing, bridge_call))
    # all_events[channel.id].append(channel.on_event('ChannelDtmfReceived',on_dtmf, outgoing, client, bridge))
    all_events[outgoing.id].append(outgoing.on_event('ChannelDtmfReceived',on_dtmf, channel, client, bridge, bridge_call))

async def bridge_destroy_in_in(channel, event, bridge, outgoing): # Уничтожение Внутреннего моста
    try:    
        await bridge.destroy()
        await channel_hangup(outgoing)
    except:
        print('error Bridge')

async def bridge_destroy_out_out(channel, event, bridge, outgoing, bc): # Уничтожение Внeшнего моста
    try:    
        name = bridge.json.get('id')
        bc['date_out'] = datetime.today()
        CallList.create(inbound=bc['inbound'],date_in=bc['date_in'],outgoing=bc['outgoing'],date_out=bc['date_out'],record=name)
        await bridge.destroy()
        await channel_hangup(outgoing)
    except:
        print('error Bridge')
    connection.close()

async def channel_destroy_in_in(channel, event, outgoing):
    try:
        await channel_hangup(outgoing)
    except:
        print('error Channal')


async def event_create(channel): # Создание переменной события
    if channel.id not in all_events:
        all_events[channel.id] = []

async def event_close(channel): # Уничтожение переменных событий
    for i in all_events[channel.id]:
        i.close()

async def channel_hangup(channel): # Закрытие канала
    await event_close(channel)
    del all_events[channel.id]
    await channel.hangup()


async def call_web_out(channel, event, client): # Обработка Web звонка
    await channel.setChannelVar(variable='CALLERID(num)',value= await correct_number(event['args'][2]))
    await asyncio.sleep(0.2)
    outgoing = await client.channels.originate(endpoint=f"SIP/{event['args'][1]}",app='bss',originator=channel.id)
    await event_create(outgoing)
    all_events[outgoing.id].append(outgoing.on_event('StasisStart', call_web, client))

async def call_web(channel, event, client): # Обработка Web звонка
    channel = channel['channel']
    outgoing = await client.channels.originate(endpoint=f"SIP/Director/{event['channel']['connected']['number']}",app='bss',originator=channel.id)
    await event_create(outgoing)
    await channel.ring()
    all_events[outgoing.id].append(outgoing.on_event('ChannelDestroyed', channel_destroy_in_in, channel))
    all_events[channel.id].append(channel.on_event('StasisEnd', channel_destroy_in_in, outgoing))
    all_events[outgoing.id].append(outgoing.on_event('StasisEnd', channel_destroy_in_in, channel))
    all_events[outgoing.id].append(outgoing.on_event('StasisStart', bridge_start_in_out, channel, client))

async def correct_number(number): # Коректировка номера
    if len(number) == 12:
        number = '+'+number[1:]
    elif len(number) == 11:
        number = '+7'+number[1:]
    elif len(number) == 6:
        number = '+73952'+number
    elif len(number) == 5:
        number = '+739550'+number
    elif number == '1':
        number = '147'
    elif number == '2':
        number = '117'
    elif number == '3':
        number = '135'
    elif number == '4':
        number = '126'
    elif number == '5':
        number = '148'
    elif number == '6':
        number = '144'
    elif number == '7':
        number = '177'
    elif number == 't':
        number = '117'
    return number

async def on_end(objs, event, client):
    if objs.id in all_events:
        del all_events[objs.id] 

async def main_asterisk():  # Точка входа
    client = await aioari.connect('http://192.168.0.69:8088/', 'viktor', '35739517')
    client.on_channel_event('StasisStart', on_start, client)
    client.on_channel_event('StasisEnd', on_end, client)
    try:
        await client.run(apps="bss")
    finally:
        await client.close()


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main_asterisk())
