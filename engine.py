from ollama import chat

def main():
    prompt = "In one sentence, explain what AC-4 (Information Flow Enforcement) means."
    resp = chat(
        model="llama3:8b",
        messages=[{"role": "user", "content": prompt}],
    )
    print(resp["message"]["content"])

if __name__ == "__main__":
    main()