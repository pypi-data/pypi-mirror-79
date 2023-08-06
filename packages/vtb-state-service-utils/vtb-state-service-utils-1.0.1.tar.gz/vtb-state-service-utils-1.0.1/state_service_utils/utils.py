import asyncio
import logging
import os
import traceback
from functools import partial

import aiohttp
import simplejson as json
from aio_pika import connect, IncomingMessage, Exchange, Message

logger = logging.getLogger('')

STATE_SERVICE_URL = os.getenv('STATE_SERVICE_URL')

STATE_SERVICE_TOKEN = os.getenv('STATE_SERVICE_TOKEN')
STATE_SERVICE_DEPLOYING_STATE = 'deploying'


class StateServiceException(Exception):
    pass


if not STATE_SERVICE_URL and not os.getenv('DEBUG'):
    raise StateServiceException('Configuration error, STATE_SERVICE_URL required')


async def _make_request(url, data: dict):
    headers = {}
    if STATE_SERVICE_TOKEN:
        headers['Authorization'] = f'Token {STATE_SERVICE_TOKEN}'

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=data) as response:
            if response.status == 400:
                raise StateServiceException(await response.json())
            elif response.status != 201:
                raise StateServiceException(f'State service request error ({response.status}): {await response.text()}')


async def add_action_event(*, order, action, graph, type, status='', data=None):
    await _make_request(
        url=f'{STATE_SERVICE_URL}/action/',
        data={
            'order': order,
            'action': action,
            'graph': graph,
            'type': type,
            'status': status,
            'data': json.dumps(data),
        }
    )


async def add_event(*, order, action, graph, type, status='', data=None, parent=None):
    await _make_request(
        url=f'{STATE_SERVICE_URL}/event/',
        data={
            'order': order,
            'action': action,
            'graph': graph,
            'type': type,
            'status': status,
            'data': json.dumps(data),
            'parent': parent
        }
    )


def state_action_decorator(func):
    async def wrapper(*, order, action, graph, node, action_type='run', **kwargs):
        await add_action_event(
            order=order,
            action=action,
            graph=graph,
            type=STATE_SERVICE_DEPLOYING_STATE,
            status=f'{node}:{action_type}:started',
            data=kwargs
        )
        try:
            result = await func(**kwargs)
            status = f'{node}:{action_type}:completed'
        except Exception as e:
            result = {'error': str(e), 'traceback': traceback.format_exc()}
            status = f"{node}:{action_type}:error"
        await add_action_event(
            order=order,
            action=action,
            graph=graph,
            type=STATE_SERVICE_DEPLOYING_STATE,
            status=status,
            data=result
        )
        return result
    return wrapper


class EventsReceiver:
    def __init__(self, fn, mq_addr, mq_input_queue):
        self.mq_addr = mq_addr
        self.input_queue = mq_input_queue
        self.fn = state_action_decorator(fn)

    async def on_message(self, message: IncomingMessage, exchange: Exchange):
        with message.process():
            data = json.loads(message.body)
            if not isinstance(data, dict):
                raise StateServiceException('Invalid message (need struct): %s', data)
            response = await self.fn(
                order=data.pop('_order_id'),
                action=data.pop('_action_id'),
                graph=data.pop('_graph_id'),
                node=data['_name'],
                action_type=data.get('_type'),  # "run" default
                **data
            )
            await exchange.publish(
                Message(body=json.dumps(response).encode(), content_type="application/json",
                        correlation_id=message.correlation_id),
                routing_key=message.reply_to,
            )

    async def _receive(self, loop, addr, queue):
        connection = await connect(addr, loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue(queue)
        await queue.consume(partial(self.on_message, exchange=channel.default_exchange))

    def run(self):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self._receive(loop, addr=self.mq_addr, queue=self.input_queue))
        loop.run_until_complete(task)
        logger.info('Awaiting events')
        loop.run_forever()
