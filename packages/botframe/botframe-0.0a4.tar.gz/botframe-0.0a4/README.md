# Как пользоваться

Установка

```
pip install vk-api botframe
```

Пример

```python
from botframe import Bot


bot = Bot('123abc', 123465)


@bot.arg()
def name(event, bot):
    text = event.message['text'].split()
    if len(text) > 2:
        for num in range(2, len(text)):
            if " ".join([text[num-2], text[num-1]]).lower() == 'i am':
                return text[num]
    return None


@bot.command(["i am"], all_text=True)
def hello(api, name):
    if name:
        message = f"Hello, {name}"
    else:
        message = f"Hello"
    api.reply(message=message)
    return "world"


if __name__ == "__main__":
    bot.run()

```

```
>> Hello, Bot. I am Eugene
<< Hello, Eugene

>> word word i am
<< Hello
```

Спасибо [python273](https://github.com/python273) за [vk_api](https://github.com/python273/vk_api), который используется в этом проекте как бэкэнд.
