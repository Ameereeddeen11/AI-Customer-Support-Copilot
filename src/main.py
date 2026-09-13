"""
This is a simple file to verify that the ollama package is working correctly.
It will just send a prompt to the model and print the response.
"""

import ollama

def ask_llm(
    prompt: str,
    model: str = "qwen2.5:14b"
) -> str:
    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]

if __name__ == "__main__":
    question: str = "Explain to me in one sentence what an embedding is, as if I were a complete beginner."

    print(f"Question: {question}\n")
    print(f"Answer: {ask_llm(question)}")