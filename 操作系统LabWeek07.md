# 操作系统LabWeek07

| 班级     | 姓名 | 学号     |
| -------- | ---- | -------- |
| 计科一班 | 吴镇 | 20331038 |



## 测试M的容量上限：

测试代码如下：

```python
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/shm.h>
#include <fcntl.h>

#define Max_Test_size 30000000000
#define PERM S_IRUSR | S_IWUSR | IPC_CREAT

int main(int argc, char *argv[])
{
    struct stat fileattr;
    key_t key;
    void *shmptr;
    int ret;
    long long int shmsize;
    printf("the shm size = %ld.\n", Max_Test_size);
    char pathname[80], key_str[80];
    if (argc < 2)
    {
        printf("Usage: ./a.out pathname\n");
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

    key = ftok(pathname, 0x27);
    if (key == -1)
    {
        return EXIT_FAILURE;
    }
    printf("key generated : IPC key = 0x%x.\n", key);
    shmsize = Max_Test_size;
    int shmid = shmget((key_t)key, shmsize, 0666 | PERM);

    while (shmid == -1)
    {
        printf("shm create fail.\nthe shmsize = %lld\n", shmsize);
        shmsize -= 1000;
        shmid = shmget((key_t)key, shmsize, 0666 | PERM);
    }

    printf("shmid = %d\n", shmid);

    shmptr = shmat(shmid, 0, 0);

    if (shmptr == (void *)-1)
    {
        return EXIT_FAILURE;
    }
    printf("\nshmcon: shared Memory attached at %p", shmptr);
    ret = shmctl(shmid, IPC_RMID, NULL);
    if (ret == 0)
    {
        printf("delete shm successfully.\n");
    }
    else
    {
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
```

在测试之前，先用ipcs -l指令查看LInux系统共享内存相关信息，查询结果如下：

![2022-03-27 19-40-53 的屏幕截图.png](https://s2.loli.net/2022/03/27/zmyBQ7k493NdUiJ.png)

可以看到，最大段数为4096，最大段大小为2的64次方大小。

再用ipcs -m来查看共享内存段被占用情况：

![2022-03-27 17-36-33 的屏幕截图.png](https://s2.loli.net/2022/03/27/ONkRos53rHU7lBh.png)

在上面的程序中创建了一定大小的共享空间。首先设置需要创建的空间的大小为：`#define Max_Test_size 30000000000`然后，通过ftok函数生成键值，每一个共享存储段都有一个对应的键值。然后通过调用shmget函数创建共享存储空间并返回一个共享存储标识符。shmget函数的函数原型为` int shmget(key_t key, size_t size,int flag);`其中，key是ftok生成的键值，size为共享内存的大小，以字节为单位，flag为操作权限。若该函数创建成功，则返回共享空间的ID，出错则返回-1。在上面的程序中，

```c
while (shmid == -1)
    {
        printf("shm create fail.\nthe shmsize = %lld\n", shmsize);
        shmsize -= 1000;
        shmid = shmget((key_t)key, shmsize, 0666 | PERM);
    }
```

该while循环的作用是：当shmget创建共享空间失败时候，就会减小创建空间的大小，直到创建完成就会退出该循环。创建成功后，用shmat函数获取第一个可用的共享内存空间的地址，最后通过shmctl函数 `ret = shmctl(shmid, IPC_RMID, NULL);`对创建的共享空间进行销毁。最后该程序的运行截图如下：

![2022-03-27 19-37-38 的屏幕截图.png](https://s2.loli.net/2022/03/27/z6vHEm87O4oyaXF.png)



## 在M上建立一个二元小顶堆：

## myheap.h文件：

学生信息结构体：

```c
typedef struct studen_massage
{
    int flag; // the flag of delete, 0 is delete.
    char name[TEXT_SIZE];
    int number;
} student;
```

这里的flag表示该节点是否被删除，若该节点已经被去除，则为0，否则为1。



小顶堆结构体：

```c
typedef struct myheap
{
    int total_len; // the position of total_len is NULL
    student stu_queue[QUEUE_LEN];
} heap;
```

total_len是整个小顶堆元素的个数，并且在stu_queue[total_len]上，没有元素。



交换元素函数：

```c
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
```



对插入节点的位置进行调整：

```c
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
```

这个小顶堆从0开始，如果小顶堆的大小为0，则直接加入元素。parent得到插入节点的父亲节点，将父亲节点的值和子结点进行比较，若父节点比较大，则交换父节点和子结点的位置，让学生学号小的往上浮。



插入节点：

```c
void insert(heap *a, student value)
{
    // add the value to the end of the heap
    a->stu_queue[a->total_len].flag = value.flag;
    a->stu_queue[a->total_len].number = value.number;
    strcpy(a->stu_queue[a->total_len].name, value.name);
    a->total_len++;
    // adjust the heap
    heapUp(a, a->total_len - 1);
}
```

这个函数的作用是在堆的末尾插入元素。



删除学生节点：

```c
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
```

此处直接将学生结构体里面的flag置为0，表示被删除。



### createshmop.c：

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/shm.h>
#include <fcntl.h>

#include "myheap.h"

#define SHM_SIZE 10000
#define PERM S_IRUSR | S_IWUSR | IPC_CREAT

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
    int *lock;
    lock = (int *)shmptr; // create the lock to enable there is only one process at the same time
    int sign = 1;
    lock = &sign;
    shared = (heap *)(shmptr + sizeof(int *));
    shared->total_len = 0; // initial the heap

    printf("heap has been created.\n");
    printf("enter the numbers of students you want to add:");
    int number_student; // the numbers of student added
    scanf("%d", &number_student);
    char c;
    c = getchar();
    while (number_student--)
    {
        student *value_add = (student *)malloc(sizeof(student));
        value_add->flag = 1;
        printf("enter the name of student:");
        scanf("%s", value_add->name);
        c = getchar();
        printf("enter the ID of student :");
        scanf("%d", &value_add->number);
        c = getchar();
        insert(shared, *value_add);
    }
    printf("the min heap has been created.\n");
    display(shared);
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
```

在上面的程序中：

```c
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
```

这段代码创建了共享空间，大小为10000字节。

然后根据要求，在共享空间中创建lock使得每次只有一个进程使用共享空间。

```c
	int *lock;
    lock = (int *)shmptr; // create the lock to enable there is only one process at the same time
    int sign = 1;
    lock = &sign;
    shared = (heap *)(shmptr + sizeof(int *));
```



```c
	int number_student; // the numbers of student added
    scanf("%d", &number_student);
    char c;
    c = getchar();
    while (number_student--)
    {
        student *value_add = (student *)malloc(sizeof(student));
        value_add->flag = 1;
        printf("enter the name of student:");
        scanf("%s", value_add->name);
        c = getchar();
        printf("enter the ID of student :");
        scanf("%d", &value_add->number);
        c = getchar();
        insert(shared, *value_add);
    }
```

这个代码段的主要作用在于将学生的信息输入堆中。在这里采用一边插入一边排序的方法。



最后进行销毁：

```c
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
```



运行结果截图：

![2022-03-28 14-30-10 的屏幕截图.png](https://s2.loli.net/2022/03/28/CMvLqpB95dW1IVz.png)

这里构建的是小顶堆，学生学号比较小的会被分配到前面。



## 对上述结构的节点实现插入、删除、修改等操作，以及多终端并发执行

在这段代码中，进行并发执行的逻辑是：

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/shm.h>
#include <fcntl.h>
#include <time.h>

#include "myheap.h"

#define SHM_SIZE 10000
#define PERM S_IRUSR | S_IWUSR | IPC_CREAT

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
            scanf("%d", &hold_num);
            c = getchar();
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
        else if (operator== 4) // Heapsort
        {
            if (*lock == 1)
            {
                *lock = 0;
                HeapSort(shared, shared->total_len);
                display(shared);
            }
        }
        else if (operator== 5)
        {
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
```



```c
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
```

这一部分代码主要在于通过Linux系统调用创建共享空间。之后在共享空间中设置lock标志，当lock=1时则表示shared memory目前没有任何进程在对其进行操作，当lock=0时候，则表示当前共享空间处于被占用状态。

`int operator; // -insert , 2-delete , 3-find according studentnumber , 4-Heapsort, 5-show`

这里定义了一个操作标识符，可以输入相应的数字进行相应的操作。



#### 当输入为1时，进行插入操作：

关键代码：

```c
			printf("enter the name of students you want to insert:");
            char hold_name[TEXT_SIZE];
            scanf("%s", hold_name);
            c = getchar();
            int hold_num;
            scanf("%d", &hold_num);
            c = getchar();
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
```

这里一次插入一个学生类结构体，并且在插入的时候进行排序。



#### 当输入为2时，进行删除操作：

```c
			printf("enter the ID of the student you want to delete:");
            int ID;
            scanf("%d", &ID);
            c = getchar();
            if (*lock == 1)
            {
                *lock = 0;
                delete_value(shared, ID);
                printf("delete sucessfully.\n");
            }
```

在这里进行删除操作，直接将学生结构体里面的flag置为0，表示删除操作。



#### 当输入为3时，进行查找操作：

```c
			printf("enter the ID of student you want to search:");
            int stu_ID;
            scanf("%d", &stu_ID);
            student *found;
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
```

在这里根据学生的学号进行查找，查找成功就返回对应结构体，失败则打印失败。



#### 当输入为4时，进行堆排序：

```c
				*lock = 0;
                HeapSort(shared, shared->total_len);
                display(shared);
```

这里建立的是最小堆，所以在排序时候最终结果是降序的。



#### 当输入为5时，显示打印堆里面的元素：

```c
*lock = 0;
display(shared);
```



#### 当进程执行完毕时候，就自动删除该共享内存：

```c
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
```



#### 堆调整代码段：

```c
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
```

在这里建立最小堆，当子结点比较父节点小的时候，就和父节点进行交换，并且向下调整。



#### 建立小顶堆：

```c
void buildHeap(heap *a, int size)
{
    for (int i = size / 2 - 1; i >= 0; i--)
    {
        adjust(a, i, size);
    }
}
```

从最后一个父亲节点开始调整。



#### 进行堆排序：

```c
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
```

排序完成之后，列表中节点是根据学号大小降序排列。



#### 根据对应学号查找学生：

```c
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
```

查找成功则返回对应学生的结构体。



#### 从头开始打印列表信息：

```c
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
```

这里对于flag=0也就是被删除的节点，直接跳过不打印。



### 程序运行截图及分析：

![2022-03-30 14-57-00 的屏幕截图.png](https://s2.loli.net/2022/03/30/hqftnxLlAjCFaBz.png)

这里只用两个终端执行同一个进程来演示。程序运行开始时候，先打印共享空间的大小、IPC键值、共享空间的ID和共享空间在实际内存中的第一个地址。然后就到了选择需要的操作。

在左边的终端中选择插入操作，这里连续插入了两个学生的信息。当左边进程插入完毕之后，右边进程根据学生的ID进行学生的查询操作，查找成功时候就返回学生的信息。紧接着就打印堆中所有学生。再插入一个学生然后进行堆排序。排序完后，再在左边的终端打印信息，可以发现学号是从小到大排列。



在这次实验中，当lock的值为0时候，就表示共享空间已经有进程在使用，；当lock的值为1的时候，表示共享空间此时无进程使用，表示处于可用状态。为了更好地体现并发性，这里是将终端中的进程真正需要访问共享空间或者需要对其进行改变的时候，才会让该终端中的进程获取共享空间的操作权。而在进程在真正需要进行操作共享内存时候，会首先将lock置为0，完成操作之后就置为1。

例如，当多个终端同时运行这个代码时候，设其中一个终端运行的进程A需要进行插入操作（增加节点），在A进行学生信息输入的时候，进程会创建临时的变量来存储那些输入的信息，在完全输入之后，该进程才可以访问空间，对共享空间进行修改。在这个A进行输入的过程中，除进程A以外的其他终端内运行的进程，可以进行其他操作例如删除、查找等。也就是说，在输入信息的时候，该进程是没有占有共享空间。这里主要将进程的输入信息时间和真正需要操作共享内存的时间区分开来，在输入信息的时候，就将共享空间使用权空出来，给有需要的进程。在这种情况下，当多个终端并发执行该进程的时候，在其中一个终端上操作时候就可以看成共享空间被其“占用”。



## 思考：

使用逻辑值lock实现的并发机制不能彻底解决访问冲突问题：

这里还需要考虑特殊情况，当一个终端上的进程输入想要进行的操作后，这个操作需要访问共享内存较长时间，当这个时侯其他终端也输入完毕想要访问空间时候，因为共享内存中的lock=0（处于占用状态），所以不能访问，就会处于等待的状态，直到共享空间解锁。这里就利用了lock标识符的功能，使共享空间每次仅有一个进程对其进行操作。

还有一种极端情况，当两个终端同时需要进行共享空间的访问时候，这时候就会产生冲突，到底哪个终端中的进程会首先将lock的值修改为0表示占有，这个问题是lock实现的并发机制不能彻底解决访问冲突问题。
