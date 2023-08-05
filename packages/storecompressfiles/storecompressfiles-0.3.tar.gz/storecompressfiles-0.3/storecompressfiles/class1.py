def encode(s):
  #old_size=sys.getsizeof(s)
  code=""
  for i in s:
    if i=="’" or i=="‘":continue
    sl=len(bin(ord(i)).replace("0b",""))
    z='0'*(7-sl)
    code+=z+bin(ord(i)).replace("0b","")
  
  s1,s2="",""
  #print(len(code))
  for i in range(len(code)//2):
    s1+=code[i]
    s2+=code[len(code)-i-1]
  
  half_code=""
  for i in range(len(s1)):
    if s1[i]=="1" and s2[i]=="0":half_code+="5"
    elif s1[i]=="0" and s2[i]=="1":half_code+="6"
    else:half_code+=str(int(s1[i])+int(s2[i]))
  
  if len(code)%2!=0:
    if code[(len(code)//2)]=="0":half_code+="3"
    else:half_code+="4"
  #new_size=sys.getsizeof(int(half_code))
  #compress_perc=round(((old_size-new_size)/old_size)*100,2)
  #print("COMPRESSION RATE: ",compress_perc)
  #print(half_code)
  #print(code)
  return int(half_code)

def decode(x):
 
  de=""
  s1,s2="",""
  for i in str(x):
    if i=="5":
      s1+="1"
      s2+="0"
    elif i=="6":
      s1+="0"
      s2+="1"
    elif i=="2":
      s1+="1"
      s2+="1"
    elif i=="0":
      s1+="0"
      s2+="0"
  #print(s1+s2[::-1])
  if str(x)[-1]=="4" or str(x)[-1]=="3":
    if str(x)[-1]=="3":de=s1+"0"+s2[::-1]
    else:de=s1+"1"+s2[::-1]
  else:de=s1+s2[::-1]


  new=""
  for i in range(0,len(de),7):new+=chr(int(de[i:i+7],2))
  return new
