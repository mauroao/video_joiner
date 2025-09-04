import argparse
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.fx.all import fadein, fadeout

def main():
    parser = argparse.ArgumentParser(description='Join video files with fade transitions.')
    parser.add_argument('--folder', type=str, required=True, help='Folder containing video files.')
    args = parser.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"Error: Folder not found at '{folder}'")
        return

    video_files = sorted([f for f in os.listdir(folder) if f.endswith(('.mp4', '.avi', '.mov'))])

    if not video_files:
        print(f"No video files found in '{folder}'")
        return

    clips = []
    for video_file in video_files:
        clip = VideoFileClip(os.path.join(folder, video_file))
        clips.append(clip)

    if not clips:
        return

    fade_duration = 1  # seconds

    # Create the transitions
    video_fx = [clips[0]]
    for i in range(len(clips) - 1):
        video_fx.append(clips[i+1].set_start(video_fx[-1].end - fade_duration).crossfadein(fade_duration))

    # Concatenate all clips
    final_clip = CompositeVideoClip(video_fx)

    # Write the result to a file
    output_file = os.path.join(folder, 'output.mp4')
    if os.path.exists(output_file):
        os.remove(output_file)
    final_clip.write_videofile(output_file, codec='libx264', audio=False)

if __name__ == '__main__':
    main()