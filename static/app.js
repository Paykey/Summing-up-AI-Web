// 요약 실행 버튼 요소
const summarizeBtn = document.getElementById("summarizeBtn");
// 사용자가 업로드할 파일 input 요소
const lectureFile = document.getElementById("lectureFile");
// 요약 결과를 표시할 pre 요소
const summaryResult = document.getElementById("summaryResult");

// 파일 업로드 및 서버 요약 요청을 처리하는 메인 함수
async function summarizeLecture() {
  // 선택된 첫 번째 파일만 대상으로 처리
  const selectedFile = lectureFile.files?.[0];

  // 파일이 없으면 요청을 보내지 않고 안내 문구 출력
  if (!selectedFile) {
    statusText.textContent = "요약할 파일을 먼저 선택해 주세요.";
    return;
  }

  // 중복 클릭 방지를 위해 요청 중에는 버튼 비활성화
  summarizeBtn.disabled = true;
  // 진행 상태를 사용자에게 즉시 안내
  statusText.textContent = "요약 중입니다...";
  summaryResult.textContent = "요약 생성 중...";

  try {
    // multipart/form-data 전송을 위해 FormData 사용
    const formData = new FormData();
    // 백엔드에서 기대하는 키 이름("file")으로 파일 첨부
    formData.append("file", selectedFile);

    // 백엔드 요약 API 호출
    const response = await fetch("/summarize", {
      method: "POST",
      body: formData,
    });

    // 성공/실패 여부와 관계없이 JSON 본문 파싱
    const data = await response.json();

    // 서버 에러 메시지가 있으면 그대로 사용자에게 노출
    if (!response.ok) {
      throw new Error(data.detail || "요약에 실패했습니다.");
    }

    // 정상 응답 시 요약 결과를 화면에 반영
    summaryResult.textContent = data.summary || "요약 결과가 비어 있습니다.";
    statusText.textContent = "완료";
  } catch (error) {
    // 네트워크/서버 오류 처리
    summaryResult.textContent =
      "오류가 발생했습니다. 서버 로그를 확인해 주세요.";
    // 사용자에게 오류 메시지 전달
    statusText.textContent = error.message;
  } finally {
    // 요청 종료 후 버튼 다시 활성화
    summarizeBtn.disabled = false;
  }
}

// 버튼 클릭 시 요약 실행
summarizeBtn.addEventListener("click", summarizeLecture);
