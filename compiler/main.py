# Currently inserting sub instructions into stack.

import sys
import argparse
import json
import memory

symbols = {}
lambdas = {}
staticMemory = memory.StaticMemory()
symCount = 0

alphabet = "abcdefghijklmnopqrstuvwxyz_"

def main(argv=sys.argv):
  parser = argparse.ArgumentParser(description='Simple programming language')
  parser.add_argument('-f', dest='file', action='store', help='sum the integers (default: find the max)')

  args = parser.parse_args()
  f = open(args.file, 'r')
  progArr = parse(f)
  compile(progArr)

def compile(progArr):
  asm = ""
  for i in range(0, len(progArr)):
    asm += compileExpression(progArr[i], lineNum=(asm.count("\n")))
  asm += "HLT ;\n"

  memoryStr = staticMemory.toString()
  for i in lambdas:
    lineCount = str(asm.count("\n")+1)
    asm += lambdas[i]["body"]
    asm = asm.replace(lambdas[i]["namespace"], lineCount)
    memoryStr = memoryStr.replace(lambdas[i]["namespace"], lineCount)
  asm+="&\n"
  asm += memoryStr
  print (asm)


def compileExpression(expArr, scope="", lineNum=0, quoted=False):
  global symCount, staticMemory, symbols, lambdas

  if (expArr[0] == "lambda"):
    return processlambda(str(len(lambdas)), expArr[1], expArr[2])

  asm = ""
  innerASM = []
  args = []

  start = 1
  if ((scope + expArr[0]) in symbols):
    start = 0
  for i in range(start,len(expArr)):
    if (isinstance(expArr[i], list)): # Compile a sub-expression
      if (expArr[0] == "if"):
        continue

      result = ""      
      if (expArr[0] == "let" and isinstance(expArr[1], list)):
        break
      else:
        result=compileExpression(expArr[i], scope, lineNum=(lineNum+asm.count("\n")))

      loc = staticMemory.malloc(1)

      if (expArr[i][0]=="lambda"):
        staticMemory.set(loc, result[1])
        symbols[expArr[1]] = result[1]
      else:
        asm += result
        asm += "STA " + str(loc) + ";\n"
      expArr[i] = "__" + str(symCount)
      symbols[expArr[i]] = loc
      symCount += 1
    else: # Compile a symbol
      argName = scope+str(expArr[i])
      unprocessedArgName = expArr[i]
      print (expArr[i])
      if (isinstance(unprocessedArgName, int)):
        argName = str(expArr[i])
        expArr[i] = str(expArr[i])
      else:
        expArr[i] = argName
      if (argName not in symbols):
        loc = staticMemory.malloc(1)
        if (isinstance(unprocessedArgName, int)):
          staticMemory.set(loc, expArr[i])
        symbols[argName] = loc
        innerASM.append(None)

  if (quoted):
    return ""

  if (expArr[0] == "+"):
    asm += add(expArr[1], expArr[2])
  elif (expArr[0] == "-"):
    asm += sub(expArr[1], expArr[2])
  elif (expArr[0] == "let"):
    asm += let(expArr[1], expArr[2])
  elif (expArr[0] == "if"):
    asm += ifBlock(expArr[1], expArr[2], expArr[3], (lineNum+asm.count("\n")))
  elif (expArr[0] == "print"):
    asm += printInt(expArr[1])
  elif (expArr[0] in symbols):
    asm += goToFunction(expArr[0], expArr[1:])

  return asm

def processFunction(name, args, body):
  namespace = name + "__"

  symbols[name] = staticMemory.malloc(1)

  lambdas[name] = {}

  lambdas[name]["namespace"] = namespace
  staticMemory.set(symbols[name], namespace)
  
  for i in range(0, len(args)):
    args[i] = namespace + args[i]
    symbols[args[i]] = 3+i;
    #symbols[args[i]] = staticMemory.malloc(1)
  
  lambdas[name]["args"] = args;
  lambdas[name]["argCount"] = len(args)

  bodyStr = ""
  for i in range(0, len(body)):
    bodyStr += compileExpression(body[i], namespace)

  bodyStr += "JAL -1;\n"
  lambdas[name]["body"] = bodyStr


  return ("LDA " + namespace + ";\n", namespace)

def goToFunction(symName, args, inFunction=False):
  asm = ""
  loc = symbols[symName]
  if (symbols[symName] <= 6):
    loc = staticMemory.malloc(1)
    asm += "LDA " + str(symbols[symName]) + ";\n"
    asm += "STA " + str(loc) + ";\n"

  for i in range(0, len(args)):
    
    asm += "ALC " + str(3+i) + ";\n"
    asm += "LDA " + str(symbols[args[i]]) + ";\n";
    asm += "STA " + str(i+3) + ";\n"

  asm += "JAL " + str(loc) + ";\n"

  for i in range(0, len(args)):
    asm += "DLC " + str(3+i) + ";\n"
  return asm

def processlambda(name, args, body):
  global symbols, lambdas
  asm = ""

  recurseSave = "ALC " + str(len(args)) + ";\n" # Grow the stack
  recurseLoad = ""
  for i in range(0, len(args)):
    loc = staticMemory.malloc(1)
    symbol = name + "__" + str(i)
    symbols[symbol] = loc
    
    recurseSave += "LDA " + str(loc) + ";\n" # Load the argument from memory
    recurseSave += "STI 0;\n" # Store the argument on the stack
    recurseSave += incrementStack()

    recurseLoad += "LDI 0;\n" # Load item from top of stack
    recurseLoad += "STA " + str(loc) + ";\n" # Store item in argument
    recurseLoad += decrementStack()

  recurseLoad += "DLC " + str(len(args)) + ";\n" 
  recurseLoad += "JAL 0;\n" # return

  for i in range(0, len(body)):
    asm += compileExpression(body[i], str(name) + "__")

  asm += recurseLoad

  #asm.replace("JMP", recurseSave + "JMP")
  #asm.replace("JMP")
  lambdas.append({'asm': asm, 'prepend': recurseSave, 'postpend': recurseLoad})
  loc = staticMemory.malloc(1)
  staticMemory.set(loc, "lambda__"+name)

  return loc#"LDA " + str(loc) + ";\n"

def gotoLambda(symName, args):
  prefix = staticMemory.get(symbols[symName]).split("__")[1] + "__"
  asm = ""
  for i in range(0, len(args)):
    asm += "LDA " + str(symbols[str(args[i])]) + ";\n" # Load the symbol into PC
    asm += "STA " + str(symbols[prefix + str(i)]) + ";\n" # Store the symbol as the argument
  return asm + "JAL " + staticMemory.get(symbols[symName]) + ";\n"


def ifBlock(cond, trueBlock, falseBlock, lineNum):
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

def printInt(num):
  result = "LDA 1;\n"
  result += "SYS " + str(symbols[num]) + ";\n"
  return result

# allocates memory for a symbol and returns instructions for placing a int into that memory
def let(symbol, value):
  if (isinstance(symbol, list)):
    processFunction(symbol[0], symbol[1:], value)
    return ""

  """
  if (value in lambdas):
    symbols[symbol] = symbols[value]
    return ""
  """

  asm = "LDA " + str(symbols[value]) + ";\n"
  asm += "STA " + str(symbols[symbol]) + ";\n"
  return asm

def incrementStack():
  result = "LDA 0;\n"
  result += "ADD 1;\n"
  result += "STA 0;\n"
  return result

def decrementStack():
  result = "LDA 0;\n"
  result += "ADD 2;\n"
  result += "STA 0;\n"
  return result


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
  return json.loads(result)

if __name__ == "__main__":
  main()