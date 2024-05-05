import random
randomlist = random.sample(range(-4000, 3000), 1000)
print(randomlist)
best,sum=(0,0)
for i in randomlist:
    sum=max(i,sum+i)
    best=max(best,sum)
    print(sum,best)
print(best)