# pip install googletrans==4.0.0rc1

from googletrans import Translator

word = "merhaba"

translator = Translator()
translated = translator.translate(word, dest="en")
result = translated.text

print(result)

message = f"$ {result}, my name is Jeff, I like programming"

txt1 = message.split(", ")
print(txt1)

txt2 = message.split("$ ")
listToStr = "".join(map(str, txt2))
print(listToStr)
