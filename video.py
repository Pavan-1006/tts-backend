from moviepy.editor import AudioFileClip, ImageClip

def mp3_to_mp4(mp3_path, mp4_path, image_path):
    audio = AudioFileClip(mp3_path)

    image = (
        ImageClip(image_path)
        .set_duration(audio.duration)
        .set_audio(audio)
    )

    image.write_videofile(
        mp4_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )
