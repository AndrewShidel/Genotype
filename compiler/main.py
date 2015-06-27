# Currently inserting sub instructions into stack.

import sys
import argparse
import json
import memory

symbols = {}
staticMemory = memory.StaticMemory()
symCount = 0

def main(argv=sys.argv):
  parser = argparse.ArgumentParser(description='Simple programming language')
  parser.add_argument('-f', dest='file', action='store', help='sum the integers (default: find the max)')

  args = parser.parse_args()
  print (args.file)
  f = open(args.file, 'r')
  progArr = parse(f)
  compile(progArr)

def compile(progArr):
  asm = ""
  for i in range(0, len(progArr)):
    asm += compileExpression(progArr[i])
  asm += "HLT ;\n&\n"
  asm += staticMemory.toString()
  print (asm)


def compileExpression(expArr):
  global symCount, staticMemory, symbols
  asm = ""
  innerASM = []
  args = []
  for i in range(1,len(expArr)):
    if (isinstance(expArr[i], list)):
      asm+=compileExpression(expArr[i])
      loc = staticMemory.malloc(1)
      asm += "STA " + str(loc) + ";\n"
      expArr[i] = "__" + str(symCount)
      symbols[expArr[i]] = loc
      symCount += 1
    else:
      if (expArr[i] not in symbols):
        if (isinstance(expArr[i], (int, str) )):
          loc = staticMemory.malloc(1)
          staticMemory.set(loc, expArr[i])
          symbols[expArr[i]] = loc
        innerASM.append(None)

  if (expArr[0] == "+"):
    asm += add(expArr[1], expArr[2])
  elif (expArr[0] == "-"):
    asm += sub(expArr[1], expArr[2])
  return asm

# Arithmetic Operations:
# num1, num2 - memory locations
def add(num1, num2):
  result = "LDA " + str(symbols[num1]) + ";\n"
  result += "ADD " + str(symbols[num2]) + ";\n"
  return result;
def sub(num1, num2):
  result = "LDA " + str(symbols[num1]) + ";\n"
  result += "SUB " + str(symbols[num2]) + ";\n"
  return result;
def multiply(num1, num2):
  return
def divide(num1, num2):
  return

# allocates memory for a symbol and returns instructions for placing a int into that memory
def set(symbol, value):
  return



"""
Converts source code into a multi-dim array.
Ex: "(set x 3)(set y (+ x 5))" -> [["set", "x", 3], ["set", "y", ["+", "x", 5]]]
"""
def parse(f):
  result = "["
  paranCount = 0
  inFuncitonName = False
  inSymbolName = False
  while f:
    c = f.read(1)
    if not c:
      print ("End of file")
      break
    if (c=='('):
      paranCount+=1
      result += "[\""
      inFuncitonName = True
    elif (c==')'):
      if (inSymbolName):
        inSymbolName = False
        result += "\""
      paranCount-=1
      result += "]"
      if (paranCount==0):
        result += ","
    elif (c.isspace() and paranCount>0):
      if (inSymbolName):
        result += "\""
        inSymbolName = False
      if (inFuncitonName):
        result += "\""
        inFuncitonName = False
      result += ","
    elif (not c.isspace()):
      if (not inSymbolName and not inFuncitonName):
        inSymbolName = True
        result += "\""
      result += c
  result = result[:len(result)-1]
  result += "]"
  return json.loads(result)

if __name__ == "__main__":
  main()