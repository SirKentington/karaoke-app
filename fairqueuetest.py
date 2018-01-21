
import fairqueue
import random

def rstring():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])

# Test that removing a string

fq = fairqueue.FairQueue()

fq.add('kent', 'song1')
fq.add('kent', 'song2')
fq.add('kent', 'song3')

for item in fq:
    print item
    
print fq
print fq['kent']

fq = fairqueue.FairQueue()
fq.add('kent', 'song1')
fq.add('kent', 'song2')
fq.add('kent', 'song3')
fq.add('lisa', 'song4')
fq.add('lisa', 'song5')
fq.add('lisa', 'song6')
fq.add('nels', 'song7')
fq.add('nels', 'song8')
fq.add('nels', 'song9')
print fq.keys()
nl = [('baby', 'song10'), ('baby', 'song11'), ('baby', 'song12')]

print fq
print fq['nels']
print fq
print fq.keypop('nels')
print fq
