m = '等等'
n = '我很好'

# text = m + n                            # 新增 text 變數，記錄輸入的字串
# repeat = []                             # 新增 repeat 變數為空串列
# not_repeat = []                         # 新增 not_repeat 變數為空串列
# for i in text:                          # 使用 for 迴圈，依序取出每個字元
#     a = text.count(i, 0, len(text))     # 判斷字元在字串中出現的次數
#     if a>1 and i not in repeat:         # 如果次數大於 1，且沒有存在 repeat 串列中
#         repeat.append(i)                  # 將字元加入 repeat 串列
#     if a == 1 and i not in not_repeat:   # 如果次數等於 1，且沒有存在 not_repeat 串列中
#       not_repeat.append(i)              # 將字元加入 not_repeat 串列

# print(repeat)
# print(not_repeat)

repeat = []
not_repeat = []

for i in m:
    a = m.count(i,0, len(m))
    for j in n:
        b = n.count(j,0,len(n))
        if a>1:
            a = 1
            not_repeat.append(i)
        if b>1:
            b = 1
            not_repeat.append(j)
        if (a+b)>1 and i or j not in repeat:
            repeat.append(i)
            repeat.append(j)

print(repeat) #[]
print(not_repeat)  

# from zhon.hanzi import punctuation
# sentence = '你好嗎。'
# sentence_str = punctuation
# print("Chinese ounctuation:",sentence_str)
# for i in punctuation:
#     sentence = sentence.replace(i, '')
# print(sentence)
