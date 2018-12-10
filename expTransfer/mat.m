for c = 1:25
	ob_path = strcat('/home/muso/Desktop/obama/karaoke/split_parts/Shape Of You 2/obama/',int2str(c),'.wav');
	[source, sr]= audioread(ob_path);
	ta_path = strcat('/home/muso/Desktop/obama/karaoke/split_parts/Shape Of You/prof/',int2str(c),'.wav');
	target = audioread(ta_path);
	y = expTrans(source, target, sr);
	res_path = strcat('/home/muso/Desktop/obama/karaoke/split_parts/Shape Of You/obama_res_2/',int2str(c),'.wav');
	audiowrite(res_path, y, sr);
end