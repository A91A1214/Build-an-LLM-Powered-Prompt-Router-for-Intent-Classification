import sys
from router import classify_intent, route_and_respond, log_request

def main():
    print("--- LLM Prompt Router ---")
    print("Type 'exit' to quit.")
    
    # 15 Test cases provided in prompt
    test_cases = [
        "how do i sort a list of objects in python?",
        "explain this sql query for me",
        "This paragraph sounds awkward, can you help me fix it?",
        "I'm preparing for a job interview, any tips?",
        "what's the average of these numbers: 12, 45, 23, 67, 34",
        "Help me make this better.",
        "I need to write a function that takes a user id and returns their profile, but also i need help with my resume.",
        "hey",
        "Can you write me a poem about clouds?",
        "Rewrite this sentence to be more professional.",
        "I'm not sure what to do with my career.",
        "what is a pivot table",
        "fxi thsi bug pls: for i in range(10) print(i)",
        "How do I structure a cover letter?",
        "My boss says my writing is too verbose."
    ]

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("\nRunning test cases...\n")
        for test in test_cases:
            process_message(test)
        print("\nTests complete. Check route_log.jsonl for results.")
        return

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                break
            process_message(user_input)
        except KeyboardInterrupt:
            break

def process_message(message: str):
    print(f"User: {message}")
    
    # Classify intent
    intent_data = classify_intent(message)
    intent = intent_data["intent"]
    confidence = intent_data["confidence"]
    
    print(f"Detected Intent: {intent} (Confidence: {confidence:.2f})")
    
    # Route and respond
    response = route_and_respond(message, intent_data)
    print(f"Assistant: {response}")
    
    # Log
    log_request(intent, confidence, message, response)

if __name__ == "__main__":
    main()
