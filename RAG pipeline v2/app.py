# import os
# from fastapi import FastAPI, Request, Form
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates

# import markdown
# from main import ChromaQueryHandler

# from pymongo import MongoClient
# from uuid import uuid4
# from datetime import datetime
# import csv
# from io import StringIO
# from fastapi.responses import StreamingResponse
# from bs4 import BeautifulSoup

# client = MongoClient("mongodb://localhost:27017/")
# db = client["agrichat"]
# sessions_collection = db["sessions"]

# app = FastAPI()

# static_dir = os.path.join(os.path.dirname(__file__), "static")
# app.mount("/static", StaticFiles(directory=static_dir), name="static")
# templates = Jinja2Templates(directory="templates")

# query_handler = ChromaQueryHandler(
#     chroma_path=r"./chroma_db",
#     # chroma_path=r"/Users/madhurthareja/itachicmd/agrichat-annam/RAG pipeline v2/chroma_db",
#     # model_name="gemma3:1b",
#     model_name="gemma:2b",
#     base_url="http://localhost:11434/v1",
# )

# def get_session(request: Request):
#     session_id = request.cookies.get("session_id")
#     if session_id:
#         return sessions_collection.find_one({"session_id": session_id}), session_id
#     return None, None

# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     response = templates.TemplateResponse("index.html", {
#         "request": request,
#         "session": None,
#         "messages": [],
#         "recent_sessions": list(
#             sessions_collection.find({"status":"active"}, {"session_id": 1, "timestamp": 1, "crop": 1, "state": 1, "status":1, "has_unread": 1})
#             .sort("timestamp", -1).limit(10)
#         )
#     })
#     response.delete_cookie("session_id")
#     return response

# @app.post("/query", response_class=HTMLResponse)
# async def query(request: Request, question: str = Form(...)):
#     session_id = str(uuid4())
#     raw_answer = query_handler.get_answer(question)
#     answer_only = raw_answer.split("</think>")[-1].strip() if "</think>" in raw_answer else raw_answer.strip()
#     html_answer = markdown.markdown(answer_only, extensions=["extra", "nl2br"])

#     session_data = {
#         "session_id": session_id,
#         "timestamp": datetime.now(),
#         "messages": [{"question": question, "answer": html_answer}],
#         "crop": "unknown",
#         "state": "unknown",
#         "status": "active",
#         "has_unread": True
#     }
#     sessions_collection.insert_one(session_data)

#     response = RedirectResponse(url=f"/resume/{session_id}", status_code=303)
#     response.set_cookie(key="session_id", value=session_id)
#     return response

# @app.get("/resume/{session_id}",response_class=HTMLResponse)
# async def resume_session(session_id: str, request: Request):
#     session = sessions_collection.find_one({"session_id": session_id}) 
#     if (not session) or session.get("status")=="archived":
#         return RedirectResponse("/")

#     sessions_collection.update_one(
#         {"session_id": session_id},
#         {"$set": {"has_unread": False}}
#     )
#     messages = session.get("messages", [])
#     response = templates.TemplateResponse("index.html", {
#         "request": request,
#         "session": session,
#         "messages": messages,
#         "recent_sessions": list(
#             sessions_collection.find({"status":"active"}, {"session_id": 1, "timestamp": 1, "crop": 1, "state": 1, "status": 1, "has_unread": 1})
#             .sort("timestamp", -1).limit(10)
#         )
#     })
#     response.set_cookie(key="session_id", value=session_id)
#     return response

# @app.post("/resume/{session_id}/query", response_class=HTMLResponse)
# async def continue_session(session_id: str, request: Request, question: str = Form(...)):
#     session = sessions_collection.find_one({"session_id": session_id})
#     if not session:
#         return RedirectResponse("/")

#     raw_answer = query_handler.get_answer(question)
#     answer_only = raw_answer.split("</think>")[-1].strip() if "</think>" in raw_answer else raw_answer.strip()
#     html_answer = markdown.markdown(answer_only, extensions=["extra", "nl2br"])

#     sessions_collection.update_one(
#         {"session_id": session_id},
#         {"$push": {"messages": {"question": question, "answer": html_answer}},"$set": {"has_unread": True}}
#     )

#     return RedirectResponse(url=f"/resume/{session_id}", status_code=303)

# @app.post("/new-session", response_class=HTMLResponse)
# async def new_session(request: Request):
#     response = RedirectResponse("/", status_code=302)
#     response.delete_cookie("session_id")
#     return response

# @app.get("/export/csv/{session_id}")
# async def export_csv(session_id: str):
#     session = sessions_collection.find_one({"session_id": session_id})
#     if not session:
#         return {"error": "Session not found"}
    
#     output=StringIO()
#     writer = csv.writer(output)
#     writer.writerow(["Question","Answer"])
    
#     for msg in session.get("messages",[]):
#         question = msg["question"]
#         soup = BeautifulSoup(msg["answer"], "html.parser")
#         plain_answer = soup.get_text()
#         writer.writerow([question, plain_answer])
        
#     output.seek(0)
#     return StreamingResponse(output, media_type="text/csv", headers={
#         "Content-Disposition": f"attachment; filename=agrichat_session_{session_id}.csv"
#     })
    
# @app.post("/toggle-status/{session_id}/{status}",response_class=HTMLResponse)
# async def toggle_status(request: Request,session_id: str,status: str):
#     new_status=""
#     if status=="active":
#         new_status="archived"
#     else:
#         new_status="active"
#     sessions_collection.update_one({"session_id":session_id},{"$set":{"status":new_status}}) 
#     referer = request.headers.get("referer")
#     return RedirectResponse(url=referer,status_code=303)

# # @app.get("/get-archives",response_class=HTMLResponse)
# # async def get_archived_session(request=Request):
    
    
    
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import markdown
from main import ChromaQueryHandler

from pymongo import MongoClient
from uuid import uuid4
from datetime import datetime
import csv
from io import StringIO
from fastapi.responses import StreamingResponse
from bs4 import BeautifulSoup

client = MongoClient("mongodb://localhost:27017/")
db = client["agrichat"]
sessions_collection = db["sessions"]

app = FastAPI()

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory="templates")

query_handler = ChromaQueryHandler(
    chroma_path=r"./chroma_db",
    # chroma_path=r"/Users/madhurthareja/itachicmd/agrichat-annam/RAG pipeline v2/chroma_db",
    # model_name="gemma3:1b",
    model_name="gemma:2b",
    base_url="http://localhost:11434/v1",
)

def get_session(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        return sessions_collection.find_one({"session_id": session_id}), session_id
    return None, None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Get all recent sessions (both active and archived) for the sidebar
    all_sessions = list(
        sessions_collection.find(
            {}, 
            {"session_id": 1, "timestamp": 1, "crop": 1, "state": 1, "status": 1, "has_unread": 1, "messages": {"$slice": 1}}
        ).sort("timestamp", -1).limit(20)
    )
    
    response = templates.TemplateResponse("index.html", {
        "request": request,
        "session": None,
        "messages": [],
        "recent_sessions": all_sessions
    })
    response.delete_cookie("session_id")
    return response

@app.post("/query", response_class=HTMLResponse)
async def query(request: Request, question: str = Form(...)):
    session_id = str(uuid4())
    raw_answer = query_handler.get_answer(question)
    answer_only = raw_answer.split("</think>")[-1].strip() if "</think>" in raw_answer else raw_answer.strip()
    html_answer = markdown.markdown(answer_only, extensions=["extra", "nl2br"])

    # Try to extract crop and state information from the question or answer
    crop = extract_crop_info(question, answer_only)
    state = extract_state_info(question, answer_only)

    session_data = {
        "session_id": session_id,
        "timestamp": datetime.now(),
        "messages": [{"question": question, "answer": html_answer}],
        "crop": crop,
        "state": state,
        "status": "active",
        "has_unread": True
    }
    sessions_collection.insert_one(session_data)

    response = RedirectResponse(url=f"/resume/{session_id}", status_code=303)
    response.set_cookie(key="session_id", value=session_id)
    return response

@app.get("/resume/{session_id}", response_class=HTMLResponse)
async def resume_session(session_id: str, request: Request):
    session = sessions_collection.find_one({"session_id": session_id}) 
    if not session:
        return RedirectResponse("/")

    # Get all recent sessions for the sidebar
    all_sessions = list(
        sessions_collection.find(
            {}, 
            {"session_id": 1, "timestamp": 1, "crop": 1, "state": 1, "status": 1, "has_unread": 1, "messages": {"$slice": 1}}
        ).sort("timestamp", -1).limit(20)
    )

    # Mark session as read if it's active
    if session.get("status") == "active":
        sessions_collection.update_one(
            {"session_id": session_id},
            {"$set": {"has_unread": False}}
        )

    messages = session.get("messages", [])
    response = templates.TemplateResponse("index.html", {
        "request": request,
        "session": session,
        "messages": messages,
        "recent_sessions": all_sessions
    })
    response.set_cookie(key="session_id", value=session_id)
    return response

@app.post("/resume/{session_id}/query", response_class=HTMLResponse)
async def continue_session(session_id: str, request: Request, question: str = Form(...)):
    session = sessions_collection.find_one({"session_id": session_id})
    if not session:
        return RedirectResponse("/")
    
    # Check if session is archived - prevent querying archived sessions
    if session.get("status") == "archived":
        return RedirectResponse(f"/resume/{session_id}", status_code=303)

    raw_answer = query_handler.get_answer(question)
    answer_only = raw_answer.split("</think>")[-1].strip() if "</think>" in raw_answer else raw_answer.strip()
    html_answer = markdown.markdown(answer_only, extensions=["extra", "nl2br"])

    # Update crop and state if we can extract better info
    crop = extract_crop_info(question, answer_only) or session.get("crop", "unknown")
    state = extract_state_info(question, answer_only) or session.get("state", "unknown")

    sessions_collection.update_one(
        {"session_id": session_id},
        {
            "$push": {"messages": {"question": question, "answer": html_answer}},
            "$set": {
                "has_unread": True,
                "crop": crop,
                "state": state,
                "timestamp": datetime.now()  # Update timestamp to move to top
            }
        }
    )

    return RedirectResponse(url=f"/resume/{session_id}", status_code=303)

@app.post("/new-session", response_class=HTMLResponse)
async def new_session(request: Request):
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("session_id")
    return response

@app.get("/export/csv/{session_id}")
async def export_csv(session_id: str):
    session = sessions_collection.find_one({"session_id": session_id})
    if not session:
        return {"error": "Session not found"}
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Question", "Answer", "Timestamp"])
    
    for i, msg in enumerate(session.get("messages", [])):
        question = msg["question"]
        soup = BeautifulSoup(msg["answer"], "html.parser")
        plain_answer = soup.get_text()
        timestamp = session["timestamp"].strftime("%Y-%m-%d %H:%M:%S") if i == 0 else ""
        writer.writerow([question, plain_answer, timestamp])
        
    output.seek(0)
    filename = f"agrichat_session_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]), 
        media_type="text/csv", 
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
    
@app.post("/toggle-status/{session_id}/{status}", response_class=HTMLResponse)
async def toggle_status(request: Request, session_id: str, status: str):
    new_status = "archived" if status == "active" else "active"
    
    sessions_collection.update_one(
        {"session_id": session_id},
        {"$set": {"status": new_status}}
    ) 
    
    # If archiving the current session, redirect to home
    current_session_id = request.cookies.get("session_id")
    if status == "active" and current_session_id == session_id:
        response = RedirectResponse(url="/", status_code=303)
        response.delete_cookie("session_id")
        return response
    
    # Otherwise redirect back to the current page
    referer = request.headers.get("referer", "/")
    return RedirectResponse(url=referer, status_code=303)

def extract_crop_info(question: str, answer: str) -> str:
    """Extract crop information from question or answer"""
    crops = [
        "wheat", "rice", "corn", "maize", "barley", "oats", "sorghum", "millet",
        "cotton", "sugarcane", "soybean", "groundnut", "peanut", "sunflower",
        "mustard", "sesame", "potato", "onion", "tomato", "cabbage", "cauliflower",
        "carrot", "beetroot", "radish", "spinach", "lettuce", "brinjal", "eggplant",
        "okra", "peas", "beans", "chickpea", "lentil", "pigeon pea", "black gram",
        "green gram", "apple", "banana", "mango", "orange", "grapes", "pomegranate",
        "papaya", "guava", "watermelon", "melon", "cucumber", "pumpkin", "gourd"
    ]
    
    text = (question + " " + answer).lower()
    for crop in crops:
        if crop in text:
            return crop.title()
    return "General"

def extract_state_info(question: str, answer: str) -> str:
    """Extract state/region information from question or answer"""
    states = [
        "punjab", "haryana", "uttar pradesh", "up", "bihar", "west bengal",
        "maharashtra", "gujarat", "rajasthan", "madhya pradesh", "mp",
        "karnataka", "andhra pradesh", "ap", "telangana", "tamil nadu",
        "kerala", "odisha", "orissa", "jharkhand", "chhattisgarh",
        "assam", "himachal pradesh", "hp", "uttarakhand", "jammu and kashmir",
        "jk", "goa", "manipur", "meghalaya", "mizoram", "nagaland",
        "sikkim", "tripura", "arunachal pradesh"
    ]
    
    text = (question + " " + answer).lower()
    for state in states:
        if state in text:
            return state.title()
    return "General"

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}