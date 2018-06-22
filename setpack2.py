import random

class Agent():

    def __init__(self, i):     
        self.A = set()
        self.B = set()
        self.i = i
        self.parent = None
        self.sibling = None
        self.children = set()
        
    def prefers(self,A,B):
        global nu
        
        #Prefer a over b
        if A == None:
            return B
        if B == None:
            return A
        if A in nu and B not in nu:
            return B
        if B in nu and A not in nu:
            return A
        if self.parent != None:
            if A in self.parent.B and B not in self.parent.B:
                return B
            if B in self.parent.B and A not in self.parent.B:
                return A
        
        return len(A.B) < len(B.B)

    def top(self):
        global nu, sigma
        
        if len(self.B) == 0 or (self.parent != None and len(self.B.intersection(self.parent.B)) == len(self.B)):
            return None
        
        B = list(self.B)
        B.sort(key = lambda x: len(x.B))
        for i in range(len(B)):
            if self.parent!= None and B[0] in self.parent.B:
                del B[0]
                continue
            if B[0].parent != None and B[0].parent in self.B:
                del B[0]
                continue
            if B[0] in nu:
                B.append(B[0])
                del B[0]
            else:
                break
        return B[0]

    def update(self):
        global S, nu, sigma
        self.B = set()
        for k in sigma:
            if k == self or self in k.children:
                continue
            s = set([obj for obj in k.i])
            s = s.union(self.i)
            for i in S:
                if s.issubset(i) and self not in k.A and k not in self.A:
                    self.B.add(k)
                    break
                    
    def root(self):
        ret = self
        while ret.parent != None:
            ret = ret.parent
        return ret

    def apply(self,J):
        global sigma, nu
        global S, CC
        
        if J in self.root().children:
            print(J.i,"is already matched to",self.i)
            return
        
        J.A.add(self)
        J.B.add(self)
        
        #for k in J.children:
        #    k.B.add(self)
        #for k in self.children:
        #    k.B.add(J)
            
        print(J.i,"now has A =",[i.i for i in J.A])
        print(J.i,"now has B =",[i.i for i in J.B])

        if J.prefers(self, J.sibling):
            print(J.i,"prefers",self.i,"over its partner","(none)" if J.sibling == None else J.sibling.i)

            if self.sibling != None:
                print(self.i,"is currently matched")
                    
                self.sibling.B.remove(self)
                self.B.remove(self.sibling)
                
                #o = self.root().i
                
                for k in self.root().children:
                    if k in self.B:
                        self.B.remove(k)
                        
                self.parent.i = self.sibling.i
                self.parent.B = self.sibling.B
                self.parent.A = self.sibling.A.union(self.parent.A)
                self.parent.children = self.sibling.children
                nxt = self.parent
                while nxt.parent != None:
                    nxt2 = nxt.parent
                    nxt2.i = nxt.i.union(nxt.sibling.i)
                    nxt2.children = nxt.children.union(nxt.sibling.children).union({nxt,nxt.sibling})
                    nxt = nxt2

                if nxt in nu:
                    nu.remove(nxt)

                if nxt in S:
                    nu.add(nxt)
                else:
                    sigma.add(nxt)

                sigma.remove(self.sibling)

##                for k in sigma:
##                    if self.sibling in k.B:
##                        k.B.remove(self.sibling)
##                        k.B.add(self.parent)
##                    if k not in nxt.children and k != nxt:
##                        k.dupdate(nxt, o)
                
                if self in self.parent.A:
                    CC.append(self.parent)
                

            if J.sibling != None:
                J.sibling.B.remove(J)
                J.B.remove(J.sibling)
                
                #o = J.root().i

                for k in J.root().children:
                    if k in J.B:
                        J.B.remove(k)
                
                J.parent.i = J.sibling.i
                J.parent.B = J.sibling.B
                J.parent.A = J.sibling.A.union(J.parent.A)
                J.parent.children = J.sibling.children
                nxt = J.parent
                while nxt.parent != None:
                    nxt2 = nxt.parent
                    nxt2.i = nxt.i.union(nxt.sibling.i)
                    nxt2.children = nxt.children.union(nxt.sibling.children).union({nxt,nxt.sibling})
                    nxt = nxt2

                if nxt in nu:
                    nu.remove(nxt)

                if nxt in S:
                    nu.add(nxt)

                sigma.remove(J.sibling)

##                for k in sigma:
##                    if J.sibling in k.B:
##                        k.B.remove(J.sibling)
##                        k.B.add(J.parent)
##                    if k not in nxt.children and k != nxt:
##                        k.dupdate(nxt, o)
                
                if J in J.parent.A:
                    CC.append(J.parent)

            if J == self:
                self.sibling = self
                nu.add(self)
                sigma.remove(self)
                return

            self.sibling = J
            J.sibling = self

            if J in nu:
                nu.remove(J)
            
            multiset = Agent(self.i.union(J.i))
            self.parent = multiset
            J.parent = multiset
            multiset.children = self.children.union(J.children).union({self,J})

            sigma.add(multiset)
            
            if multiset.i in S:
                nu.add(multiset)
                sigma.remove(multiset)
            
            for k in sigma:
                k.update()


        else:
            self.B.remove(J)
        

def main(phi):
    global CC
    global sigma
    global K, T
    
    CC = []
    K = 1
    T = 1

    terminate = False

    while not terminate:
        print("Sigma:",[i.i for i in sigma])
        print("Mu:",[i.i for i in mu])
        print("Nu:",[i.i for i in nu])
        print()
        for i in sigma:
            print(i.i,"A =",[j.i for j in i.A],"B =",[j.i for j in i.B], "children =",[j.i for j in i.children],"sibling =",None if i.sibling == None else i.sibling.i,"parent =",None if i.parent == None else i.parent.i)

        for i in nu:
            print("Nu:",i.i,"A =",[j.i for j in i.A],"B =",[j.i for j in i.B], "children =",[j.i for j in i.children],"sibling =",None if i.sibling == None else i.sibling.i,"parent =",None if i.parent == None else i.parent.i)
        
        terminate = True
        for a in sigma:
            if a.top() != a.sibling and a.top() != None:
                terminate = False
                break
                
        if terminate:
            break

        if len(CC) == 0:
            print("We have a null CC")
            i = list(sigma)[phi(K)]
            if i.top() == None:
                K += 1
                continue
            print(i.i,"proposes to",i.top().i)
            i.apply(i.top())
            K += 1

        else:
            print("We have a nonempty CC")
            i = CC[-1]
            if i.top() == None:
                K += 1
                CC.pop()
                continue
            print(i.i,"proposes to",i.top().i)
            i.apply(i.top())
            if i.sibling != None or len(i.B) == 0:
                CC.pop()

        print()

        T += 1

def phi(k):
    global sigma
    return k % len(sigma)      

sigma = set()
mu = set()
nu = set()

N_ELEMENTS = random.randint(5,5)
N_SUBSETS = random.randint(7,7)
U = list(range(N_ELEMENTS))
S = []
for i in range(N_SUBSETS):
    e = random.randint(1,N_ELEMENTS)
    s = set()
    for j in range(e):
        s.add(U[random.randint(0,N_ELEMENTS-1)])
    if s not in S:
        S.append(s)

for i in U:
    a = Agent({i})
    sigma.add(a)

remove = set()
for i in sigma:
    i.update()
    if i.i in S:
        remove.add(i)

for i in remove:
    sigma.remove(i)
    nu.add(i)

print("U",U)
print("S",S)

main(phi)
print()
for i in nu:
    print(i.i)
