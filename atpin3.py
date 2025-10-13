# attempt 3
import random
a=random.randint(1,5)
atp=[]
for atp in range(1,4):
    b=int(input("enter the number:"))
    if b==a:
        print("value matched")
        break
    elif a>b:
        print("value greater")
    elif a<b:
        print("value lesser")
else:
    print("you lost")
    