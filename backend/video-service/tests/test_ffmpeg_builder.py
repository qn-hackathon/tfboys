from app.utils.ffmpeg_builder import FFmpegCommandBuilder


def test_build_scene_video_command():
    command = FFmpegCommandBuilder.build_scene_video_command(
        image_path="/tmp/image.jpg",
        audio_path="/tmp/audio.mp3",
        subtitle_filter="drawtext=text='test'",
        output_path="/tmp/output.mp4",
        duration=5.0
    )
    
    assert "ffmpeg" in command
    assert "/tmp/image.jpg" in command
    assert "/tmp/audio.mp3" in command
    assert "/tmp/output.mp4" in command


def test_build_concat_command():
    command = FFmpegCommandBuilder.build_concat_command(
        scene_videos=["/tmp/scene1.mp4", "/tmp/scene2.mp4"],
        output_path="/tmp/final.mp4",
        concat_file="/tmp/concat.txt"
    )
    
    assert "ffmpeg" in command
    assert "/tmp/concat.txt" in command
    assert "/tmp/final.mp4" in command
