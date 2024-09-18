from ollama import Client
client = Client(host='http://10.61.0.125:11434')
response = client.chat(model='llama3.1', messages=[
  {
    "role": "user",
    "content": "why is the sky blue?"
  },
  {
    "role": "assistant",
    "content": "due to rayleigh scattering."
  },
  {
    "role": "user",
    "content": "how is that different than mie scattering?"
  }
])
print(response['message']['content'])