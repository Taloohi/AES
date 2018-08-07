def bi(x): #Converts decimal to 8 bit binary integer
    return("{0:{fill}8b}".format(x, fill='0'))

S = [[99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118],
     [202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192],
     [183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21],
     [4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 179, 117],

       #

     [81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210],     

     [83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207],


     [208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168],


     [9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132],  #Modified Sbox   


     [205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115],
     [96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219],
     [224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121],
     [231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8],
     [186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138],
     [112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158],
     [225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223],
     [140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]]

#plain = "00112233445566778899aabbccddeeff"
#key = "000102030405060708090a0b0c0d0e0f"

plain = "0000000000000000000000000000abd6"
key = "1a0c24f2875493bcb7080e43930f5686"

def group(text):
    grouped = [
          [int(text[0:2],16),int(text[8:10],16), int(text[16:18],16),  int(text[24:26],16)],
          [int(text[2:4],16),int(text[10:12],16),int(text[18:20],16), int(text[26:28],16)],
          [int(text[4:6],16),int(text[12:14],16),int(text[20:22],16), int(text[28:30],16)],
          [int(text[6:8],16),int(text[14:16],16),int(text[22:24],16),  int(text[30::],16)]
           ]
    return grouped

#--------------------------------------------------------------------------------------------------------

#Byte Substitute 
    
def BS(a): #ByteSub
    b = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    for i in range(0,4):
        for j in range(0,4):
            b[i][j] = S[int(f"{a[i][j]:#0{4}x}"[2],16)][int(f"{a[i][j]:#0{4}x}"[3],16)] #Converts to hex then back to decimal for location

    return b


#--------------------------------------------------------------------------------------------------------

#Shifter


def SR(b): #Shift Row
    for i in range(0,4):
        b[i] = b[i][i::]+b[i][:i:]
    return b


#--------------------------------------------------------------------------------------------------------

#MixColumn Product

def prod(a,b):
    second = bi(a)
    result = 0

    if b == 1:
        return a
    else:
        if second[0] == '1':
            second = '0' + second[1::]
            second = second[1::]+second[:1:]
            result = int(second,2)^27
        elif second[0] == '0':
            result = second[1::]+second[:1:]
            result = int(result,2)

        if b == 2:
            return result
        elif b == 3:
            return result^a         

#--------------------------------------------------------------------------------------------------------

#MixColumn    

def MC(c):
    M = [[2,3,1,1],
         [1,2,3,1],
         [1,1,2,3],
         [3,1,1,2]]

    D = [[0 for x in range(4)] for y in range(int((4)))]

    for i in range(0,4):
        for j in range(0,4):
            D[i][j] = prod(c[0][j],M[i][0])^prod(c[1][j],M[i][1])^prod(c[2][j],M[i][2])^prod(c[3][j],M[i][3])

    return D    

#--------------------------------------------------------------------------------------------------------
#RoundKey Addition
def ARK(d,k):
    E = [[0 for x in range(4)] for y in range(int((4)))]

    for i in range(0,4):
        for j in range(0,4):
            E[i][j] = d[i][j]^k[i][j]

    return E
#--------------------------------------------------------------------------------------------------------


inputState = group(plain)

key1 = group(key)


wHex = [[int(key[0:2],16),int(key[2:4],16),int(key[4:6],16),int(key[6:8],16)],
        [int(key[8:10],16),int(key[10:12],16),int(key[12:14],16),int(key[14:16],16)],
        [int(key[16:18],16),int(key[18:20],16),int(key[20:22],16),int(key[22:24],16)],
        [int(key[24:26],16),int(key[26:28],16),int(key[28:30],16),int(key[30::],16)]
        ]

W = [[0 for x in range(4)] for y in range(int((44)))] # Sets size of W
W[0:4] = wHex[0:4]

def KS(W,j):
    rot = [W[1],W[2],W[3],W[0]]

    RC = [0,1,2,4,8,16,32,64,128,27,54]

    sub = [0,0,0,0]
    for i in range(0,4):
            sub[i] = S[int(f"{rot[i]:#0{4}x}"[2],16)][int(f"{rot[i]:#0{4}x}"[3],16)]

    Y = [sub[0]^RC[j],sub[1],sub[2],sub[3]]

    return Y

def XOR(W,Q):
    g = [f"{W[0]:#0{4}x}"[2::],f"{W[1]:#0{4}x}"[2::],f"{W[2]:#0{4}x}"[2::],f"{W[3]:#0{4}x}"[2::]]
    e = ''.join(g)

    f = [f"{Q[0]:#0{4}x}"[2::],f"{Q[1]:#0{4}x}"[2::],f"{Q[2]:#0{4}x}"[2::],f"{Q[3]:#0{4}x}"[2::]]
    h = ''.join(f)

    X = int(e,16)^int(h,16)

    transform = f"{X:#0{10}x}"[2::]

    out = [int(transform[0:2],16),int(transform[2:4],16),int(transform[4:6],16),int(transform[6:8],16)]
    
    return out
    

for i in range(4,44):
    if (i % 4 == 0):
        W[i] = (XOR(W[i-4],KS(W[i-1],int(i/4))))        
    else:
        W[i] = (XOR(W[i-4],W[i-1])) #W[i-4]^W[i-1]

bs = [[0 for x in range(1)] for y in range(int((11)))]
sr = [[0 for x in range(1)] for y in range(int((11)))]
mc = [[0 for x in range(1)] for y in range(int((11)))]
out = [[0 for x in range(1)] for y in range(int((11)))]


RoundKey = [[*zip(*W[0:4])],[*zip(*W[4:8])],[*zip(*W[8:12])],[*zip(*W[12:16])],[*zip(*W[16:20])],[*zip(*W[20:24])],
            [*zip(*W[24:28])],[*zip(*W[28:32])],[*zip(*W[32:36])],[*zip(*W[36:40])],[*zip(*W[40::])]]

out[0] = ARK(inputState,RoundKey[0])

for i in range(1,10):
    bs[i] = BS(out[i-1])
    sr[i] = SR(bs[i])
    mc[i] = MC(sr[i])

    out[i] = ARK(RoundKey[i],mc[i])


bs[10] = BS(out[9])
sr[10] = SR(bs[10])

out[10] = ARK(RoundKey[10],sr[10])


for i in range(0,11):
	print("\n\n","Key Round ", i, ":")
	for j in range(0,4):
		for k in range(0,4):
			print (hex(RoundKey[i][k][j])[2::]," ",end='')


for i in range(0,11):
	print("\n\n","Output Round", i, ":")
	for j in range(0,4):
		for k in range(0,4):
			print (hex(out[i][k][j])[2::]," ",end='')

