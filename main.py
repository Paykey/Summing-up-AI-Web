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