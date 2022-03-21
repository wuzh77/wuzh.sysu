#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string.h>
#include <sys/shm.h>
#include "FIFOqueuestruct.h"


int main(int argc, char *argv[])
{
    void *shmptr = NULL; //define the ptr of shared memory
    struct shared_struct *shared = NULL; //define the shared memory 
    int shmid; //define the id of shared memory
    key_t key; //define the IPC ke y of the shared memory

    sscanf(argv[1], "%x", &key); //create IPC key ()
    printf("shmwrite: IPC key = 0x%x\n",key); //print the IPC key to check if it is the same

    shmid = shmget((key_t)key, QUEUE_SIZE*sizeof(struct shared_struct),0666|PERM); //get the shared memory ID
    if (shmid == -1){
        return EXIT_FAILURE; // if it fails to create ,exit
    }
    shmptr = shmat(shmid, 0, 0); //get the ptr of the shared memory in real memory
    if (shmptr == (void *)-1){
        return EXIT_FAILURE;//if fail to get the position ,exit
    }
    printf("shmwrite: shmid = %d;  shared memory attached at %p\n",shmid, shmptr);
    //print the id and real memory position
    printf("the write process is working.\n");

    shared = (struct shared_struct *) shmptr; //generate the shared memory
    
    while (1) {
        while (shared->written == 1) //if written==1 turn to read process
        {
            sleep(1);
        }
        int exit_flag = 0; //the flag to decide whether to add node
        printf("if you want to add node in queue please press 0, or 1:");
        scanf("%d",&exit_flag); 
        if (exit_flag)
        {
            if (shared->front != shared->rear)
            {
                printf("you are going to read process.\n");
                shared->written = 1;
                continue; // go to the read memory
            }
            else{
                printf("the queue is empty,exit the process automatically.\n");
                shared->written = 1;
                shared->flag_write = 1;
                exit(EXIT_SUCCESS); // exit the process sucessfully
            }
        }
        char c; //to get the \n
        int num_student; // the numbers of students added to the queue
        printf("enter the numbers of student you want to add :");
        scanf("%d",&num_student);
        c = getchar();
        while (num_student--){ //enter the infomation of student.
        printf("Enter the infomation of the student:\n");
        printf("student name:");
        scanf("%s",shared->my_queue[shared->rear].name);
        c = getchar();
        printf("student grade:");
        scanf("%s",shared->my_queue[shared->rear].grade);
        c = getchar();
        printf("student ID:");
        scanf("%s",shared->my_queue[shared->rear].number);
        shared->rear = (shared->rear + 1)%QUEUE_LEN;
        }
        shared->written = 1; //it's read process 
        if (shared->rear == shared->front) {
            int exit_write;
            printf("the queue is empty,if you want to exit,press 1,or 0:"); 
            scanf("%d",&exit_write);
            if (!exit_write)
            {
                continue;
            }
            
            break;
        }
    }

    if (shmdt(shmptr) == -1) {
        return EXIT_FAILURE;
    }

    exit(EXIT_SUCCESS);
    
}