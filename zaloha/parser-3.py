#!/usr/bin/python

import sys,socket,string,pygame,math

def budik(what,x,y,size,sizen,angle):
#    pygame.draw.rect(window,(0,0,0),(x-size,y-size,x+size,y+size))
    window.blit(what,(x,y))
    pygame.draw.line(window,(255,255,255),(x+size/2,y+size/2),(x+(size/2)+math.cos(angle*math.pi/180)*sizen,y+(size/2)+math.sin(angle*math.pi/180)*sizen))
#    return

def draw_blade(val):
	budik(blade,0,0,153,45,165+(210*float(val)))

def draw_radar(val):
	budik(radar,153,0,192,50,270+(340*float(val)))
	

pygame.init()

blade=pygame.image.load('blade.png')
radar=pygame.image.load('radar.png')

window=pygame.display.set_mode((640,480))

budik(blade,0,0,153,45,20)
budik(radar,153,0,192,50,270)
pygame.display.flip()

udp_ip="192.168.1.8"
udp_port=9089

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind( (udp_ip,udp_port) )

values={}

while True:
    data,addr=sock.recvfrom(1024)
    tmp=string.split(data[9:-1],":")
    for rec in tmp:
	key,val=string.split(rec,"=")
	try:
		values[int(key)]=val
	finally:
		pass

#    values_sorted=sorted(values.keys(),key=lambda x:values[x])
#    values=values_sorted
    for key,val in values.iteritems():
	if key==53:
#		print str(1+(float(val)*14))
#		pygame.draw.rect(window,(0,0,0),(25,10,75,50))
#		pygame.draw.aaline(window,(255,255,255),(50,50),(25+val*50,10),3)
		draw_blade(val)
	elif key==94:
		draw_radar(val)
		
    pygame.display.flip()

#  File "parser.py", line 40, in <module>
#    values[int(key)]=float(val)
#ValueError: invalid literal for float(): ELEC
#    ON
#BATTERY
#
#FLYING
