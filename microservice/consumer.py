import json
import asyncio
from aio_pika import connect, IncomingMessage

from db import async_session_maker
from crud import product_crud

import tracemalloc
tracemalloc.start()


async def main():
    connection = await connect("amqps://lvtbhjno:KO5sOzrpJntPFAUtJlAag49ksPGo20KX@moose.rmq.cloudamqp.com/lvtbhjno")
    channel = await connection.channel()
    queue = await channel.declare_queue('main')

    async def callback(message: IncomingMessage):
        print('Received in main')
        data = json.loads(message.body)
        print(data)

        session = async_session_maker()

        if message.content_type == 'product_created':
            await product_crud.create(session=session, create_obj=data)
        elif message.content_type == 'product_updated':
            await product_crud.update(session=session, id=data.get('id'), obj_new=data)
        elif message.content_type == 'product_deleted':
            await product_crud.delete(session=session, id=data.get('id'))
        await session.close()

    await queue.consume(callback, no_ack=True)

    print('Started consuming')

    await asyncio.Future()

asyncio.run(main())

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')