#!/usr/bin/python

import sys,socket,string,pygame,math

def prepocet(pre,c):
	for i in range(7-1):
#		print pre[i][0],c,pre[i+1][0]
		if pre[i][0]<=c and pre[i+1][0]>c:
			a=pre[i]
			b=pre[i+1]
			tmp=((c-a[0])/(b[0]-a[0]))
			return(tmp*(b[2]-a[2])+a[2])
#			print tmp*(b[1]-a[1])+a[1],tmp*(b[2]-a[2])+a[2]
	

def budik(what,x,y,size,sizen,angle):
    window.blit(what,(x,y))
    pygame.draw.aaline(window,(255,255,255),(x+size/2,y+size/2),(x+(size/2)+math.cos(angle*math.pi/180)*sizen,y+(size/2)+math.sin(angle*math.pi/180)*sizen))

def draw_blade(val):
	budik(blade,0,0,153,45,165+(210*float(val)))

def draw_radar(val):
	budik(radar,153,0,192,50,270+(prepocet(((0,0,0),(0.1838,20,65),(0.4631,50,165),(0.7541,150,270),(0.833,200,300),(0.9329,300,330),(1,350,340))
,float(val))))

def draw_vvi(val):
	budik(vvi,345,0,192,55,180+(180*float(val)))


pygame.init()

blade=pygame.image.load('blade.png')
radar=pygame.image.load('radar.png')
vvi=pygame.image.load('vvi.png')

window=pygame.display.set_mode((640,480))


draw_blade(0)
draw_radar(0)
draw_vvi(0)
pygame.display.flip()

udp_ip="192.168.1.8"
udp_port=9089

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind( (udp_ip,udp_port) )

while True:
    data,addr=sock.recvfrom(1024)
    tmp=string.split(data[9:-1],":")
    for rec in tmp:
	key,val=string.split(rec,"=")
	key=int(key)
	if key==53:
		draw_blade(val)
	elif key==94:
		draw_radar(val)
	elif key==24:
		draw_vvi(val)
		
    pygame.display.flip()


