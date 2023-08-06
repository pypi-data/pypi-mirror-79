def Caesar(m, k):
    cm = ""
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in m.upper():
        f = letters.find(i)
        if i not in letters:
            cm += i
        else:
            cm += letters[(f + k) % len(letters)]
    return cm.lower()
def Binary(a):
  a = a.lower()
  res = []
  i = 0
  while i < len(a):
    binary = {"a":"01000001",
              "b":"01000010",
              "c":"01000011",
              "d":"01000100",
              "e":"01000101",
              "f":"01000110",
              "g":"01000111",
              "h":"01001000",
              "i":"01001001",
              "j":"01001010",
              "k":"01001011",
              "l":"01001100",
              "m":"01001101",
              "n":"01001110",
              "o":"01001111",
              "p":"01010000",
              "q":"01010001",
              "r":"01010010",
              "s":"01010011",
              "t":"01010100",
              "u":"01010101",
              "v":"01010110",
              "w":"01010111",
              "x":"01011000",
              "y":"01011001",
              "z":"01011010",
              " ":"00100000"}
    res+=binary[a[i]]
    i+=1
  res = ''.join(res)
  return res
def MorseCode(word):
	word = word.upper()
	i = 0
	solution=[]
	alphabet = ["A","B","C","D","E","F","G","H","I","J",
	"K","L","M","N","O",
	"P","Q","R","S","T","U","V","W","X","Y","Z",
	"1","2","3","4","5","6","7","8","9","0"]
	while i < len(word):
		if word[i] == alphabet[0]:
			solution+="._"
		elif word[i] == alphabet[1]:
			solution+="_..."
		elif word[i] == alphabet[2]:
			solution+= "_._."
		elif word[i] == alphabet[3]:
			solution+= "_.."
		elif word[i] == alphabet[4]:
			solution+= "."
		elif word[i] == alphabet[5]:
			solution+= ".._."
		elif word[i] == alphabet[6]:
			solution+= "_ _."
		elif word[i] == alphabet[7]:
			solution+= "...."
		elif word[i] == alphabet[8]:
			solution+= ".."
		elif word[i] == alphabet[9]:
			solution+= "._ _ _"
		elif word[i] == alphabet[10]:
			solution+= "_._"
		elif word[i] == alphabet[11]:
			solution+= "._.."
		elif word[i] == alphabet[12]:
			solution+= "_ _"
		elif word[i] == alphabet[13]:
			solution+= "_."
		elif word[i] == alphabet[14]:
			solution+= "_ _ _"
		elif word[i] == alphabet[15]:
			solution+= "._ _."
		elif word[i] == alphabet[16]:
			solution+= "_ _._"
		elif word[i] == alphabet[17]:
			solution+= "._."
		elif word[i] == alphabet[18]:
			solution+= "..."
		elif word[i] == alphabet[19]:
			solution+= "_"
		elif word[i] == alphabet[20]:
			solution+= ".._ "
		elif word[i] == alphabet[21]:
			solution+= "..._"
		elif word[i] == alphabet[22]:
			solution+= "._ _"
		elif word[i] == alphabet[23]:
			solution+= "_.._"
		elif word[i] == alphabet[24]:
			solution+= "_._ _"
		elif word[i] == alphabet[25]:
			solution+= "_ _.."
		elif word[i] == alphabet[26]:
			solution+= "._ _ _ _"
		elif word[i] == alphabet[27]:
			solution+= ".._ _ _"
		elif word[i] == alphabet[28]:
			solution+= "..._ _"
		elif word[i] == alphabet[29]:
			solution+= "...._"
		elif word[i] == alphabet[30]:
			solution+= "....."
		elif word[i] == alphabet[31]:
			solution+= "_...."
		elif word[i] == alphabet[32]:
			solution+= "_ _..."
		elif word[i] == alphabet[33]:
			solution+= "_ _ _.."
		elif word[i] == alphabet[34]:
			solution+= "_ _ _ _."
		elif word[i] == alphabet[35]:
			solution+= "_ _ _ _ _"
		i+=1
	solution = ' '.join(solution)
	return solution 
def Atbash(s):
    abc = "abcdefghijklmnopqrstuvwxyz"
    return s.translate(str.maketrans(
        abc + abc.upper(), abc[::-1] + abc.upper()[::-1]))