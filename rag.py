import ollama

with open("data.txt", "r", encoding="utf-8") as f:
    context = f.read()[:5000]

question = input("Ask a question: ")

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": f"Context: {context}\n\nQuestion: {question}"
        }
    ]
)

print(response["message"]["content"])