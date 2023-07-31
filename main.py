import streamlit as st
import speech_recognition as sr
from textblob import TextBlob
import openai

# Function to correct the spelling of input text
def correct_spelling(input_text):
    if not input_text:
        return input_text

    blob = TextBlob(input_text)
    corrected_text = blob.correct()
    return str(corrected_text)

# Function to chat with GPT-3.5 using OpenAI API
def chat_with_gpt(input_topic):
    # GPT-3.5 API call using OpenAI API
    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
    openai.api_key = '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'
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=input_topic,
        max_tokens=100
    )
    answer = response['choices'][0]['text'].strip()
    return answer

def main():
    st.title("Ask your Chatbot")

    # Sidebar with black background containing chat history and previous chats
    st.sidebar.title("Chat History")
    chat_history = st.sidebar.empty()
    previous_chats = []

    # Text input box for user to type or use speech recognition
    input_topic = st.text_input("Your Message:")
    speech_button = st.button("🎤 Voice Recognize")

    if speech_button:
        # Use speech recognition to get user input
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Start Asking your question...")
            audio = recognizer.listen(source)

        try:
            st.write("Please wait...")
            input_topic = recognizer.recognize_google(audio)
            st.text_area("Your Message:", value=input_topic, key='input_text')
        except sr.UnknownValueError:
            st.write("Speech Recognition could not understand audio.")
        except sr.RequestError:
            st.write("Could not request results from Speech Recognition service.")

    if input_topic:
        # Correct the input sentence for spelling mistakes
        corrected_topic = correct_spelling(input_topic)

        # Chat with GPT and get the answer
        answer = chat_with_gpt(corrected_topic)

        # Save chat history
        previous_chats.append((corrected_topic, answer))

        # Display previous chats in sidebar
        chat_history.markdown("\n\n".join([f"**You:** {chat[0]}\n\n**Bot:** {chat[1]}" for chat in previous_chats]))

        # Display the answer
        st.subheader("Answer:")
        st.write(answer)

if __name__ == "__main__":
    main()