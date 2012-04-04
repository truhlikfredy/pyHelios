#!/usr/bin/python

import sys,socket,string,pygame,math,time

text_offset=5*25


def conv_nonlinear(table,value):
	for i in range(len(table)-1):
		if table[i][0]<=value and table[i+1][0]>value:
			a=table[i]
			b=table[i+1]
			tmp=((value-a[0])/(b[0]-a[0]))
#			print tmp*(b[1]-a[1])+a[1],tmp*(b[2]-a[2])+a[2]
			return(tmp*(b[2]-a[2])+a[2])

def draw_needle(center_x,center_y,angle,color,size_x,size_y=None):
	if size_y==None:
		size_y=size_x

#	print angle,size_x
	pygame.draw.aaline(window,color,(center_x,center_y),(center_x+math.cos(angle*math.pi/180)*size_x,center_y+math.sin(angle*math.pi/180)*size_y))


def draw_gauge(what,x,y,size,size_needle,angle1,angle2=None):
    window.blit(what,(x,y))
    color1=(255,255,255)

    if angle2:
#	    pygame.draw.aaline(window,(255,150,150),(x+size/2,y+size/2),(x+(size/2)+math.cos(angle2*math.pi/180)*sizen,y+(size/2)+math.sin(angle2*math.pi/180)*sizen))
            draw_needle(x+size/2,y+size/2,angle2,(255,150,150),size_needle)
	    color1=(150,255,150)

#    pygame.draw.aaline(window,color1,(x+size/2,y+size/2),(x+(size/2)+math.cos(angle*math.pi/180)*sizen,y+(size/2)+math.sin(angle*math.pi/180)*sizen))
    draw_needle(x+size/2,y+size/2,angle1,color1,size_needle)

def draw_blade(val=0):
	draw_gauge(blade,153*0,153*0+text_offset,153,45,165+(210*float(val)))

def draw_ias(val=0):
	draw_gauge(ias,153*1,153*0+text_offset,153,45,275+(conv_nonlinear(( (0,0,0),(0.142857,50,90),(1,350,360)),float(val))))

def draw_acc(val=0,acc_min=0,acc_max=0):
	x=153*2
	y=153*0+text_offset
	size=153
	draw_gauge(acc,x,y,size,40,170+(300*float(val)))
	draw_needle(x+size/2,y+size/2,170+(300*float(acc_min)),(255,100,100),35)
	draw_needle(x+size/2,y+size/2,170+(300*float(acc_max)),(255,100,100),35)


def draw_rotor_rpm(val=0):
	draw_gauge(rotor_rpm,153*3,153*0+text_offset,153,40,315+(350*float(val)))


def draw_eng_rpm(val1=0,val2=0):
	draw_gauge(eng_rpm,153*4,153*0+text_offset,153,45,315+350*float(val1),315+350*float(val2))

def draw_fuel(val1=0,val2=0):
	draw_gauge(fuel,153*0,153*1+text_offset,153,45,115+305*float(val1),115+305*float(val2))

#draw_radar(ralt,ralt_danger,ralt_danger_lamp,ralt_flag)

def draw_radar(ralt=0,ralt_danger=0,ralt_danger_lamp=0,ralt_flag=0):
	#danger 0.6090
	scale=((0,0,0),(0.1838,20,65),(0.4631,50,165),(0.7541,150,270),(0.833,200,300),(0.9329,300,330),(1,350,340))
	x=192*1
	y=153*2+text_offset
	size=192

	if ralt:
		draw_gauge(radar,x,y,size,50,270+(conv_nonlinear(scale,float(ralt))))
	else:
		draw_gauge(radar,x,y,size,50,270+(conv_nonlinear(scale,0)))
	draw_needle(x+size/2,y+size/2,270+(conv_nonlinear(scale,float(ralt_danger))),(255,100,100),45)
	if float(ralt_danger_lamp)==1:
	    pygame.draw.circle(window,(255,0,0),(x+size-15,y+size-15),15)
	if float(ralt_flag)>0:
	    pygame.draw.circle(window,(255,50,50),(x+size/2,y+size/2),25)

def draw_vvi(val=0):
	draw_gauge(vvi,192*0,153*2+text_offset,192,55,180+(180*float(val)))

def draw_temp(val1=0,val2=0):
	x=153*1
	y=153*1+text_offset
	size=153
	window.blit(eng_temp,(x,y))
	color=(255,255,255)
	draw_needle(x+44,y+71,135+(float(val1)*270),color,20)
	draw_needle(x+44,y+102,90+((float(val1)*1200)%100)*3.60,color,15)

	draw_needle(x+106,y+71,135+(float(val2)*270),color,20)
	draw_needle(x+106,y+102,90+((float(val2)*1200)%100)*3.60,color,15)

def draw_baro(val=0):
	draw_gauge(baro,2*153,1*153+text_offset,153,55,270+(360*float(val)),270+(360*10*float(val)))

def draw_clock(hours=0,minutes=0,seconds=0,flight_status=0,flight_minutes=0,flight_seconds=0,sw_minutes=0,sw_seconds=0):
	x=153*3
	y=153*1+text_offset
	size=153
	window.blit(clock,(x,y))

#	73,51 7x7

	pygame.draw.rect(window,(100,100,100),(x+73,y+51,8,8))
	if (float(flight_status)==0.1):
		pygame.draw.rect(window,(255,100,100),(x+73,y+51,8,8))
	elif (float(flight_status)==0.2):
 		pygame.draw.rect(window,(255,100,100),(x+73+4,y+51,4,8))


	draw_needle(x+size/2,y+size/2,270+(float(hours)*360),(255,255,255),45)
	draw_needle(x+size/2,y+size/2,270+(float(minutes)*360),(255,100,100),50)
	draw_needle(x+size/2,y+size/2,270+(float(seconds)*360),(100,255,100),55)

	draw_needle(x+76,y+42,270+(float(flight_minutes)*360),(255,255,255),20)
	draw_needle(x+76,y+42,270+(float(flight_seconds)*360),(100,100,255),18)

	draw_needle(x+76,y+110,270+(float(sw_minutes)*360),(255,255,255),20)
	draw_needle(x+76,y+110,270+(float(sw_seconds)*360),(100,100,255),18)

def rot_center_square(image, angle):
	"""rotate an image while keeping its center and size"""
	orig_rect = image.get_rect()
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = orig_rect.copy()
	rot_rect.center = rot_image.get_rect().center
	rot_image = rot_image.subsurface(rot_rect).copy()
	return rot_image

def rot_center(image,rect,angle):
	rot_image=pygame.transform.rotate(image,angle)
	rot_rect=rot_image.get_rect(center=rect.center)
	return rot_image,rot_rect

def draw_adi(roll=0,pitch=0,sidelip=0):
	x=153*4
	y=153*1+text_offset
	size=153
	instr_center_x=76
	instr_center_y=69
	gulicka_y=146

	tmp=pygame.Surface((size,size))
	tmp.blit(adi_horizont,(0,0-(float(pitch)*22*9)))
	window.blit(tmp,(x,y))
#	window.blit(adi_horizont,(x,y),(0,float(pitch)*22*9))
	window.blit(adi_instrument,(x,y))

        adi_kri=pygame.transform.rotozoom(adi_kridla,-float(roll)*180,1)
	w,h=adi_kri.get_size()
#	print w,h
	window.blit(adi_kri,(x+(instr_center_x)-(w/2),y+(instr_center_y)-(h/2)))
#	rot,cen=rot_center(adi_kridla,-float(roll)*180)
#	window.blit(rot,(x,y))
#	window.blit(adi_kri,(x,y))
	w,h=adi_gulicka.get_size()
	window.blit(adi_gulicka,(x+instr_center_x+float(sidelip)*16-(w/2),y+gulicka_y-(h/2)))

#hsi_course_flag=0
#hsi_glide_flag=0
#hsi_range_hundreds=0
#hsi_range_tenth=0
#hsi_course_hundreds=0
#hsi_course_units=0

def draw_hsi(heading=0,cmd_course=0,cmd_heading=0,bearing=0,range_units=0,long_dev=0,late_dev=0,heading_flag=0,course_flag=0,course_na_flag=0):
	x=192*2
	y=153*2+text_offset
	size=192

	instr_center_x=96
	instr_center_y=96

	window.blit(hsi_hover_back,(x,y))

	#i want to have 55 but at moment the graphics layers are not ready for it so it will be 22
	tmp=pygame.Surface((size,size),0,hsi_hover_cross)
	tmp.blit(hsi_hover_cross,(float(late_dev)*22,-(float(long_dev)*22)))
	window.blit(tmp,(x,y))

	h_compas=pygame.transform.rotozoom(hsi_compas,(float(heading)*360),1)
	w,h=h_compas.get_size()
	window.blit(h_compas,(x+(instr_center_x)-(w/2),y+(instr_center_y)-(h/2)))

	h_rmi=pygame.transform.rotozoom(hsi_rmi,(-float(bearing)*360),1)
	w,h=h_rmi.get_size()
	window.blit(h_rmi,(x+(instr_center_x)-(w/2),y+(instr_center_y)-(h/2)))

	h_dta=pygame.transform.rotozoom(hsi_dta,((float(heading)-float(cmd_course))*360),1)
	w,h=h_dta.get_size()
	window.blit(h_dta,(x+(instr_center_x)-(w/2),y+(instr_center_y)-(h/2)))

	window.blit(hsi_top,(x,y))

	h_dh=pygame.transform.rotozoom(hsi_dh,(float(heading)-float(cmd_heading))*360,1)
	w,h=h_dh.get_size()
	window.blit(h_dh,(x+(instr_center_x)-(w/2),y+(instr_center_y)-(h/2)))

	text=font.render(str(int(float(cmd_course)*360)),1,(255,255,255))
	window.blit(text,(x+146,y+18))

	text=font.render(str(int(float(range_units)*10)),1,(255,255,255))
	window.blit(text,(x+17,y+18))


	if float(heading_flag)==1:
	    window.blit(hsi_kc,(x,y))

	if float(course_flag)==1:
	    window.blit(hsi_k,(x,y))

	if float(course_na_flag)==1:
	    window.blit(hsi_l,(x,y))


pygame.init()

blade=pygame.image.load('blade.png')
radar=pygame.image.load('radar.png')
vvi=pygame.image.load('vvi.png')
ias=pygame.image.load('ias.png')
rotor_rpm=pygame.image.load('rotor-rpm.png')
acc=pygame.image.load('acc.png')
eng_rpm=pygame.image.load('eng-rpm.png')
clock=pygame.image.load('clock2.png')
fuel=pygame.image.load('fuel.png')
eng_temp=pygame.image.load('temp.png')
baro=pygame.image.load('baro.png')

adi_horizont=pygame.image.load('adi-horizont.png')
adi_instrument=pygame.image.load('adi-instrument.png')
adi_kridla=pygame.image.load('adi-kridla.png')
adi_gulicka=pygame.image.load('adi-gulicka.png')

hsi_compas=pygame.image.load('hsi-compas.png')
hsi_dta=pygame.image.load('hsi-dta.png')
hsi_hover_back=pygame.image.load('hsi-hover-back.png')
hsi_hover_cross=pygame.image.load('hsi-hover-cross.png')
hsi_k=pygame.image.load('hsi-k.png')
hsi_kc=pygame.image.load('hsi-kc.png')
hsi_l=pygame.image.load('hsi-l.png')
hsi_rmi=pygame.image.load('hsi-rmi.png')
hsi_top=pygame.image.load('hsi-top.png')
hsi_dh=pygame.image.load('hsi-dh.png')

window=pygame.display.set_mode((768,650))
font=pygame.font.Font(None,24)
sf=pygame.font.Font(None,15)

draw_blade()
draw_radar()
draw_vvi()
draw_ias()
draw_rotor_rpm()
draw_acc(1)
draw_eng_rpm()
draw_fuel()
draw_temp()
draw_baro()
draw_clock()
draw_adi()
draw_hsi()

lamps=(
(
(237,3,"fire",3,"lh eng"),
(239,3,"fire",3,"apu"),
(568,3,"fire",3,"hydr"),
(241,3,"fire",3,"rh eng"),
(243,3,"fire",3,"grbx"),
(244,3,"1",3,""),
(245,3,"2",3,""),
(655535,4,"",4,""),
(655535,4,"",4,""),
(655535,4,"",4,""),
(655535,4,"",4,""),
(655535,4,"",4,""),
(655535,4,"",4,""),
),(
(655535,4,"",4,""),
(165,0,"ENR",0,"NAV ON"),
(164,0,"AC-POS",0,"CAL-DATA"),
(211,0,"X-FEED",0,"VLV OPEN"),
(167,0,"MASTER",0,"ARM ON"),
(189,1,"computer",1,"diagnose"),
(181,2,"lh eng",2,"anti-ice"),
(182,2,"rh eng",2,"anti-ice"),
(200,2,"fwd tank",0,"pump on"),
(201,2,"aft tank",0,"pump on"),
(78,3,"lh eng",3,"overspd"),
(79,3,"rh eng",3,"overspd"),
(80,3,"over-g",3,"")
),(
(170,0,"r-alt",0,"hold"),
(171,0,"enr",0,"course"),
(178,2,"weap",2,"arm"),
(187,0,"turbo",0,"gear"),
(180,0,"weapon",0,"training"),
(206,1,"computer",1,"fail"),
(190,0,"lh eng",0,"dust-prot"),
(191,0,"rh eng",0,"dust-prot"),
(209,0,"lh vlv",0,"closed"),
(210,0,"rh vlv",0,"closed"),
(81,3,"lh eng",3,"vibr"),
(82,3,"rh eng",3,"vibr"),
(83,3,"ias",3,"max")
),(
(175,0,"auto",0,"hover"),
(176,0,"next",0,"wp"),
(173,0,"cannon",0,""),
(204,0,"agb",0,"oil press"),
(179,1,"hms",1,"fail"),
(212,0,"inverter",0,"on"),
(207,1,"lh power",1,"set lim"),
(208,1,"rh power",1,"set lim"),
(185,0,"lh outer",0,"tank pump"),
(186,0,"rh outer",0,"tank pump"),
(84,3,"main",3,"grbx"),
(85,3,"fire",3,""),
(86,3,"iff",3,"fail")
),(
(172,0,"auto",0,"descent"),
(166,0,"route",0,"end"),
(177,0,"cannon",0,"v"),
(213,0,"sl-hook",0,"open"),
(188,1,"hud",1,"no ready"),
(205,1,"skval",1,"fail"),
(183,0,"rotor",0,"anti-ice"),
(184,0,"wndshld",0,"heater"),
(202,0,"lh inner",0,"tank pump"),
(203,0,"rh inner",0,"tank pump"),
(46,1,"rotor",1,"rpm"),
(44,3,"master",3,"warning"),
(2222,4,"",4,"")
))

lamps_color=(
(60,255,60),
(255,255,60),
(200,255,200),
(255,60,60),
(0,0,0)
)

lamps_back=(
(0,60,0),
(60,60,0),
(30,60,30),
(60,0,0),
(0,0,0)
)



#5*25 offset under the text

#text=sf.render("R-ALT COURSE WEAP TURBO MASTER COMPUTER ANTI-ICE ANTI-ICE FWD TANK AFT TANK LH ENG RH ENG OVER-G",1,(255,255,255))
#window.blit(text,(0,0))

pygame.display.flip()

while False:
	for l in range(360):
		draw_hsi((float(l))/360)
		pygame.display.flip()
		time.sleep(0.1)


udp_ip="192.168.1.8"
udp_port=9089

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind( (udp_ip,udp_port) )

pygame.display.flip()

eng_rpm1=0
eng_rpm2=0
eng_rpm_refresh=False

fuel1=0
fuel2=0
fuel_refresh=False

eng_temp1_hund=0
eng_temp1_tenth=0
eng_temp2_hund=0
eng_temp2_tenth=0
eng_temp_refresh=False

baro_thousands=0
baro_tenth=0
baro_pressure=0
baro_refresh=False

clock_hours=0
clock_minutes=0
clock_seconds=0
clock_flight_status=0
clock_flight_hours=0
clock_flight_minutes=0
clock_sw_minutes=0
clock_sw_seconds=0
clock_refresh=False

adi_refresh=False
adi_roll=0
adi_pitch=0
adi_steering_flag=0
adi_attitude_flag=0
adi_bank_steering=0
adi_pitch_steering=0
adi_airspeed_dev=0
adi_track_dev=0
adi_height_dev=0
adi_sideslip=0

ralt_refresh=False
ralt=0
ralt_danger=0
ralt_danger_lamp=0
ralt_flag=0

acc_refresh=False
acc_val=0
acc_min=0
acc_max=0

hsi_refresh=False
hsi_heading=0
hsi_cmd_course=0
hsi_cmd_heading=0
hsi_bearing=0
hsi_heading_flag=0
hsi_course_flag=0
hsi_glide_flag=0
hsi_range_hundreds=0
hsi_range_tenth=0
hsi_range_units=0
hsi_course_hundreds=0
hsi_course_units=0
hsi_long_dev=0
hsi_late_dev=0
hsi_range_flag=0
hsi_course_na_flag=0


while True:
    data,addr=sock.recvfrom(1024)
    tmp=string.split(data[9:-1],":")
    for rec in tmp:
	key,val=string.split(rec,"=")
	key=int(key)
	if key==53:
		draw_blade(val)
	elif key==94:
		ralt=val
		ralt_refresh=True
	elif key==93:
		ralt_danger=val
		ralt_refresh=True
	elif key==92:
		ralt_danger_lamp=val
		ralt_refresh=True
	elif key==95:
		ralt_flag=val
		ralt_refresh=True
	elif key==24:
		draw_vvi(val)
		pass
	elif key==51:
		draw_ias(val)
	elif key==52:
		draw_rotor_rpm(val)
	elif key==97:
		acc_val=val
		acc_refresh=True
	elif key==98:
		acc_max=val
		acc_refresh=True
	elif key==99:
		acc_min=val
		acc_refresh=True
	elif key==135:
                eng_rpm1=val
		eng_rpm_refresh=True
        elif key==136:
		eng_rpm2=val
		eng_rpm_refresh=True
	elif key==137:
		fuel1=val
		fuel_refresh=True
	elif key==138:
		fuel2=val
		fuel_refresh=True
	elif key==133:
		eng_temp1_hund=val
		eng_temp_refresh=True
	elif key==566:
		eng_temp1_tenth=val
		eng_temp_refresh=True
	elif key==134:
		eng_temp2_hund=val
		eng_temp_refresh=True
	elif key==567:
		eng_temp2_tenth=val
		eng_temp_refresh=True
	elif key==87:
		baro_thousands=val
		baro_refresh=True
	elif key==573:
		baro_tenth=val
		baro_refresh=True
	elif key==98:
		baro_pressure=val
		baro_refresh=True
	elif key==68:
		clock_hours=val
		clok_refresh=True
	elif key==69:
		clock_minutes=val
		clock_refresh=True
 	elif key==70:
		clock_seconds=val
		clock_refresh=True
	elif key==75:
		clock_flight_status=val
		clock_refresh=True
	elif key==72:
		clock_flight_hours=val
		clock_refresh=True
	elif key==531:
		clock_flight_minutes=val
		clock_refresh=True
	elif key==73:
		clock_sw_minutes=val
		clock_refresh=True
	elif key==532:
		clock_sw_seconds=val
		clock_refresh=True
	elif key==100:			#treba dorobit aj tie palicky sa vyklonia ked je test
		adi_roll=val
		adi_refresh=True
	elif key==101:
		adi_pitch=val
		adi_refresh=True
	elif key==102:
		adi_steering_flag=val
		adi_refresh=True
	elif key==109:
		adi_attitude_flag=val
		adi_refresh=True
	elif key==107:
		adi_bank_steering=val
		adi_refresh=True
	elif key==106:
		adi_pitch_steering=val
		adi_refresh=True
	elif key==111:
		adi_airspeed_dev=val
		adi_refresh=True
	elif key==103:
		adi_track_dev=val
		adi_refresh=True
	elif key==526:
		adi_height_dev=val
		adi_refresh=True
	elif key==108:
		adi_sideslip=val
		adi_refresh=True
	elif key==112:
		hsi_heading=val
		hsi_refresh=True
	elif key==118:
		hsi_cmd_course=val
		hsi_refresh=True
	elif key==124:
		hsi_cmd_heading=val
		hsi_refresh=True
	elif key==115:
		hsi_bearing=val
		hsi_refresh=True
	elif key==119:
		hsi_heading_flag=val
		hsi_refresh=True
	elif key==114:
		hsi_course_flag=val
		hsi_refresh=True
	elif key==125:
		hsi_glide_flag=val	#asi a-10
		hsi_refresh=True
	elif key==117:
		hsi_range_hundreds=val
		hsi_refresh=True
	elif key==527:
		hsi_range_tenth=val
		hsi_refresh=True
	elif key==528:
		hsi_range_units=val
		hsi_refresh=True
	elif key==529:
		hsi_course_hundreds=val
		hsi_refresh=True
	elif key==530:
		hsi_course_units=val
		hsi_refresh=True
	elif key==127:
		hsi_long_dev=val
		hsi_refresh=True
	elif key==128:
		hsi_late_dev=val
		hsi_refresh=True
	elif key==116:
		hsi_range_flag=val
		hsi_refresh=True
	elif key==121:
		hsi_course_na_flag=val
		hsi_refresh=True
	else:
	    try:
#		string.isdigit(val)
		value_int=float(val)
		for row in range(5):
		    for l in range(13):
			rec=lamps[row][l]
			if rec[0]==key:
				pygame.draw.rect(window,lamps_back[rec[1]],(l*59,row*25-3,59,25))
				if value_int>0:
					text=sf.render(rec[2].upper(),1,lamps_color[rec[1]])
					w,h=text.get_size()
					window.blit(text,(59*l+59/2-w/2,0+row*25))

					text=sf.render(rec[4].upper(),1,lamps_color[rec[3]])
					w,h=text.get_size()
					window.blit(text,(59*l+59/2-w/2,10+row*25))
	    except:
		print str(key)+'='+val
		pass

#2004=ekran

    if hsi_refresh==True:
#	print hsi_heading,hsi_cmd_course,hsi_cmd_heading,hsi_bearing,hsi_heading_flag,hsi_course_flag,hsi_glide_flag
#	print hsi_range_hundreds,hsi_range_tenth,hsi_range_units,hsi_course_hundreds,hsi_course_units,hsi_long_dev,hsi_late_dev,hsi_range_flag,hsi_course_na_flag

#	print hsi_glide_flag,hsi_range_hundreds,hsi_range_tenth,hsi_course_hundreds,hsi_course_units
#	print hsi_long_dev,hsi_late_dev,hsi_range_flag
	draw_hsi(hsi_heading,hsi_cmd_course,hsi_cmd_heading,hsi_bearing,hsi_range_units,hsi_long_dev,hsi_late_dev,hsi_heading_flag,hsi_course_flag,hsi_course_na_flag)
	hsi_refresh=False

    if acc_refresh==True:
#	print acc_val,acc_min,acc_max
	draw_acc(acc_val,acc_min,acc_max)
	acc_refresh=False

    if ralt_refresh==True:
#	print ralt,ralt_danger,ralt_danger_lamp,ralt_flag
	draw_radar(ralt,ralt_danger,ralt_danger_lamp,ralt_flag)
	ralt_refresh=False

    if eng_rpm_refresh==True:
	draw_eng_rpm(eng_rpm1,eng_rpm2)
	eng_rpm_refresh=False

    if fuel_refresh==True:
	draw_fuel(fuel1,fuel2)
	fuel_refresh=False

    if eng_temp_refresh==True:
#	print(eng_temp1_hund,eng_temp1_tenth,eng_temp2_hund,eng_temp2_tenth)
#	print(round(float(eng_temp1_hund)*1200),round(float(eng_temp2_hund)*1200))
	draw_temp(eng_temp1_hund,eng_temp2_hund)
	eng_temp_refresh=False

    if baro_refresh==True:
#	print float(baro_thousands)*10000,baro_tenth,baro_pressure,600+float(baro_pressure)*200
	baro_refresh=False
	draw_baro(baro_thousands)

    if clock_refresh==True:
#	print clock_hours,clock_minutes,clock_seconds,clock_flight_status,clock_flight_hours,clock_flight_minutes,clock_sw_minutes,clock_sw_seconds
	draw_clock(clock_hours,clock_minutes,clock_seconds,clock_flight_status,clock_flight_hours,clock_flight_minutes,clock_sw_minutes,clock_sw_seconds)
	clock_refresh=False

    if adi_refresh==True:
#	print adi_roll,adi_pitch,adi_steering_flag,adi_attitude_flag,adi_bank_steering,adi_pitch_steering,adi_airspeed_dev,adi_track_dev,adi_height_dev,adi_sideslip
#	print str(float(adi_roll)*360)

#####	dorobit steerting a attitude flag
	draw_adi(adi_roll,adi_pitch,adi_sideslip)
	adi_refresh=False

    pygame.display.flip()

