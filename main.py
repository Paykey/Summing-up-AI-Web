import os
import asyncio
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() # .env 파일에 있는 환경변수 불러오기

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def root():
    return {"message": "main page"}

@app.get("/sub1")
def sub1():
    return {"message": "sub page 1"}

@app.get("/sub2")
def sub2():    
    return {"message": "sub page 2"}

class UserInfo(BaseModel):
    name: str           # 이름
    age: int            # 나이
    symptoms: list[str] # 증상 리스트
    
@app.post("/send_info")
def recieve_info(user: UserInfo):
    print(f"Received info for {user.name}, age {user.age}, symptoms: {', '.join(user.symptoms)}")
    return {"status":"성공", "message": f"{user.name}님의 정보가 성공적으로 수신되었습니다."}

@app.post("/upload_photo")
def recieve_photo(photo: UploadFile = File(...)):
    # 백엔드 로그 출력
    print(f"Received photo: {photo.filename}, content type: {photo.content_type}")
    
    # 프론트엔딩 확인
    return {
        "status": "성공",
        "message": f"'{photo.filename}' 사진이 성공적으로 업로드되었습니다."
    }
    

# 프론트엔드(사용자)가 보낼 데이터 형식
class SummaryRequest(BaseModel):
    text: str

# 요약 요청을 처리하는 API 엔드포인트
# 프론트엔드에서 긴 텍스트를 보내면, OpenAI API를 호출하여 요약된 결과 반환
@app.post("/summarize")
async def summarize_text(request: SummaryRequest):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            # system: AI의 역할(페르소나)을 부여
            {"role": "system", "content": "너는 대학생의 전공 강의자료를 핵심만 3줄로 요약해 주는 역할이야. 반드시 한국어로 대답해."},
            # user: 사용자가 실제로 보낸 긴 텍스트
            {"role": "user", "content": request.text}
        ]
    )
    
    # AI의 응답에서 요약된 텍스트를 추출하여 프론트엔드에 반환
    # response.choices[0].message.content -> AI가 생성한 요약 텍스트
    return {"summary": response.choices[0].message.content}