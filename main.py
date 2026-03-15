import asyncio
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

app = FastAPI()

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
    
# 가짜 ai 
@app.post("/analyze")
async def analyze_data(file: UploadFile = File(...)):
    # 1. 파일 이름 출력 (터미널 확인용)
    print(f"업로드된 파일: {file.filename}")
    
    # 2. AI가 열심히 분석하는 척 3초 기다리기
    await asyncio.sleep(3)
    
    # 3. 가짜 AI 분석 결과 반환
    return {
        "status": "success",
        "message": "AI 분석이 완료되었습니다.",
        "filename": file.filename,
        "ai_result": "정상 판정 (확률: 98%)" # 나중에 진짜 AI 결과가 들어갈 자리
    }