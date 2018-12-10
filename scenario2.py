ans = 0
count=0
mylist=[1,2,3,4,5,6,7]
for k in range(10)[::-1]:
    print(k)
    count=count+1
    if k >= 7:
        ans=ans+k
        break
print(count,ans)

