# Currently inserting sub instructions into stack.

import sys
import argparse
import json
import memory

symbols = {}
lambdas = []
staticMemory = memory.StaticMemory()
symCount = 0

alphabet = "abcdefghijklmnopqrstuvwxyz_"

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
    asm += compileExpression(progArr[i], lineNum=(asm.count("\n")))
  asm += "HLT ;\n"

  memoryStr = staticMemory.toString()
  for i in range(0, len(lambdas)):
    lineNum = asm.count("\n")
    asm = asm.replace("lambda__"+str(i), str(lineNum))
    memoryStr = memoryStr.replace("lambda__"+str(i), str(lineNum))
    asm += lambdas[i]
  asm+="&\n"
  asm += memoryStr
  print (asm)


def compileExpression(expArr, scope="", lineNum=0):
  if (expArr[0] == "lambda"):
    return processlambda(str(len(lambdas)), expArr[1], expArr[2])

  global symCount, staticMemory, symbols
  asm = ""
  innerASM = []
  args = []
  for i in range(1,len(expArr)):
    if (isinstance(expArr[i], list)):
      if (expArr[0] == "if"):
        continue
      asm+=compileExpression(expArr[i],lineNum=(lineNum+asm.count("\n")))
      loc = staticMemory.malloc(1)
      asm += "STA " + str(loc) + ";\n"
      expArr[i] = "__" + str(symCount)
      symbols[expArr[i]] = loc
      symCount += 1
    else:
      if (scope+str(expArr[i]) not in symbols):
        if (isinstance(expArr[i], (int, str))):
          loc = staticMemory.malloc(1)
          if (isinstance(expArr[i], int)):
            staticMemory.set(loc, expArr[i])
          symbols[scope+str(expArr[i])] = loc
        expArr[i] = scope+str(expArr[i])
        innerASM.append(None)

  if (expArr[0] == "+"):
    asm += add(expArr[1], expArr[2])
  elif (expArr[0] == "-"):
    asm += sub(expArr[1], expArr[2])
  elif (expArr[0] == "let"):
    asm += let(expArr[1], expArr[2])
  elif (expArr[0] == "if"):
    asm += ifBlock(expArr[1], expArr[2], expArr[3], (lineNum+asm.count("\n")))
  elif (expArr[0] in symbols):
    asm += gotoLambda(expArr[0], expArr[1:])

  return asm

def processlambda(name, args, body):
  global symbols, lambdas
  asm = ""
  for i in range(0, len(args)):
    loc = staticMemory.malloc(1)
    symbol = name + "__" + args[i]
    symbols[symbol] = loc
  for i in range(0, len(body)):
    asm += compileExpression(body[i], name + "__")
  lambdas.append(asm)
  loc = staticMemory.malloc(1)
  staticMemory.set(loc, "lambda__"+name)
  return "LDA " + str(loc) + ";\n"

def gotoLambda(symName, args):
  return "JMP " + str(symbols[symName]) + ";\n"

def ifBlock(cond, trueBlock, falseBlock, lineNum):
  print("Line nums = " + str(lineNum))
  result = ""
  if (isinstance(cond, list)):
    result = compileExpression(cond, lineNum=(lineNum+result.count("\n")))
  else:
    result = "LDA " + str(symbols[cond]) + ";\n"

  if (isinstance(trueBlock, list)):
    trueBlock = compileExpression(trueBlock)
  else:
    trueBlock = "LDA " + str(symbols[trueBlock]) + ";\n"

  if (isinstance(falseBlock, list)):
    falseBlock = compileExpression(falseBlock)
  else:
    falseBlock = "LDA " + str(symbols[falseBlock]) + ";\n"

  offset = lineNum+result.count("\n")+trueBlock.count("\n")+falseBlock.count("\n")+3
  trueBlock += "JMP " + str(offset) + ";\n"

  result += "JMZ " + str(lineNum+result.count("\n")+trueBlock.count("\n")+2) + ";\n"
  result += trueBlock
  result += falseBlock
  return result

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
def let(symbol, value):
  asm = "LDA " + str(symbols[value]) + ";\n"
  asm += "STA " + str(symbols[symbol]) + ";\n"
  return asm



"""
Converts source code into a multi-dim array.
Ex: "(set x 3)(set y (+ x 5))" -> [["set", "x", 3], ["set", "y", ["+", "x", 5]]]
"""
def parse(f):
  global alphabet

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
      if (result[(len(result)-2):] == "[\""):
        result=result[0:(len(result)-1)]
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
      if (not inSymbolName and not inFuncitonName and c.lower() in alphabet):
        inSymbolName = True
        result += "\""
      result += c
  result = result[:len(result)-1]
  result += "]"
  print (result)
  return json.loads(result)

if __name__ == "__main__":
  main()