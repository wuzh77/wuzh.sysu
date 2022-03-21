#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/shm.h>
#include <fcntl.h>

#include "FIFOqueuestruct.h"

int main(int argc, char *argv[]){
    struct stat fileattr;//file infomation struct
    key_t key;
    int shmid; //shared memory ID
    void *shmptr; //shared memory real address
    struct shared_struct *shared = NULL;//create shared memory
    pid_t childpid1, childpid2;//create child process
    char pathname[80], key_str[10], cmd_str[80];
    
    int shmsize, ret;
    shmsize = QUEUE_SIZE*sizeof(struct shared_struct);//define the size of shared memory
    printf("the max length of the infomation in struct is %d, shm size = %d\n",TEXT_SIZE,shmsize);

    if (argc < 2){
        printf("Error.\n");
        return EXIT_FAILURE;
    }
    strcpy(pathname, argv[1]);

    if (stat(pathname, &fileattr) == -1){ //get the infomation of file.
        ret = creat(pathname, O_RDWR);
        if (ret == -1)
        {
            return EXIT_FAILURE;
        }
        printf("shared file object created.\n");
    }

    key = ftok(pathname, 0x27);
    if (key == -1)
    {
        return EXIT_FAILURE;
    }
    printf("key generated: IPC key = 0x%x\n",key);

    shmid = shmget((key_t)key, shmsize, 0666|PERM);//generate the shared memory

    if (shmid == -1)
    {
        return EXIT_FAILURE;
    }
    printf("shmcon: shmid = %d\n", shmid);
    shmptr = shmat(shmid, 0, 0); //return the virtual base address mapping to the shared memory
    
    if (shmptr == (void *)-1)
    {
        return EXIT_FAILURE;
    }
    printf("\nshmcon: shared Memory attached at %p", shmptr); 
    shared = (struct shared_struct *)shmptr;
    shared->written = 0;//nput the data 
    shared->front = shared->rear = 0;
    shared->flag_write = 0;
    sprintf(cmd_str, "ipcs -m | grep '%d'\n", shmid); 
    printf("\n------ Shared Memory Segments ------\n");
    system(cmd_str);
    sleep(2);

    if(shmdt(shmptr) == -1) {
        return EXIT_FAILURE;
    }
    printf("\nshmcon: shared Memory detached at %p", shmptr);
    printf("\n------ Shared Memory Segments ------\n");
    system(cmd_str);

    sprintf(key_str, "%x", key);
    char *argv1[] = {" ", key_str, 0};
    
    childpid1 = vfork();//create a child process
    if(childpid1 < 0) {//faile to create
        return EXIT_FAILURE;
    } 
    else if (childpid1 == 0) // implement the child process
    {
        execv("/home/wuzhen/下载/alg.8/mywrite", argv1); //call write with IPC key

    }
    else{
        childpid2 = vfork();//create the read process
        if(childpid2 < 0) {
            return EXIT_FAILURE;
        }
        else if (childpid2 == 0) {
            execv("/home/wuzhen/下载/alg.8/myread", argv1); /* call read with IPC key */
        }
        else {
            wait(&childpid1);
            wait(&childpid2);
                 /* shmid can be removed by any process knewn the IPC key */
            if (shmctl(shmid, IPC_RMID, 0) == -1) {
                return EXIT_FAILURE;
            }
            else {
                printf("shmcon: shmid = %d removed \n", shmid);
                printf("\n------ Shared Memory Segments ------\n");
                system(cmd_str);
                printf("\n\n"); 
            }
        }
    }
    
}