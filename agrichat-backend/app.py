from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pymongo import MongoClient
from uuid import uuid4
from datetime import datetime
from bs4 import BeautifulSoup
#from {// main.py path} import ChromaQueryHandler
from RAGpipelinev3.main import ChromaQueryHandler
import markdown
import csv
from starlette.middleware.base import BaseHTTPMiddleware
from io import StringIO
import os

app = FastAPI()

class CustomCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            response = JSONResponse(content={"message": "Preflight OK"})
        else:
            response = await call_next(request)

        origin = request.headers.get("origin")
        if origin == "https://agrichat-annam.vercel.app":
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"

        return response

app.add_middleware(CustomCORSMiddleware)

@app.options("/{rest_of_path:path}")
async def preflight_handler():
    return JSONResponse(
        content={"message": "CORS preflight"},
        headers={
            "Access-Control-Allow-Origin": "https://agrichat-annam.vercel.app",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        },
    )


MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["agrichat"]
sessions_collection = db["sessions"]

query_handler = ChromaQueryHandler(
    chroma_path="./chroma_db",
    model_name="gemma:2b",
    base_url="http://localhost:11434/v1",
)

def clean_session(s):
    s["_id"] = str(s["_id"])
    return s

@app.get("/api/sessions")
async def list_sessions():
    sessions = list(
    sessions_collection.find({}, {"session_id": 1, "timestamp": 1, "crop": 1, "state": 1, "status": 1, "has_unread": 1, "messages": {"$slice": 1}})
    .sort("timestamp", -1)
    .limit(20)
    )
    return {"sessions": [clean_session(s) for s in sessions]}

@app.post("/api/query")
async def new_session(question: str = Form(...)):
    session_id = str(uuid4())
    raw_answer = query_handler.get_answer(question)
    answer_only = raw_answer.split("</think>")[-1].strip() if "</think>" in raw_answer else raw_answer.strip()
    html_answer = markdown.markdown(answer_only, extensions=["extra", "nl2br"])
    crop = "unknown"
    state = "unknown"
    session = {
        "session_id": session_id,
        "timestamp": datetime.now(),
        "messages": [{"question": question, "answer": html_answer}],
        "crop": crop,
        "state": state,
        "status": "active",
        "has_unread": True,
    }
    sessions_collection.insert_one(session)
    session.pop("_id", None)
    return {"session": session}

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    session = sessions_collection.find_one({"session_id": session_id})
    if session:
        session["_id"] = str(session["_id"])
        sessions_collection.update_one({"session_id": session_id},{"$set":{"has_unread":False}})
        session["has_unread"]=False
    return {"session": session}


@app.post("/api/session/{session_id}/query")
async def continue_session(session_id: str, question: str = Form(...)):
    session = sessions_collection.find_one({"session_id": session_id})
    if not session or session.get("status") == "archived":
        return JSONResponse(status_code=403, content={"error": "Session is archived or missing"})

    raw_answer = query_handler.get_answer(question)
    answer_only = raw_answer.split("</think>")[-1].strip()
    html_answer = markdown.markdown(answer_only, extensions=["extra", "nl2br"])

    crop = session.get("crop", "unknown")
    state = session.get("state", "unknown")

    sessions_collection.update_one(
        {"session_id": session_id},
        {
            "$push": {"messages": {"question": question, "answer": html_answer}},
            "$set": {
                "has_unread": True,
                "crop": crop,
                "state": state,
                "timestamp": datetime.now()
            },
        },
    )

    updated = sessions_collection.find_one({"session_id": session_id})
    if updated:
        updated.pop("_id", None)
    return {"session": updated}



@app.post("/api/toggle-status/{session_id}/{status}")
async def toggle_status(session_id: str, status: str):
    new_status = "archived" if status == "active" else "active"
    sessions_collection.update_one(
        {"session_id": session_id},
        {"$set": {"status": new_status}}
    )
    return {"status": new_status}
    
@app.get("/api/export/csv/{session_id}")
async def export_csv(session_id: str):
    session = sessions_collection.find_one({"session_id": session_id})
    if not session:
        return JSONResponse(status_code=404, content={"error": "Session not found"})

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Question", "Answer", "Timestamp"])
    for i, msg in enumerate(session.get("messages", [])):
        q = msg["question"]
        a = BeautifulSoup(msg["answer"], "html.parser").get_text()
        t = session["timestamp"].strftime("%Y-%m-%d %H:%M:%S") if i == 0 else ""
        writer.writerow([q, a, t])

    output.seek(0)
    filename = f"session_{session_id}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
    
@app.delete("/api/delete-session/{session_id}")
async def delete_session(session_id: str):
    result = sessions_collection.delete_one({"session_id":session_id})
    if result.deleted_count == 0:
        return JSONResponse(status_code=404, content={"error":"Session not found"})
    return {"message": "Session deleted successfully"}