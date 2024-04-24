import streamlit as st
#from llama_index.llms.ollama import Ollama
import ollama

#ollama = Ollama()

def generate_response():
    response=ollama.chat(model="llama3", request_timeout=300.0 , stream=True, message=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token


st.title("Teste ChatBot COREGPT")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content" : "Como posso lhe ajudar nobre Padawan ?"}]

# Write message history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"] ).write(msg["content"])
    else:
        st.chat_message(msg["role"] ).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role" : "user", "content" : prompt})
    st.chat_message("user").write(prompt)
    st.session_state["full_message"] = ""
    st.chat_message("assistant").write_stream(generate_response)
    st.session_state["full_message"] = ""
    st.session_state.messages.append({"role" : "assistant", "content" : st.session_state["full_message"]})
