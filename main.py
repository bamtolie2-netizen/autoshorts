"""
전체 파이프라인 실행:
대본 생성 -> 음성 생성 -> 배경영상 다운로드 -> 영상 합성 -> 유튜브 업로드

실행: python main.py
"""
import os
import sys
import traceback
from datetime import datetime

import config
import script_generator
import tts_generator
import footage_fetcher
import video_assembler
import youtube_uploader


def run_once():
    print("=== 1. 대본 생성 중 ===")
    script = script_generator.generate_script()
    print(f"주제: {script['topic']}")
    print(f"제목: {script['title']}")

    print("=== 2. 나레이션 음성 생성 중 ===")
    audio_path = os.path.join(config.OUTPUT_DIR, "narration.mp3")
    tts_generator.generate_narration(script["narration"], audio_path)
    duration = tts_generator.get_audio_duration(audio_path)
    print(f"음성 길이: {duration:.1f}초")

    print("=== 3. 배경 영상 다운로드 중 ===")
    clips = footage_fetcher.download_clips(
        script["search_keywords"], min_total_seconds=duration + 5
    )
    print(f"다운로드된 클립: {len(clips)}개")

    print("=== 4. 영상 합성 중 (시간이 좀 걸립니다) ===")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_path = os.path.join(config.OUTPUT_DIR, f"short_{timestamp}.mp4")
    video_assembler.assemble(clips, audio_path, script["sentences"], duration, final_path)
    print(f"완성된 영상: {final_path}")

    print("=== 5. 유튜브 업로드 중 ===")
    video_id = youtube_uploader.upload_short(
        final_path, script["title"], script["description"], script["tags"]
    )
    print(f"완료! privacyStatus={config.YOUTUBE_PRIVACY_STATUS}, video_id={video_id}")

    # 다운로드한 배경 클립 정리 (용량 관리)
    for c in clips:
        try:
            os.remove(c)
        except OSError:
            pass


if __name__ == "__main__":
    try:
        run_once()
    except Exception:
        print("파이프라인 실행 중 오류 발생:", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
