#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/shm.h>
#include <fcntl.h>
#include <time.h>
#include <malloc.h>
#include <string.h>
#define TEXT_SIZE 20 // define the massage length of student name
#define QUEUE_LEN 30 // the max numbers of students

#define SHM_SIZE 10000 // define the shared memory size.
#define PERM S_IRUSR | S_IWUSR | IPC_CREAT

typedef struct studen_massage
{
    int flag; // the flag of delete, 0 is delete.
    char name[TEXT_SIZE];
    int number;
} student;

typedef struct myheap
{
    int total_len; // the position of total_len is NULL
    student stu_queue[QUEUE_LEN];
} heap;

void swap_pos(heap *a, int index1, int index2) // exchange the position of student
{
    // create a struct to hold the infomation
    student *temp = (student *)malloc(sizeof(student));
    temp->flag = a->stu_queue[index1].flag;
    strcpy(temp->name, a->stu_queue[index1].name);
    temp->number = a->stu_queue[index1].number;

    a->stu_queue[index1].flag = a->stu_queue[index2].flag;
    strcpy(a->stu_queue[index1].name, a->stu_queue[index2].name);
    a->stu_queue[index1].number = a->stu_queue[index2].number;

    a->stu_queue[index2].flag = temp->flag;
    a->stu_queue[index2].number = temp->number;
    strcpy(a->stu_queue[index2].name, temp->name);
}

void heapUp(heap *a, int index)
{
    if (index > 0) // the heap start from 0
    {
        // the parent of the value
        int parent = index / 2;
        // the value of parent and the index
        int parentNUM = a->stu_queue[parent].number;
        int indexNUM = a->stu_queue[index].number;

        if (parentNUM > indexNUM)
        {
            // exchange the position of index and parent
            swap_pos(a, parent, index);
            heapUp(a, parent);
        }
    }
}

void insert(heap *a, student value)
{
    if (a->total_len >= QUEUE_LEN)
    {
        printf("the heap is full.\n");
        return;
    }

    // add the value to the end of the heap
    a->stu_queue[a->total_len].flag = value.flag;
    a->stu_queue[a->total_len].number = value.number;
    strcpy(a->stu_queue[a->total_len].name, value.name);
    a->total_len++;
    // adjust the heap
    heapUp(a, a->total_len - 1);
}

void delete_value(heap *a, int student_number)
{
    for (int i = 0; i < a->total_len; i++)
    {
        if (a->stu_queue[i].number == student_number)
        {
            a->stu_queue[i].flag = 0;
            break;
        }
    }
}

void adjust(heap *a, int index, int n)
{
    int parent = index;         // the parent index
    int child = parent * 2 + 1; // the child index
    while (child < n)
    {
        if (child + 1 < n && a->stu_queue[child].number > a->stu_queue[child + 1].number)
        {
            child++; // find the minimum of children
        }
        if (a->stu_queue[parent].number > a->stu_queue[child].number)
        {
            swap_pos(a, parent, child); // if parent is greater than child , exchange.
            parent = child;
        }
        child = 2 * child + 1;
    }
}

void buildHeap(heap *a, int size)
{
    for (int i = size / 2 - 1; i >= 0; i--)
    {
        adjust(a, i, size);
    }
}

void HeapSort(heap *a, int size)
{
    printf("Heapsort start.\n");
    buildHeap(a, size); // initial the heap
    for (int i = size - 1; i >= 0; i--)
    {
        swap_pos(a, 0, i);
        adjust(a, 0, i);
    }
    printf("Finish.\n");
}

student *search_Value(heap *a, int studentnum) // find the student according to the student numbers.
{
    for (int i = 0; i < a->total_len; i++)
    {
        if (a->stu_queue[i].flag == 0)
        {
            continue;
        }

        if (a->stu_queue[i].number == studentnum)
        {
            return &a->stu_queue[i];
        }
    }
    return NULL; // if not , return NULL.
}

void display(heap *a)
{
    for (int i = 0; i < a->total_len; i++)
    {
        if (a->stu_queue[i].flag == 0)
        {
            continue;
        }

        printf("student name: %s\tstudent ID: %d\n", a->stu_queue[i].name, a->stu_queue[i].number);
    }
}

int main(int argc, char *argv[])
{
    struct stat fileattr;
    key_t key; // the key of IPC.
    int shmid; // the id of shm
    void *shmptr;
    heap *shared;
    char pathname[80], key_str[10], cmd_str[80];
    int shmsize, ret;
    shmsize = SHM_SIZE; // the size of shm
    printf("the shmsize to create is %d\n.", shmsize);

    if (argc < 2)
    {
        printf("Failure.\n");
        return EXIT_FAILURE;
    }
    strcpy(pathname, argv[1]);

    if (stat(pathname, &fileattr) == -1)
    {
        ret = creat(pathname, O_RDWR);
        if (ret == -1)
        {
            return EXIT_FAILURE;
        }
        printf("shared file object created.\n");
    }

    key = ftok(pathname, 0x27); // generate the key of IPC
    if (key == -1)
    {
        return EXIT_FAILURE;
    }

    printf("key generated :IPC key = 0x%x.\n", key);
    shmid = shmget((key_t)key, shmsize, 0666 | PERM);

    if (shmid == -1)
    {
        printf("create shm failed.\n");
        return EXIT_FAILURE;
    }
    printf("shmcon: shmid = %d.\n", shmid);
    shmptr = shmat(shmid, 0, 0); // returns the virtual base address mapping to the shared memory, *shmaddr=0 decided by kernel

    if (shmptr == (void *)-1)
    {
        return EXIT_FAILURE;
    }
    printf("shm attached at %p.\n", shmptr);
    int *lock = NULL;
    lock = (int *)shmptr; // create the lock to enable there is only one process at the same time
    shared = (heap *)(shmptr + sizeof(int *));
    shared->total_len = 0; // initial the heap
    int *first_sign = NULL;
    int hold = 1;
    first_sign = (int *)(shmptr + sizeof(int *) + sizeof(heap *));
    if (*first_sign == 0)
    {
        *lock = 1; // 1-free, 0-been used
    }
    *first_sign++;
    char c;
    int operator; // -insert , 2-delete , 3-find according studentnumber , 4-Heapsort, 5-show
    while (1)
    {
        printf("if you want to operator shared memory, enter 1,or 0 to exit the process:");
        int ues_sign;
        scanf("%d", &ues_sign);
        c = getchar();
        if (ues_sign == 0)
        {
            break;
        }
        printf("enter the operations you want to do:\n1-instert.\t2-delete.\t3-search student according studentID.\t4-Heapsort.\t5-show the heap.\n");
        scanf("%d", &operator);
        if (operator== 1) // insert student
        {
            printf("enter the name of students you want to insert:");
            char hold_name[TEXT_SIZE];
            scanf("%s", hold_name);
            c = getchar();
            int hold_num;
            printf("enter the ID of student:");
            scanf("%d", &hold_num);
            c = getchar();
            while (*lock == 0)
            {
                printf("the shared memory is been used.\n");
                sleep(1);
            }
            if (*lock == 1)
            {
                *lock = 0;
                student *value_add = (student *)malloc(sizeof(student));
                value_add->flag = 1;
                strcpy(value_add->name, hold_name);
                value_add->number = hold_num;
                insert(shared, *value_add);
                printf("add sucessfully.\n");
            }
        }
        else if (operator== 2) // delete student
        {
            printf("enter the ID of the student you want to delete:");
            int ID;
            scanf("%d", &ID);
            c = getchar();
            while (*lock == 0)
            {
                printf("the shared memory is been used.\n");
                sleep(1);
            }
            if (*lock == 1)
            {
                *lock = 0;
                delete_value(shared, ID);
                printf("delete sucessfully.\n");
            }
        }
        else if (operator== 3) // search student
        {
            printf("enter the ID of student you want to search:");
            int stu_ID;
            scanf("%d", &stu_ID);
            student *found;
            while (*lock == 0)
            {
                printf("the shared memory is been used.\n");
                sleep(1);
            }
            if (*lock == 1)
            {
                *lock = 0;
                found = search_Value(shared, stu_ID);
                if (found)
                {
                    printf("the student has been found:\nstudent name: %s\tstudent ID= %d\n", found->name, found->number);
                }
                else
                {
                    printf("Not found.\n");
                }
            }
        }
        else if (operator== 4)
        {
            while (*lock == 0)
            {
                printf("the shared memory is been used.\n");
                sleep(1);
            }

            if (*lock == 1)
            {
                *lock = 0;
                HeapSort(shared, shared->total_len);
                display(shared);
            }
        }
        else if (operator== 5)
        {
            while (*lock == 0)
            {
                printf("the shared memory is been used.\n");
                sleep(1);
            }
            if (*lock == 1)
            {
                *lock = 0;
                display(shared);
            }
        }
        *lock = 1;
    }
    ret = shmctl(shmid, IPC_RMID, NULL);
    if (ret == 0)
    {
        printf("the shm is destoryed.\n");
    }
    else
    {
        printf("the shm destory failed.\n");
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}