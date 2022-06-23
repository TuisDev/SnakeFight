num = 0b10010001

for i in range(8):
    print((num << i & 0xff) >> 7)
