
from collections import defaultdict, namedtuple
import copy

Entry = namedtuple('Entry', 'singer song')

class RRQueue(object):
    def __init__(self):
        self.queues = defaultdict(list)

    def add(self, singer, song):
        self.queues[singer].append(song)

    def queue(self):
        queue = []
        queues = copy.deepcopy(self.queues)
        total = len(self)

        while len(queue) < total:
            for singer in queues.keys():
                if len(queues[singer]) == 0:
                    del queues[singer]
                    continue
                song = queues[singer].pop(0)
                queue.append(Entry(singer, song))
        return queue

    def pop(self):
        for singer in queues.keys():
            if len(queues[singer]) == 0:
                del queues[singer]
                continue
            song = queues[singer].pop(0)
            queue.append(Entry(singer, song))

    def __len__(self):
        total = 0
        for queue in self.queues.values():
            total += len(queue)
        return total

def do_test():
    rrq = RRQueue()
    rrq.add('Kent', 'Song KA')
    rrq.add('Kent', 'Song KB')
    rrq.add('Kent', 'Song KC')
    rrq.add('Lisa', 'Song LA')
    rrq.add('Lisa', 'Song LB')
    rrq.add('Lisa', 'Song LC')
    rrq.add('Nels', 'Song NA')
    rrq.add('Nels', 'Song NB')
    rrq.add('Nels', 'Song NC')
    print rrq.queue()

if __name__ == '__main__':
    do_test()
