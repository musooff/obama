from moviepy.editor import VideoFileClip


def cut_part(start, end, name, output):
	shape = VideoFileClip(name)
	print shape.duration
	final = shape.subclip(start, end)
	final.write_videofile(output)
cut_part(0,0.3, "although my heart is falling too/althoughSentenceFolder/And although the Recovery Act represents just a small fraction .mp4", "although my heart is falling too/althoughOnlyFolder/0.mp4")