x = int(input('Enter a number: '))
perfectCube = True
counter = 0
for i in range(x):
    i +=1
    if counter ** 3 == x:
        perfectCube = True
        break;
    else:
        perfectCube = False

if perfectCube:
    print(counter)
else:
    print("error")