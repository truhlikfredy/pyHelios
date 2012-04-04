#include <arpa/inet.h>
  #include <netinet/in.h>
  #include <stdio.h>
  #include <sys/types.h>
  #include <sys/socket.h>
#include <unistd.h>
#include <string.h>

  #define BUFLEN 2000
  #define NPACK 10
  #define PORT 9089

/* void diep(char *s)
  {
    perror(s);
    exit(1);
  }
*/

void gotoxy(int x, int y)
{
  printf("\033[%d;%df", y, x);
  fflush(stdout);
}

 int main(void)
  {
    struct sockaddr_in si_me, si_other;
    int s, i, slen=sizeof(si_other);
    char buf[BUFLEN];
    char buf2[BUFLEN];

    char * pch;
    if ((s=socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP))==-1)
      return(1);

    memset((char *) &si_me, 0, sizeof(si_me));
    si_me.sin_family = AF_INET;
    si_me.sin_port = htons(PORT);
    si_me.sin_addr.s_addr = htonl(INADDR_ANY);
    if (bind(s, &si_me, sizeof(si_me))==-1)
        return(1);

//    for (i=0; i<NPACK; i++) {
//    system("clear");
    while(1) {
      int  id[100];
      double hodnota[100];
      int ind=0;
//      gotoxy(1,1);
      if (recvfrom(s, buf, BUFLEN, 0, &si_other, &slen)==-1)
        return(1);
      strcpy(buf2,buf+9);
//      slen=slen-9;
//      strncpy(buf,buf2,slen);
      printf("%s\n\n",buf2);

/*
        pch = strtok (buf2,":");
        while (pch != NULL)
	{
	    char * tmp;
	    char tmp2[100];
	    tmp=pch;
	    while (*tmp!='=') {
		tmp++;
	    }
	    strncpy(tmp2,pch,tmp-pch);
	    tmp2[tmp-pch+1]=0;
	    id[ind]=atoi(tmp2);
	    hodnota[ind]=atof(tmp+1);
//		printf("%d => %4.6f\n", id[ind],hodnota[ind]);
		printf("%d => %s\n", id[ind],tmp+1);
	    ind++;
	    pch = strtok (NULL, ":");
	}
*/
    }

    close(s);
    return 0;
}