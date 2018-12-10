import os

v_old_dir = "video_files"
v_new_dir = "wh_obama"

def check_dif():
	old_list = os.listdir(v_old_dir)
	new_list = os.listdir(v_new_dir)

	l_common_videos = []
	l_common_subs = []

	l_not_in_old_vidoes = []
	l_not_in_old_subs = []
	l_not_in_new_videos = []
	l_not_in_new_subs = []


	sor_old = sorted(old_list)
	sor_new = sorted(new_list)


	count = 0
	for i, el in enumerate(sor_new):	
		if count %2 == 0:
			if el in sor_old:
				l_common_subs.append(el)
			else:
				l_not_in_old_subs.append(el)
		else:
			if el in sor_old:
				l_common_videos.append(el)
			else:
				l_not_in_old_vidoes.append(el)
		count += 1
	print "Not in old subs"
	for f in l_not_in_old_subs:
		print f
	print "Not in old videos"
	for f in l_not_in_old_vidoes:
		print f
	print "not in subs", len(l_not_in_old_subs)
	print "not in videos", len(l_not_in_old_vidoes)
	print "common subs", len(l_common_subs)
	print "common videos", len(l_common_videos)
#check_dif()

def check_dif2():
	old_list = os.listdir(v_old_dir)
	new_list = os.listdir(v_new_dir)

	l_common_videos = []
	l_common_subs = []

	l_not_in_old_vidoes = []
	l_not_in_old_subs = []
	l_not_in_new_videos = []
	l_not_in_new_subs = []


	sor_old = sorted(old_list)
	sor_new = sorted(new_list)


	count = 0
	for i, el in enumerate(sor_old):	
		if count %2 == 0:
			if not el.replace(".en.vtt", ".mp4") == sor_old[count + 1]:
				print count, el
		count += 1
	print "Not in old subs"
	for f in l_not_in_old_subs:
		print f
	print "Not in old videos"
	for f in l_not_in_old_vidoes:
		print f
	print "not in subs", len(l_not_in_old_subs)
	print "not in videos", len(l_not_in_old_vidoes)
	print "common subs", len(l_common_subs)
	print "common videos", len(l_common_videos)
check_dif2()