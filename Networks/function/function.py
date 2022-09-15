
lowercase = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
uppercase = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def caeser_cipher(msg):
    ans = ""
    for i in range(len(msg)):
        if msg[i] in lowercase or msg[i] in uppercase:
            if msg[i].isupper():
                ans += uppercase[(uppercase.index(msg[i]) + 2) % 26]
            elif msg[i].islower():
                ans += lowercase[(lowercase.index(msg[i]) + 2) % 26]
        else:
            ans += str(msg[i])
    return ans

def reverse(msg):
    temp = ""
    for i in range(len(msg) - 1, -1, -1):
        temp += msg[i]
    return temp
    
def reverse_encoding(msg):
    ans = ""
    l = msg.split()
    for element in l:
        ans += reverse(element)
        ans += " "
    return ans[0 : len(ans) - 1]

def decrypt(msg):
    ans = ""
    for i in range(len(msg)):
        if msg[i] in lowercase or msg[i] in uppercase:
            if msg[i].isupper():
                ans += uppercase[(uppercase.index(msg[i]) + 24) % 26]
            elif msg[i].islower():
                ans += lowercase[(lowercase.index(msg[i]) + 24) % 26]
        else:
            ans += str(msg[i])
    msg = ans
    return msg