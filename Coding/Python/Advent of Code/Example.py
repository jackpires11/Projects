n = 0
flag = 0
counter = 0

while True:
    n += 1
    flag += 1
    if flag == 1000000:
        counter +=1
        print(counter)
        flag = 0
