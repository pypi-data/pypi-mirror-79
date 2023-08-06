import qrcode
def qrcoder(value,imgname):
	if '.' not in imgname:
		imgname = imgname+".jpg"
	else:
		imgname = imgname
	img = qrcode.make(value)
	img.save(imgname)