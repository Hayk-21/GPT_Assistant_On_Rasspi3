import openai

openai.api_key = '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'

res = openai.ChatCompletion.create(
	model='gpt-3.5-turbo',
	messages=[{'role':'user', 'content':'Write a poem'}]
)

print(res['choices'][0]['message']['content'])
