"""
전체 파이프라인 공통 설정.
.env 파일(또는 GitHub Actions Secrets)에서 값을 읽어옵니다.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- API 키 ---
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# --- 유튜브 업로드 옵션 ---
# 처음에는 반드시 "private"로 두고, 며칠간 직접 결과물을 확인한 뒤에
# "public"으로 바꾸는 것을 강력히 권장합니다.
# (완전 무인 자동 발행은 YouTube의 대량생산 콘텐츠 정책 위반 리스크가 있습니다)
YOUTUBE_PRIVACY_STATUS = os.getenv("YOUTUBE_PRIVACY_STATUS", "private")

# 실제로 사람이 만든 관점/코멘트가 아니라 AI가 사실+코멘트를 생성했다고
# 명시적으로 공개하고 싶다면 True로 설정 (정책 안전지대를 위해 권장)
DISCLOSE_SYNTHETIC_MEDIA = os.getenv("DISCLOSE_SYNTHETIC_MEDIA", "true").lower() == "true"

# --- 대본/영상 생성 설정 ---
CLAUDE_MODEL = "claude-sonnet-5"
TARGET_VIDEO_SECONDS = 40          # 쇼츠 길이 (30~50초 권장)
TTS_VOICE = "en-US-AriaNeural"     # 미국 영어 여성 음성 (edge-tts 무료)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920

# --- 경로 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
USED_TOPICS_PATH = os.path.join(BASE_DIR, "used_topics.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")
CLIENT_SECRET_PATH = os.path.join(BASE_DIR, "client_secret.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
