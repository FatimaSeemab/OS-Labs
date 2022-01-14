#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
int main()
{ 
  int p1[2];//Child to Parent
  int p2[2];//Parent to Child
  char buffer[200]="Hello World";
  if (pipe(p1) == -1){return 1;}
  if (pipe(p2) == -1){return 1;}

  int pid=fork();
  if (pid == -1){return 2;}

  if(pid==0){
      //Child Process
     close(p1[0]);
     close(p2[1]);
     if (read(p2[0],buffer,sizeof(buffer))==-1)
     {return 4;}
     printf("data recieved by child is %s \n",buffer);
    
     strncpy(buffer,"hi, whats up",200);
    //  printf("buffer is %s",buffer);
     if (write(p1[1],buffer,sizeof(buffer))==-1)
     {return 5;}
     printf("data send to parent is %s \n",buffer);
     close(p1[1]);
     close(p2[0]);
  }

    else{
     //Parent Process   
     close(p1[1]);
     close(p2[0]);
     if(write(p2[1],buffer,sizeof(buffer))==-1)
     {return 6;}
     printf("data send to child is %s \n",buffer);
     if (read(p1[0],buffer,sizeof(buffer))==-1)
     {return 7;}
     printf("data recieved by parent is %s \n",buffer);
     close(p1[0]);
     close(p2[1]);
    }
return -1;







}