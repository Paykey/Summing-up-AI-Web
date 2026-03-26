# 파이썬 3.10 기반의 경량(slim) 이미지 사용
FROM python:3.10-slim

# 컨테이너 작업 디렉터리 설정
WORKDIR /app

# 의존성 파일을 먼저 복사해 레이어 캐시 효율 개선
COPY requirements.txt .
# 필요 패키지 설치 (캐시 비활성화로 이미지 용량 절감)
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 전체 복사
COPY . .

# 컨테이너 시작 시 Uvicorn 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]