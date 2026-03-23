import os
import httpx
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# from openai import OpenAI

load_dotenv() # .env 파일에 있는 환경변수 불러오기

# 프로젝트 루트 경로 기준으로 static/templates 파일을 안전하게 참조
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
# 정적 파일(CSS/JS) 서빙 경로
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# OpenAI API 사용 시 아래 두 줄 주석 해제
# from openai import OpenAI
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

LOCAL_LLM_ENDPOINT = os.getenv("LOCAL_LLM_ENDPOINT", "http://localhost:11434/api/generate")
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "qwen2.5:14b")

@app.get("/")
def root():
    # 첫 화면으로 HTML 템플릿 반환
    return FileResponse(BASE_DIR / "templates" / "index.html")

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
# 프론트엔드에서 긴 텍스트를 보내면 로컬 LLM으로 요약 결과 반환
@app.post("/summarize")
async def summarize_text(request: SummaryRequest):
    # 모델에 전달할 역할/출력 형식 지시문 + 사용자 원문 결합
    prompt = (
        "너는 자료를 핵심만 3줄로 요약해 주는 역할이야. "
        "반드시 한국어로 대답하고, 각 줄은 간결하게 작성해.\n\n"
        f"[강의자료]\n{request.text}"
    )

    # 로컬 LLM(Ollama) 호출
    try:
        # Ollama generate API 형식으로 요청
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                LOCAL_LLM_ENDPOINT,
                json={
                    "model": LOCAL_LLM_MODEL,
                    "prompt": prompt,
                    "stream": False,
                },
            )
        response.raise_for_status()
        data = response.json()
        # Ollama 응답의 실제 생성 텍스트는 response 키에 담김
        summary = data.get("response", "요약 결과가 비어 있습니다.")
        return {"summary": summary}
    except Exception as exc:
        # 프론트에서 바로 처리할 수 있도록 HTTP 에러로 변환
        raise HTTPException(status_code=500, detail=f"로컬 LLM 호출 실패: {exc}")

    # OpenAI API로 다시 전환할 때 아래 블록 사용
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": "너는 대학생의 전공 강의자료를 핵심만 3줄로 요약해 주는 역할이야. 반드시 한국어로 대답해.",
    #         },
    #         {"role": "user", "content": request.text},
    #     ],
    # )
    # return {"summary": response.choices[0].message.content}