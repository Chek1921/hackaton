import  json
import ast
f = open("answers.txt","r").read()
print(f)
result = ast.literal_eval(f)
print(type(result))