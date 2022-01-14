#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#define BUF_SIZE 2000
 
int main(int argc, char** argv) {
int input_fd,input_fd2;
    ssize_t ret_in; /* Number of bytes returned by read()  */
    char buffer[BUF_SIZE];      /* Character buffer */
    char buffer2[BUF_SIZE];
    int counter=0;
    char *next; /*pointer that contains value literals after token*/
    /* Are src and dest file name arguments missing */
    if(argc != 4){
        printf ("Usage: find string file1");
        return 1;
    }
    
    if(*argv[1]!='n')
    {printf("hiii n is not there");
        return 3;}
    /* Create input file descriptor */
    input_fd = open (argv [3], O_RDONLY);
    if (input_fd == -1) {
            perror ("open");
            return 2;
    }
    char delim[] = "\n";
    // int result=-1;
    // //While loop continues if there is a data in file 
    while((ret_in = read (input_fd, &buffer, BUF_SIZE)) > 0)
    {   
        //next will have the whole line in the buffer
	next=strtok(buffer, delim);
	//loop continues until there is a line in file.
	while(next != NULL)
	{	//this will also point to that line for furthur proceedings
            counter++;
	        //printf("line is %s \n",next);	
	       next = strtok(NULL, delim);
	}
    }
  
    int index=counter-atoi(argv[2]);
 
    input_fd= open (argv [3], O_RDONLY);
    // // close (input_fd);
    counter=0;
    while((ret_in = read (input_fd, &buffer2, BUF_SIZE)) > 0)
    {
        //next will have the whole line in the buffer
        next=strtok(buffer2, delim);
 
	//loop continues until there is a line in file.

	while(next != NULL)
	{
	        
            counter++;
            if (counter>=index)
	        {printf("%s \n",next);}
	       next = strtok(NULL, delim);
	}
    }
     return (EXIT_SUCCESS);
}
