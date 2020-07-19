import lirc
sockid = lirc.init("slidepuzzle")

while True:
  codeIR = lirc.nextcode()
  if "up" in codeIR():
    print("UP")
  print(codeIR)