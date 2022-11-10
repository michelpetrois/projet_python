def func1():
    global a
    print ("func1","a ",a," c ",c)
    a = 20
    b = 20
    d = 20
    print ("func1","a ",a,"b ",b,"c ",c)
    func2()

def func2():
    global c
    print ,("func2","b ",b,"c ",c)
    a = 30
    print ("func2","a ",a," b",b,"c ",c)

a=0
b=0
c=0

print ("main","a ",a,"b ",b,"c ",c)
a = 10
b = 10
c = 10
func1()
print ("main","a ",a,"b ",b,"c ",c)
