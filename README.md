# 유튜브 쇼츠 자동 생성 파이프라인

매일 자동으로: **AI 대본 생성 → 무료 TTS 나레이션 → 무료 스톡 배경영상 → 자막 합성 → 유튜브 업로드**
까지 사람 개입 없이 실행되는 파이프라인입니다.

## ⚠️ 시작하기 전에 꼭 읽어주세요

YouTube는 2025~2026년 정책 강화로 **"완전히 똑같은 틀로 대량 생산된 AI 영상"을 적극적으로
수익화 박탈/채널 정지**시키고 있습니다. 이 파이프라인은 매일 다른 주제 + AI의 짧은 통찰 코멘트를
넣어 리스크를 낮췄지만, 100% 안전한 것은 아닙니다.

**강력 권장사항**:
- `.env`의 `YOUTUBE_PRIVACY_STATUS`를 처음엔 반드시 `private`로 두세요 (기본값)
- 최소 1~2주간은 결과물을 직접 확인하고 품질/정책 리스크를 점검한 뒤 `public`으로 전환하세요
- 완전 무인 운영을 하더라도, 일주일에 한 번은 채널 상태를 확인하는 것을 권장합니다

## 1. 필요한 것 준비하기

### (1) Anthropic API 키 (대본 생성)
1. https://console.anthropic.com 가입
2. API Keys 메뉴에서 새 키 발급
3. 결제 정보 등록 (영상당 대본 생성 비용은 몇 원 수준으로 매우 저렴합니다)

### (2) Pexels API 키 (무료 스톡 영상)
1. https://www.pexels.com/api/ 접속 → 무료 가입
2. API 키 즉시 발급 (완전 무료, 시간당 200회 요청 한도)

### (3) YouTube 업로드 권한 (Google Cloud)
1. https://console.cloud.google.com 에서 새 프로젝트 생성
2. "API 및 서비스" → "라이브러리"에서 **YouTube Data API v3** 검색 후 사용 설정
3. "API 및 서비스" → "사용자 인증 정보" → "사용자 인증 정보 만들기" → **OAuth 클라이언트 ID**
   - 애플리케이션 유형: **데스크톱 앱**
4. 다운로드한 JSON 파일을 `client_secret.json` 이름으로 이 폴더에 저장
5. "OAuth 동의 화면"에서 본인 구글 계정을 **테스트 사용자**로 추가

## 2. 로컬에서 최초 1회 실행 (필수)

유튜브 인증은 브라우저 로그인이 필요해서 **최초 1회는 반드시 내 컴퓨터에서** 실행해야 합니다.

```bash
# 1) 이 폴더로 이동 후 패키지 설치
pip install -r requirements.txt

# 2) ffmpeg 설치 (없다면)
# Mac: brew install ffmpeg
# Windows: choco install ffmpeg (또는 공식 사이트에서 다운로드)

# 3) .env 파일 만들기
cp .env.example .env
# .env 파일을 열어서 ANTHROPIC_API_KEY, PEXELS_API_KEY 채워넣기

# 4) 실행 (처음 실행 시 브라우저 창이 뜨며 구글 로그인 요청)
python main.py
```

정상적으로 실행되면 `output/` 폴더에 mp4가 생기고, 유튜브 스튜디오에 **비공개**로 업로드됩니다.
동시에 `token.json`이 생성되는데, 이게 있으면 이후엔 로그인 없이 자동 실행이 가능합니다.

## 3. 완전 자동화 (매일 예약 실행) — GitHub Actions

1. 이 폴더를 GitHub 저장소로 올리기 (`.env`, `client_secret.json`, `token.json`은 `.gitignore`로 자동 제외됨)
2. 저장소 → Settings → Secrets and variables → Actions → **New repository secret**으로 아래 등록:

| Secret 이름 | 값 |
|---|---|
| `ANTHROPIC_API_KEY` | .env와 동일 |
| `PEXELS_API_KEY` | .env와 동일 |
| `YOUTUBE_PRIVACY_STATUS` | `private` (권장, 검증 후 `public`으로 변경) |
| `YOUTUBE_CLIENT_SECRET_B64` | `base64 -i client_secret.json` 실행 결과 값 |
| `YOUTUBE_TOKEN_B64` | `base64 -i token.json` 실행 결과 값 (로컬 최초 실행 후 생성된 파일) |

3. 저장소의 **Actions** 탭 → `Daily Shorts Auto Upload` 워크플로우가 매일 자동 실행됩니다
   (수동 테스트는 "Run workflow" 버튼으로 즉시 실행 가능)

## 4. 예상 비용 (월 5만원 예산 기준)

| 항목 | 비용 |
|---|---|
| 대본 생성 (Claude API) | 영상당 약 5~15원 → 30개/월 ≈ 300원 |
| TTS (edge-tts) | 무료 |
| 배경영상 (Pexels) | 무료 |
| GitHub Actions | 무료 (월 2,000분, 영상당 약 3~5분 소요 → 30개면 충분) |
| YouTube 업로드 | 무료 |
| **합계** | **월 1,000원 미만** — 예산에 여유가 많이 남습니다 |

남는 예산은 필요 시 더 좋은 TTS(ElevenLabs 등)나 프리미엄 스톡 영상(Envato)으로 업그레이드하는 데 쓰시면 됩니다.

## 5. 문제 해결

- **`ffmpeg: command not found`** → ffmpeg 미설치. 위 설치 명령 참고
- **배경 영상을 못 찾음** → `script_generator.py`가 생성한 `search_keywords`가 너무 특이한 경우. 재실행하면 다른 주제로 재시도됨
- **유튜브 업로드 시 quota 초과 오류** → 일일 업로드는 6~10개 정도가 안전선입니다 (Data API 기본 쿼터 10,000 units/day, 업로드 1회당 1,600 units)
- **자막이 화면 밖으로 나감** → `video_assembler.py`의 `fontsize`, `y=h-h/3.2` 값을 조정하세요

## 6. 파일 구조

```
shorts_automation/
├── config.py              # 공통 설정
├── script_generator.py    # 1단계: AI 대본 생성
├── tts_generator.py       # 2단계: 무료 TTS 음성
├── footage_fetcher.py     # 3단계: 무료 배경영상
├── video_assembler.py     # 4단계: ffmpeg 합성
├── youtube_uploader.py    # 5단계: 유튜브 업로드
├── main.py                # 전체 파이프라인 실행
├── requirements.txt
├── .env.example
└── .github/workflows/daily_upload.yml   # 매일 자동 실행 스케줄러
```
