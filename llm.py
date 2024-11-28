import openai

apikey = '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'
messages = [{"role": "user",
             "content": f'''You are a intelligent assistant for only financial data in Indian Stock market so restrict 
             your answers to only that.
              Here is the advisory data that we provide to all our users in JSON, 
              Here is the advisory Stocks we have from the a list , 
              Here are the details of each and every advisory stock data , 
              Here are the details for the news for the advisory Stocks. 
              Summarise the news and keep the relevant points handy as and when user asks, 
              Now help the user with their questions on advisory, fundamentals and books of the company. 
              '''}]

client = openai.OpenAI(
    api_key=apikey,
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user", "content": "Refer to yourself as AngelFin Advisor and say HI"
        }
    ],
    model="gpt-3.5-turbo",
)


def process_msg(message):
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        return reply
