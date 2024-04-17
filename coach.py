import streamlit as st
import anthropic

def main():
    st.title("Engineering Coach")

    # Create the Anthropic client
    client = anthropic.Anthropic(api_key='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')

    f = open("prompt.txt", "r")
    initPrompt = f.read()
    airesponse = "" 

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "user", "content": initPrompt})
        response = AI(st, client)
        st.session_state.messages.append({"role": "assistant", "content": "Let's get started."})


    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            airesponse = AI(st, client)
            
       
        st.session_state.messages.append({"role": "assistant", "content": airesponse})
            


def AI(st, client):
    
            stream = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4096,
                temperature=0,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            response = ''.join(block.text for block in stream.content)  # Adjusted line to concatenate the text
            st.write(response)
            return response
            


if __name__ == "__main__":
    main()