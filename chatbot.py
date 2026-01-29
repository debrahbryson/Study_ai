import os
import json
from pdfreader import read_pdfs_from_folder

KNOWLEDGE_FILE = "knowledge.json"
SCHOOL_FOLDER = "school"
# Stop words to ignore
STOP_WORDS = {"what","is","are","the","a","an","of","and","to","in","for","on","with","as","by"}

def normalize(word):
    return word.lower().rstrip("s")  # normalize plurals

def select_topic():
    print("📚 Select which notes you want to study:")
    topics = [d for d in os.listdir(SCHOOL_FOLDER) if os.path.isdir(os.path.join(SCHOOL_FOLDER, d))]
    for i, t in enumerate(topics, 1):
        print(f"{i}. {t}")

    choice = input("Enter number: ")
    try:
        choice = int(choice)
        topic = topics[choice - 1]
        print(f"\n📘 Loading knowledge for '{topic}'...\n")
        return topic
    except:
        print("❌ Invalid choice. Defaulting to first topic.")
        return topics[0]

def build_knowledge(topic_folder):
    folder_path = os.path.join(SCHOOL_FOLDER, topic_folder)
    knowledge = read_pdfs_from_folder(folder_path)

    # Save to knowledge.json
    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=2)
    print("✅ Knowledge base built for this topic.")
    return knowledge

def load_knowledge(topic_folder):
    # rebuild knowledge base every time for simplicity
    return build_knowledge(topic_folder)

def answer_question(question, knowledge):
    question_words = {normalize(w) for w in question.split() if normalize(w) not in STOP_WORDS}

    scored = []
    for item in knowledge:
        text = item["text"].lower()
        score = sum(text.count(word) for word in question_words)
        if score >= 1:  # minimal threshold
            scored.append((score, item))

    if not scored:
        return "❌ I couldn't find a relevant answer in these notes."

    scored.sort(key=lambda x: x[0], reverse=True)
    response = ""
    for score, item in scored[:3]:  # top 3 matches
        source = item.get("source", "Unknown PDF")
        response += f"\n📄 Source: {source}\n"
        response += item["text"][:700] + "\n"
    return response

def chatbot():
    print("🤖 Study Chatbot (Powered by your school notes)")
    print("Type 'exit' to quit.\n")

    topic = select_topic()
    knowledge = load_knowledge(topic)

    while True:
        question = input("You: ")
        if question.lower() == "exit":
            break
        response = answer_question(question, knowledge)
        print("\nBot:", response, "\n")

if __name__ == "__main__":
    chatbot()
