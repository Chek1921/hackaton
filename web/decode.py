import chardet

data = b"\x89\x0c\x17\xae\xda\x9d\xc0\xc0\x00\x00\x00\x01"
detected = chardet.detect(data)
decoded = data.decode('cp866')
print(decoded)