#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#define BUF_SIZE 2000
 
int main(int argc, char* argv[]) {
int input_fd;
    ssize_t ret_in; /* Number of bytes returned by read()  */
    char buffer[BUF_SIZE];      /* Character buffer */
    char *word; /*pointer to point a single word*/
    char *ptr;  /*pointer to point a line */
    char *replica;
    char *next; /*pointer that contains value literals after token*/
    char currentline[500]; /*To save the whole curent line and not to be modified in strtok for words*/
    char *words;
    char wordend[]=" ";/*delimiter for words*/
    /* Are src and dest file name arguments missing */
    if(argc != 3){
        printf ("Usage: find string file1");
        return 1;
    }
 
    /* Create input file descriptor */
    input_fd = open (argv [2], O_RDONLY);
    if (input_fd == -1) {
            perror ("open");
            return 2;
    }
    char delim[] = "\n";
    int result=-1;
    //While loop continues if there is a data in file 
    while((ret_in = read (input_fd, &buffer, BUF_SIZE)) > 0)
    {   
        //next will have the whole line in the buffer
	next=strtok(buffer, delim);
	//loop continues until there is a line in file.
	while(next != NULL)
	{	//this will also point to that line for furthur proceedings
	        ptr=next; 
	       
	        //saves the current value of line in current line
	        strcpy(currentline,next);	
               // the value after token was in NULL and copied until delimiter
               //in next 
	       next = strtok(NULL, delim);
	       //word will have only the words of ltne one by one
		word=strtok(ptr,wordend);
		while(word != NULL)
		{      //comparing the word we are finding 
			if((result = strcmp(word, argv[1])==0))
			{ printf("There is a match in the line. \n '%s'\n",
			currentline);
				}
			word = strtok(NULL, wordend);
		}
		
	      
	}

       
     }

    close (input_fd);
    return (EXIT_SUCCESS);
}
