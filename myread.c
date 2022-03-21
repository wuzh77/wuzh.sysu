#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string.h>
#include <sys/shm.h>
#include "FIFOqueuestruct.h"

int main(int argc, char *argv[])
{
    void *shmptr = NULL; //define the  shared memory ptr
    struct shared_struct *shared;
    int shmid; //define the id of shared memory 
    key_t key;
    //if the argc==1 exit the program
    if(argc < 2){
        printf("exit program\n");
        EXIT_FAILURE;
    }
    //generate the IPC key of the shared memory
    sscanf(argv[1], "%x",&key);
    printf("%*sshmread: IPC key = 0x%x\n", 30, " ", key);
    //create the shared memory and generate the id of the shared memory
    shmid = shmget((key_t)key,QUEUE_SIZE*sizeof(struct shared_struct),0666|PERM);
    if (shmid == -1) {
        printf("create the shared memory faild.\n");
        return EXIT_FAILURE;
    }
    shmptr = shmat(shmid, 0, 0);
    if (shmptr == (void *)-1)
    {
        return EXIT_FAILURE;
    }
    //print the infomation of the shared memory
    printf("%*sshmread: shmid = %d\n", 30, " ", shmid);    
    printf("%*sshmread: shared memory attached at %p\n", 30, " ", shmptr);
    printf("%*sshmread process ready ...\n", 30, " ");
    // shared is the FIFOqueue
    shared = (struct shared_struct *)shmptr;
    while (1) {
        while (shared->written == 0) {
            sleep(1); /* message not ready, waiting ... */
        }
        if (shared->front == shared->rear && shared->flag_write)
        {
            printf("the write process is not working,also the queue is empty.EXIT\n");
            break;
        }
        
        printf("the head of the queue is :\n");
        printf("student name: %s; ID: %s; grade: %s.\n",shared->my_queue[shared->front].name,shared->my_queue[shared->front].number,shared->my_queue[shared->front].grade);
        shared->front = (shared->front + 1)%QUEUE_LEN;
        int flag = 0;
        if (shared->front == shared->rear)
        {
            printf("the queue is empty,you should input some data in it.\n");
            shared->written = 0;
            continue;
        }
        else{
        printf("if you want to continue to get the front node , press 1,or press 0:");
        scanf("%d",&flag);
        while (shared->rear != shared->front && flag)
        {
            printf("student name: %s; ID: %s; grade: %s.\n",shared->my_queue[shared->front].name,shared->my_queue[shared->front].number,shared->my_queue[shared->front].grade);
            flag = 0;
            shared->front = (shared->front + 1)%QUEUE_LEN;
            if (shared->rear != shared->front) {
            printf("if you want to continue to get the front node , press 1,or press 0:");
            scanf("%d",&flag);
            }
        }
        }
        if (shared->front == shared->rear){
            printf("the queue is empty.\n");
            int exit_read;
            printf("if you want to exit the process press 1,or press 0:");
            scanf("%d",&exit_read);
            if (!exit_read)
            {
                shared->written = 0;
                continue;
            }
            
            break;
        }
        shared->written = 0;
        
    } /* it is not reliable to use shared->written for process synchronization */

    if (shmdt(shmptr) == -1) {
        return EXIT_FAILURE;
    }
    
    exit(EXIT_SUCCESS);
     
}