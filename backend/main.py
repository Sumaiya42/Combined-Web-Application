import os
import csv # Logging এর জন্য
import requests # n8n Webhook কল করার জন্য
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)

class LeadRequest(BaseModel):
    message: str

# n8n Webhook URL (আপনার n8n থেকে পাওয়া URL এখানে দিন)
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/task5-lead" 

@app.post("/process-lead")
async def process(request: LeadRequest):
    # ১. AI Classification
    score_result = classifier(request.message)[0]
    status = "Hot Lead" if score_result['label'] == 'POSITIVE' else "Cold Lead"

    # ২. AI Response Generation
    prompt = ChatPromptTemplate.from_template("You are a professional sales assistant. Reply to: {msg}")
    chain = prompt | llm
    ai_text = chain.invoke({"msg": request.message})

    # ৩. Logging (CSV ফাইলে সেভ করা)
    log_data = [datetime.now(), request.message, status, round(score_result['score'], 2)]
    with open('lead_logs.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(log_data)

    # ৪. Workflow Automation via n8n (শুধুমাত্র Hot Lead হলে টেলিগ্রাম/ইমেইল পাঠাবে)
    if status == "Hot Lead":
        try:
            requests.post(N8N_WEBHOOK_URL, json={
                "message": request.message,
                "status": status,
                "ai_suggestion": ai_text.content
            })
        except:
            print("n8n connection failed, but app is running.")

    return {
        "status": status,
        "ai_response": ai_text.content,
        "score": round(score_result['score'], 2)
    }