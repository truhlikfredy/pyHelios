#!/usr/bin/python

import sys,socket,string,pygame,math,time,gc
from collections import defaultdict

gau=defaultdict(int)
gau_text={}

def conv_nonlinear(table,value):
    for i in range(len(table)-1):
        if table[i][0]<=value and table[i+1][0]>value:
            a=table[i]
            b=table[i+1]
            tmp=((value-a[0])/(b[0]-a[0]))
            return(tmp*(b[2]-a[2])+a[2])

class gauges:
    color={'white':(255,255,255),'red':(255,150,150),'red+':(255,100,100),'red++':(255,50,50),'red+++':(255,0,0),'green':(150,255,150),'green+':(100,255,100),'grey':(100,100,100)}

    def __init__(self,bg,origin,size,radius=None,draw_on_init=True):
        if radius==None:
            radius=size/2

        x,y=origin

        self.next_right=(x+size,y)
        self.next_row=(0,y+size)
        self.refresh=True
        self.val={0:0,1:None}
        self.val_old={0:-1,1:None}

        self.bg=pygame.image.load(bg)
        self.x=x
        self.y=y
        self.origin=(x,y)
        self.size=size
        self.radius=radius
        self.center=(self.x+self.size/2,self.y+self.size/2)

        if draw_on_init==True:
            self.check_draw()

    def rotate(self,what,angle):
        tmp=pygame.transform.rotozoom(what,angle,1)
        w,h=tmp.get_size()
        window.blit(tmp,(self.x+self.instr_x-w/2,self.y+self.instr_y-h/2))

    def draw_needle(self,center,angle,color,size_x=None,size_y=None):
        if center==None:
            center=self.center

        if size_x==None:
            size_x=self.size

        if size_y==None:
            size_y=size_x

        center_x,center_y=center
        max=2
        for l in range(-max,max+1):
            off_x=math.cos((angle+90)*math.pi/180)*l*0.5
            off_y=math.sin((angle+90)*math.pi/180)*l*0.5
            point=math.fabs(l)*2
            pygame.draw.aaline(window,color,(center_x+off_x,center_y+off_y),(center_x+off_x+math.cos(angle*math.pi/180)*(size_x-point),center_y+off_y+math.sin(angle*math.pi/180)*(size_y-point)))

    def draw_gauge(self,size_needle,angle1,angle2=None):
        window.blit(self.bg,self.origin)
        color1=self.color['white']
        if angle2:
            self.draw_needle(None,angle2,self.color['red'],size_needle)
            color1=self.color['green']
        self.draw_needle(None,angle1,color1,size_needle)

    def check(self):
        self.refresh=False
        for key in self.val.keys():
            if not self.val_old.has_key(key) or self.val[key]!=self.val_old[key]:
                self.refresh=True
            self.val_old[key]=self.val[key]
        return(self.refresh)

    def draw(self):
        if self.refresh==True:
            self.draw_gauge(self.radius,self.val[0],self.val[1])
            self.refresh=False
            return(True)
        else:
            return(False)

    def check_draw_default(self):
        self.check()
        return(self.draw())

    def check_draw(self):
        self.check_draw_default()


class vvi_gauge(gauges):
    def check_draw(self):
        self.val[0]=180+180*gau[24]
        self.check_draw_default()

class blade_gauge(gauges):
    def check_draw(self):
        self.val[0]=165+210*gau[53]
        self.check_draw_default()

class ias_gauge(gauges):
    def check_draw(self):
        self.val[0]=275+(conv_nonlinear(((0,0,0),(0.142857,50,90),(1,350,360)),gau[51]))
        self.check_draw_default()

class acc_gauge(gauges):
    def check_draw(self):
        self.val[0]=170+300*gau[97]
        self.val['min']=170+300*gau[99]
        self.val['max']=170+300*gau[98]
        if self.check_draw_default():
            self.draw_needle(None,self.val['min'],self.color['red+'],self.radius-5)
            self.draw_needle(None,self.val['max'],self.color['red+'],self.radius-5)

class rotor_rpm_gauge(gauges):
    def check_draw(self):
        self.val[0]=315+350*gau[52]
        self.check_draw_default()

class eng_rpm_gauge(gauges):
    def check_draw(self):
        self.val[0]=315+350*gau[135]
        self.val[1]=315+350*gau[136]
        self.check_draw_default()

class fuel_gauge(gauges):
    def check_draw(self):
        self.val[0]=115+305*gau[137]
        self.val[1]=115+305*gau[138]
        self.check_draw_default()

class baro_gauge(gauges):
    #value #573 is tenth of unit, but no data stream -> perhaps from A-10?
    def check_draw(self):
        self.val[0]=270+360*gau[87]
        self.val[1]=270+3600*gau[87]
        self.val['pressure']=gau[98]
        self.check_draw_default()

class temp_gauge(gauges):
    #566 eng1_tenth & 567 eng2_tenth = no data
    def check_draw(self):
        self.val['eng1']=135+270*gau[133]
        self.val['eng1_tenth']=90+(1200*gau[133])%100
        self.val['eng2']=135+270*gau[134]
        self.val['eng2_tenth']=90+(1200*gau[134])%100
        if self.check():
            window.blit(self.bg,self.origin)
            self.draw_needle((self.x+44,self.y+71),self.val['eng1'],self.color['white'],self.radius)
            self.draw_needle((self.x+44,self.y+102),self.val['eng1_tenth'],self.color['white'],self.radius-5)
            self.draw_needle((self.x+106,self.y+71),self.val['eng2'],self.color['white'],self.radius)
            self.draw_needle((self.x+106,self.y+102),self.val['eng2_tenth'],self.color['white'],self.radius-5)

class clock_gauge(gauges):
    def check_draw(self):
        self.val['hours']=270+360*gau[68]
        self.val['min']=270+360*gau[69]
        self.val['sec']=270+360*gau[70]
        self.val['flight_status']=gau[75]
        self.val['flight_hours']=270+360*gau[72]
        self.val['flight_min']=270+360*gau[531]
        self.val['sw_min']=270+360*gau[73]
        self.val['sw_sec']=270+360*gau[532]

        if self.check():
            window.blit(self.bg,self.origin)

            pygame.draw.rect(window,self.color['grey'],(self.x+73,self.y+51,8,8))
            if (self.val['flight_status']==0.1):
                pygame.draw.rect(window,self.color['red+'],(self.x+73,self.y+51,8,8))
            elif (self.val['flight_status']==0.2):
                pygame.draw.rect(window,self.color['red+'],(self.x+73+4,self.y+51,4,8))

            self.draw_needle(None,self.val['hours'],self.color['white'],45)
            self.draw_needle(None,self.val['min'],self.color['red+'],50)
            self.draw_needle(None,self.val['sec'],self.color['green+'],55)

            self.draw_needle((self.x+76,self.y+42),self.val['flight_hours'],self.color['white'],self.radius)
            self.draw_needle((self.x+76,self.y+42),self.val['flight_min'],self.color['red+'],self.radius-2)

            self.draw_needle((self.x+76,self.y+110),self.val['sw_min'],self.color['red+'],self.radius)
            self.draw_needle((self.x+76,self.y+110),self.val['sw_sec'],self.color['green+'],self.radius-2)

class radar_gauge(gauges):
    #default danger 0.6090
    def check_draw(self):
        scale=((0,0,0),(0.1838,20,65),(0.4631,50,165),(0.7541,150,270),(0.833,200,300),(0.9329,300,330),(1,350,340))

        self.val[0]=270+conv_nonlinear(scale,gau[94])
        self.val['danger']=270+conv_nonlinear(scale,gau[93])
        self.val['danger_lamp']=gau[92]
        self.val['flag']=gau[95]
        if self.check_draw_default():
            self.draw_needle(None,self.val['danger']    ,self.color['red+'],self.radius-5)
            if self.val['danger_lamp']==1:
                pygame.draw.circle(window,self.color['red+++'],(self.x+self.size-15,self.y+self.size-15),15)
            if self.val['flag']>0:
                pygame.draw.circle(window,self.color['red++'],self.center,25)

class adi_gauge(gauges):
    #not all informations are displaying, but it's in just very rare cases when they are needed and are not in the default values
    def __init__(self,bg,origin,size,radius=None,draw_on_init=True):
        self.horisont=pygame.image.load('img/adi-horisont.png')
        self.wings=pygame.image.load('img/adi-wings.png')
        self.ball=pygame.image.load('img/adi-ball.png')
        self.instr_x=76
        self.instr_y=69
        self.ball_y=146
        gauges.__init__(self,bg,origin,size,radius,draw_on_init)

    def check_draw(self):
        self.val['roll']=180*gau[100]
        self.val['pitch']=22*9*gau[101]
        self.val['steering_flag']=gau[102]
        self.val['attitude_flag']=gau[109]
        self.val['bank_steering']=gau[107]
        self.val['pitch_steering']=gau[106]
        self.val['airspeed_dev']=gau[111]
        self.val['track_dev']=gau[103]
        self.val['height_dev']=gau[526]
        self.val['sideslip']=gau[108]

        if self.check():
            tmp=pygame.Surface((self.size,self.size))
            tmp.blit(self.horisont,(0,-self.val['pitch']))
            window.blit(tmp,self.origin)
            window.blit(self.bg,self.origin)

            self.rotate(self.wings,-self.val['roll'])

            w,h=self.ball.get_size()
            window.blit(self.ball,(self.x+self.instr_x+self.val['sideslip']*16-w/2,self.y+self.ball_y-h/2))

class hsi_gauge(gauges):
    #not sure if data for these:
    #hsi_course_flag
    #hsi_glide_flag
    #hsi_range_hundreds
    #hsi_range_tenth
    #hsi_course_hundreds
    #hsi_course_units
    def __init__(self,bg,origin,size,radius=None,draw_on_init=True):
        self.compas=pygame.image.load('img/hsi-compas.png')
        self.dta=pygame.image.load('img/hsi-dta.png')
        self.hover_back=pygame.image.load('img/hsi-hover-back.png')
        self.hover_cross=pygame.image.load('img/hsi-hover-cross.png')
        self.k=pygame.image.load('img/hsi-k.png')
        self.kc=pygame.image.load('img/hsi-kc.png')
        self.l=pygame.image.load('img/hsi-l.png')
        self.rmi=pygame.image.load('img/hsi-rmi.png')
        self.dh=pygame.image.load('img/hsi-dh.png')

        self.instr_x=96
        self.instr_y=96

        self.font=pygame.font.Font(None,24)

        gauges.__init__(self,bg,origin,size,radius,draw_on_init)

    def check_draw(self):
        self.val['heading']=gau[112]
        self.val['cmd_course']=gau[118]
        self.val['cmd_heading']=gau[124]
        self.val['bearing']=gau[115]
        self.val['heading_flag']=gau[119]
        self.val['course_flag']=gau[114]
        self.val['glide_flag']=gau[124]     #maybe from A-10
        self.val['range_hundreds']=gau[117]
        self.val['range_tenth']=gau[527]
        self.val['range_units']=gau[528]
        self.val['course_hundreds']=gau[529]
        self.val['course_units']=gau[528]
        self.val['long_dev']=gau[127]
        self.val['late_dev']=gau[128]
        self.val['range_flag']=gau[116]
        self.val['course_na_flag']=gau[121]

        if self.check():
            window.blit(self.hover_back,self.origin)

            #i want to have 55 but at moment the graphics layers are not ready for it so it will be 22
            tmp=pygame.Surface((self.size,self.size),0,self.hover_cross)
            tmp.blit(self.hover_cross,(self.val['late_dev']*22,-self.val['long_dev']*22))
            window.blit(tmp,self.origin)

            self.rotate(self.compas,self.val['heading']*360)
            self.rotate(self.rmi,-self.val['bearing']*360)
            self.rotate(self.dta,(self.val['heading']-self.val['cmd_course'])*360)

            window.blit(self.bg,self.origin)

            self.rotate(self.dh,(self.val['heading']-self.val['cmd_heading'])*360)

            text=self.font.render(str(int(self.val['cmd_course']*360)),1,self.color['white'])
            window.blit(text,(self.x+146,self.y+18))

            text=self.font.render(str(int(self.val['range_units']*10)),1,self.color['white'])
            window.blit(text,(self.x+17,self.y+18))

            if self.val['heading_flag']==1:
                window.blit(self.kc,self.origin)

            if self.val['course_flag']==1:
                window.blit(self.k,self.origin)

            if self.val['course_na_flag']==1:
                window.blit(self.l,self.origin)

class lamps_class:
    bg=((0,30,0),(30,30,0),(25,30,25),(30,0,0),(0,0,0))
    bg_active=((0,60,0),(60,60,0),(50,60,50),(60,0,0),(0,0,0))
    text=((60,255,60),(255,255,60),(200,255,200),(255,60,60),(0,0,0))

    width=59
    height=25
    offset=3

    mesh=(
    ((655535,4,"",4,""),(165,0,"ENR",0,"NAV ON"),(164,0,"AC-POS",0,"CAL-DATA"),(211,0,"X-FEED",0,"VLV OPEN"),(167,0,"MASTER",0,"ARM ON"),(189,1,"computer",1,"diagnose"),(181,2,"lh eng",2,"anti-ice"),(182,2,"rh eng",2,"anti-ice"),(200,2,"fwd tank",0,"pump on"),(201,2,"aft tank",0,"pump on"),(78,3,"lh eng",3,"overspd"),(79,3,"rh eng",3,"overspd"),(80,3,"over-g",3,"")),
    ((170,0,"r-alt",0,"hold"),(171,0,"enr",0,"course"),(178,3,"weap",3,"arm"),(187,0,"turbo",0,"gear"),(180,0,"weapon",0,"training"),(206,1,"computer",1,"fail"),(190,0,"lh eng",0,"dust-prot"),(191,0,"rh eng",0,"dust-prot"),(209,0,"lh vlv",0,"closed"),(210,0,"rh vlv",0,"closed"),(81,3,"lh eng",3,"vibr"),(82,3,"rh eng",3,"vibr"),(83,3,"ias",3,"max")),
    ((175,0,"auto",0,"hover"),(176,0,"next",0,"wp"),(173,0,"cannon",0,""),(204,0,"agb",0,"oil press"),(179,1,"hms",1,"fail"),(212,0,"inverter",0,"on"),(207,1,"lh power",1,"set lim"),(208,1,"rh power",1,"set lim"),(185,0,"lh outer",0,"tank pump"),(186,0,"rh outer",0,"tank pump"),(84,3,"main",3,"grbx"),(85,3,"fire",3,""),(86,3,"iff",3,"fail")),
    ((172,0,"auto",0,"descent"),(166,0,"route",0,"end"),(177,0,"cannon",0,"v"),(213,0,"sl-hook",0,"open"),(188,1,"hud",1,"no ready"),(205,1,"skval",1,"fail"),(183,0,"rotor",0,"anti-ice"),(184,0,"wndshld",0,"heater"),(202,0,"lh inner",0,"tank pump"),(203,0,"rh inner",0,"tank pump"),(46,1,"rotor",1,"rpm"),(44,3,"master",3,"warning"),(2222,4,"",4,"")),
    ((237,3,"fire",3,"lh eng"),(239,3,"fire",3,"apu"),(568,3,"fire",3,"hydr"),(241,3,"fire",3,"rh eng"),(243,3,"fire",3,"grbx"),(244,3,"1",3,""),(245,3,"2",3,""),(655535,4,"",4,""),(6,2,"apu tmp",2,""),(162,2,"apu vlv",2,"open"),(168,2,"apu oil",2,"press"),(169,2,"apu stop",2,"rpm"),(174,2,"apu",2,"on"))
    )

    rows=len(mesh)
    cols=len(mesh[0])

    def __init__(self):
        self.next_right=(self.width*self.cols,self.height)
        self.next_row=(0,self.height*self.rows-self.offset)
        self.sf=pygame.font.Font(None,14)
        self.draw(True)

    def draw(self,force=False):
        for r in range(self.rows):
            for c in range(self.cols):
                rec=self.mesh[r][c]
                if gau[rec[0]]>0 or force:
                    pygame.draw.rect(window,self.bg_active[rec[1]],(c*59,r*25-self.offset,self.width-1,self.height-1))

                    text=self.sf.render(rec[2].upper(),1,self.text[rec[1]])
                    w,h=text.get_size()
                    window.blit(text,(c*self.width+self.width/2-w/2,r*self.height,self.width,self.height))

                    txt=rec[4].upper()
                    if r==4 and c==8:
                        txt=str(int(900*gau[6]))
                    text=self.sf.render(txt,1,self.text[rec[3]])
                    w,h=text.get_size()
                    window.blit(text,(c*self.width+self.width/2-w/2,r*self.height+10,self.width,self.height))
                else:
                    pygame.draw.rect(window,self.bg[rec[1]],(c*self.width,r*self.height-self.offset,self.width-1,self.height-1))
#            pygame.draw.line(window,(0,0,0),(0,r*self.height-3),(self.cols*self.width,r*self.height-3))

class ekran_class:
    color=(239,171,1)
    def __init__(self,origin):
        self.w=100
        self.h=25*3
        self.origin=origin
        self.x,self.y=origin
        self.f=pygame.font.Font(None,16)
        self.draw()

    def  draw(self):
#        window.blit(self.f.render(gau[2004],1,self.color),self.origin)
         if gau_text.has_key(2004):
            text=gau_text[2004].split('\n')
            if len(text)==4:
                pygame.draw.rect(window,(0,0,0),(self.x,self.y,self.w,self.h))
                off=0
                for txt in text:
                    line=self.f.render(txt,1,self.color)
                    window.blit(line,(self.x,self.y+off))
                    w,h=line.get_size()
                    off=off+h
#            window.blit(self.f.render(text[2],1,self.color),(self.x,self.y+25))
#            window.blit(self.f.render(text[3],1,self.color),(self.x,self.y+50))


gauge_small=153
gauge_big=192

pygame.init()
window=pygame.display.set_mode((768,650))

lamps=lamps_class()

blade=blade_gauge('img/blade.png',lamps.next_row,gauge_small,45)
ias=ias_gauge('img/ias.png',blade.next_right,gauge_small,45)
acc=acc_gauge('img/acc.png',ias.next_right,gauge_small,40)
rotor_rpm=rotor_rpm_gauge('img/rotor-rpm.png',acc.next_right,gauge_small,40)
eng_rpm=eng_rpm_gauge('img/eng-rpm.png',rotor_rpm.next_right,gauge_small,45)

fuel=fuel_gauge('img/fuel.png',eng_rpm.next_row,gauge_small,45)
temp=temp_gauge('img/temp.png',fuel.next_right,gauge_small,20)
baro=baro_gauge('img/baro.png',temp.next_right,gauge_small,55)
clock=clock_gauge('img/clock.png',baro.next_right,gauge_small,20)
adi=adi_gauge('img/adi-instrument.png',clock.next_right,gauge_small)

vvi=vvi_gauge('img/vvi.png',adi.next_row,gauge_big,55)
radar=radar_gauge('img/radar.png',vvi.next_right,gauge_big,50)
hsi=hsi_gauge('img/hsi-top.png',radar.next_right,gauge_big)
ekran=ekran_class(hsi.next_right)


pygame.display.flip()

udp_ip="192.168.1.8"
udp_port=9089

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind( (udp_ip,udp_port) )

#2001,2002,2004 ekran \n+3riadky,

while True:
    data,addr=sock.recvfrom(1024)
    tmp=string.split(data[9:-1],":")
    for rec in tmp:
        key,val=string.split(rec,"=")
        key=int(key)

        try:
            val=float(val)
            gau[key]=val
        except:
            print str(key)+' = '+val
            gau_text[key]=val
            pass


#        print str(key)+'='+str(gau[key])
#        print gau[24]

    for obj in gc.get_objects():
        if isinstance(obj,gauges):
            obj.check_draw()

    lamps.draw()
    ekran.draw()

    pygame.display.flip()
