
import requests

link = "https://api.thecatapi.com/v1/images/search?limit=10"
a: list[int] = []


answer: list[dict[str,str | int]] = requests.get(link).json()

for i in range(10):
    img_url = answer[i]['url']
    img = requests.get(img_url).content
    format = img_url[-3:]
    print(i)



    with open (f'cats/cat{i}.{format}', 'wb') as file:
        file.write(img)

   









