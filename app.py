from flask import Flask, render_template, request, jsonify
import language_tool_python

app = Flask(__name__)
tool = language_tool_python.LanguageTool('en-US')

def chatbot_reply(user):
    matches = tool.check(user)
    corrected = language_tool_python.utils.correct(user, matches)

    # Polite responses
    user_lower = user.lower()

    if "hello" in user_lower or "hi" in user_lower:
        reply = "Hello! 😊 How are you doing today?"
    elif "how are you" in user_lower:
        reply = "I'm doing great! Thanks for asking 😊 How about you?"
    elif "your name" in user_lower:
        reply = "I'm your English Learning Assistant 🤖"
    elif user.strip() == "":
        reply = "Please type something so I can help you 😊"
    else:
        reply = "That's a good sentence 👍 Keep practicing and improving!"

    return reply, corrected


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user = request.json["message"]
    reply, corrected = chatbot_reply(user)
    return jsonify({
        "reply": reply,
        "corrected": corrected
    })


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
