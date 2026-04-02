import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from transformers import pipeline


load_dotenv()


@st.cache_resource
def load_models():
    classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant", 
        temperature=0
    )
    return classifier, llm

classifier, llm = load_models()


st.set_page_config(page_title="AI Lead Handler", page_icon="🚀")

st.title("🚀 AI Lead Handler")
st.write("Analyze and respond to leads using LangChain & Hugging Face")


user_message = st.text_area("Give lead message here...", placeholder="e.g., I want to buy your product!", height=150)

if st.button("Process Lead"):
    if user_message:
        with st.spinner("Analyzing..."):
            
            score_result = classifier(user_message)[0]
            status = "Hot Lead" if score_result['label'] == 'POSITIVE' else "Cold Lead"
            status_color = "green" if status == "Hot Lead" else "red"

            
            prompt = ChatPromptTemplate.from_template("You are a professional sales lead assistant. Analyze this message and give a short 1-sentence reply to the customer: {msg}")
            chain = prompt | llm
            ai_text = chain.invoke({"msg": user_message})

            
            st.divider()
            st.subheader(f"Lead Category: :{status_color}[{status}]")
            
            st.info(f"**AI Suggested Response:**\n\n{ai_text.content}")
            
            st.caption(f"Confidence Score: {round(score_result['score'], 2)}")
    else:
        st.warning("Please enter a message first!")