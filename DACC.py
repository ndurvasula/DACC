from collections import OrderedDict

class Agent():

    def __init__(self, i, B, L):
        self.A = []
        self.B = {}
        self.L = L
        for b in B:
            self.B[b] = L[b]
        self.B = OrderedDict(sorted(self.B.items(), key=lambda x: x[1]))
        self.i = i
        self.match = i

    def prefers(self,a,b):
        #Prefer a over b
        return self.L[a] < self.L[b]

    def top(self):
        ids = [i for i in self.B.keys()]
        if len(ids) > 0:
            return ids[0]
        return None

    def update(self):
        self.B = OrderedDict(sorted(self.B.items(), key=lambda x: x[1]))

    def apply(self,J):
        global agents
        global CC
        
        if self.match == J.i or J.i == self.i:
            return
        J.A.append(self.i)
        J.B[self.i] = J.L[self.i]
        J.update()

        if J.prefers(self.i, J.match):

            if self.match != self.i:
                if self.i in agents[self.match].A:
                    CC.append(self.match)
                del agents[self.match].B[self.i]
                agents[self.match].match = agents[self.match].i

            if J.match != J.i:
                if J.i in agents[J.match].A:
                    CC.append(J.match)
                del agents[J.match].B[J.i]
                agents[J.match].match = agents[J.match].i

            self.match = J.i
            J.match = self.i

        else:
            del self.B[J.i]
        

def main(phi):
    global CC
    global agents
    global k, t
    
    CC = []
    k = 1
    t = 1

    terminate = False

    while not terminate:
        
        terminate = True
        for a in agents:
            if a.top() != a.match:
                terminate = False
                break
        if terminate:
            break

        if len(CC) == 0:
            i = agents[phi(k)]
            i.apply(agents[i.top()])
            k += 1

        else:
            i = agents[CC[-1]]
            i.apply(agents[i.top()])
            if i.match != i.i or len(i.B) == 0:
                CC.pop()

        t += 1

def phi(k):
    global agents
    return k % len(agents)

M = [0,2,4]
W = [1,3,5]
m1 = Agent(0, [int(i) for i in (str(W)[1:-1]+","+str(0)).split(",")], [100,1,100,2,100,3])
m2 = Agent(2, [int(i) for i in (str(W)[1:-1]+","+str(2)).split(",")], [100,3,100,1,100,2])
m3 = Agent(4, [int(i) for i in (str(W)[1:-1]+","+str(4)).split(",")], [100,2,100,3,100,1])
w1 = Agent(1, [int(i) for i in (str(M)[1:-1]+","+str(1)).split(",")], [3,100,1,100,2,100])
w2 = Agent(3, [int(i) for i in (str(M)[1:-1]+","+str(3)).split(",")], [2,100,3,100,1,100])
w3 = Agent(5, [int(i) for i in (str(M)[1:-1]+","+str(5)).split(",")], [1,100,2,100,3,100])
agents = [m1,w1,m2,w2,m3,w3]

main(phi)
print([i.match for i in agents])
        

        
    
        
