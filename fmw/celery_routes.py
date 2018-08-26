class CeleryRouter(object):

    def route_for_task(self, task, args=None, kwargs=None):
        if task == 'portal.task.getSMSRegBalance':
            return {'exchange': 'video',
                    'exchange_type': 'topic',
                    'routing_key': 'getbalance'}
        return None