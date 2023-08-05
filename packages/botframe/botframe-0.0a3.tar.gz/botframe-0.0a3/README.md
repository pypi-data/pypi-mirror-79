# Как пользоваться

Установка

```
pip install botframe
```

Пример

```python
from botframe import Bot

bot = Bot("token")

@bot.command(["hello"])
def hello(api):
    return "world"

if __name__ == "__main__":
    bot.run()
```
