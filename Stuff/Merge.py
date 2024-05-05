import random
array = random.sample(range(-2000, 3000), 1000)
print(array)
def sort(arr):
    if(len(arr)==1):
        return arr
    else:
        k=len(arr)//2
        l1=sort(arr[0:k])
        l2=sort(arr[k:])
        return merge(l1,l2)
def merge(arr1,arr2):
    merlst=[]
    for i in range(len(arr1)+len(arr2)):
        if(len(arr1)==0):
            merlst.append(arr2[0])
            arr2=arr2[1:]
        elif(len(arr2)==0):
            merlst.append(arr1[0])
            arr1=arr1[1:]
        elif(arr1[0]<arr2[0]):
            merlst.append(arr1[0])
            arr1=arr1[1:]
        else:
            merlst.append(arr2[0])
            arr2=arr2[1:]

    return merlst


print(sort(array))

    