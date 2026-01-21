# Импорт необходимого класса OpenAI из библиотеки openai
from openai import OpenAI

# Определение класса ChatGptService для взаимодействия с API ChatGPT
class ChatGptService:
    client: OpenAI = None
    message_list: list = None

    # Конструктор класса, инициализирующий клиент OpenAI с заданным токеном
    def __init__(self, token):
        # Инициализация клиента OpenAI с использованием переданного API-ключа
        self.client = OpenAI(
            api_key=token#, base_url="https://openai.javarush.com/v1" #(прокси для моего учебного api-key)
        )

        # Инициализация списка сообщений для хранения диалога
        self.message_list = []

    # Метод для отправки .message_list в API ChatGPT и получения ответа
    async def send_message_list(self) -> str:
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # модель указывается в соответствии с имеющимся тарифом
            messages=self.message_list,
            max_tokens=3000,#максимум 3000 токенов в ответе
            temperature=0.9,#температура креативности ответа
        )

        # Получение ответа от модели и добавление его в .message_list
        message = completion.choices[0].message
        self.message_list.append(message)

        # Возврат содержимого ответа
        return message.content

    # Метод для установки системного сообщения (промпта) в .message_list
    def set_prompt(self, prompt_text: str) -> None:
        self.message_list.clear()
        self.message_list.append({"role": "system", "content": prompt_text})

    # Метод для добавления пользовательского сообщения и отправки .message_list
    async def add_message(self, message_text: str) -> str:
        self.message_list.append({"role": "user", "content": message_text})
        return await self.send_message_list()

    # Метод для отправки одного системного и одного пользовательского сообщения
    async def send_question(self, prompt_text: str, message_text: str) -> str:
        # Очистка .message_list и добавление системного и пользовательского сообщений
        self.message_list.clear()
        self.message_list.append({"role": "system", "content": prompt_text})
        self.message_list.append({"role": "user", "content": message_text})

        # Отправка .message_list и возврат ответа
        return await self.send_message_list()
