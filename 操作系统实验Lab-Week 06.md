# 操作系统实验Lab-Week 06:



| 专业             | 学号     | 班级     | 姓名 |
| ---------------- | -------- | -------- | ---- |
| 计算机科学与技术 | 20331038 | 计科一班 | 吴镇 |

## 实验内容：

1. 编译运行课件lecture 08例程代码：

   producer-consumer问题的POSIX API应用示例： alg.8-4 ~alg.8-6

2. reader-writer问题的Linux系统调用示例alg.8-1 ~ alg.8-3只处理单个存储节点。修改示例程序将共享空间组织成一个FIFO循环队列(参考数据结构课程相关内容),队列节点具有结构类型(比如：学号，姓名、成绩)，并采用共享内存变量控制队列数据结构同步。



## 代码运行结果展示：

### `alg.8-1-shmcon.c`:

程序运行结果截图：

![2022-03-20 13-53-42 的屏幕截图.png](https://s2.loli.net/2022/03/20/3yWPXmYZNIdwige.png)

argc为整数也就是程序参数的个数，argv[]为一个指针类型的数组，其数组中每一个元素都是指针并且指向了程序的参数。当程序`int main(int argc ,char *argv[])`执行时就会把程序名以及其他参数的个数复制给argc然后通过指针数组中的argv[0]指向了第一个参数也就所谓的程序名。该程序在为输入数据时候，运行结果如上。因为argc<2所以程序直接退出。argc在没有输入数据的时候，其值为1，argc[0]就是这个程序的名字。

在有数据输入的时候，运行结果截图为：

![2022-03-20 14-32-28 的屏幕截图.png](https://s2.loli.net/2022/03/20/qz3fU5uM2IdKomw.png)

可以看到，输入的另一个参数为“123”。该程序首先输出传送数据块数以及共享空间的大小。然后输出argv[0]和argv[1]看看里面包含了什么内容。然后，利用strcpy将argv[1]里面的内容复制到pathname中。

这里简单说明一下`struct stat`和`stat()`函数。

- `int stat(const char *restrict pathname, struct stat *restrict buf)`:

  提供文件名字，获取文件对应的属性。pathname-文件或者文件夹路径，buffer-获取的信息保存在内存中，当正确执行时候，返回值为0，错误时为-1。该函数将参数pathname所制定的文件状态，复制到参数buf中。

- `struct stat` :

  其中包含许多文件对应的属性，例如：设备号码，文件所有者，文件最后被访问的时间等等。

当复制成功之后，将会打印`"shared file object created"`。

之后调用ftok()函数，该函数把一个存在的路径名和一个整数标识符转换成一个key_t值，成为IPC键值。函数原型为`key_t ftok(const char *pathname, int proj_id)`该函数把从pathname中到处的信息和id的低序8位组合成一个整数的IPC键。可以看到，生成的IPC键值为0x2709431a。

接下来调用shmget()函数，该函数介绍如下：

函数原型：`int shmget(key_t  key, size_t  size, int  flag)`

- 函数参数解析：key-标识符的规则；size-共享存储段的字节数；flag-读写权限，成功时返回共享存储的id，失败则返回-1。
- 通过“键”的使用也使得一个IPC对象能为多个进程所共用。

之后打印共享空间的id为32830。

shmat函数用来返回虚拟的共享地址在真实内存中的映射。

shmat函数介绍如下：

- 函数原型：`void *shmat（int shmid，const void *shmaddr,int shmflg）`
- 参数解析：第一个是shmid是shmget返回的共享空间的id，第二个参数一般为0，以便由内和选择地址。，第三个参数若指定了SHM_RDONLY位，则以只读方式连接此段，否则以读写的方式连接次段。该函数返回该段所连接的实际地址，出错则返回-1。

然后程序`shared = (struct shared_struct *)shmptr`用这句话将实际内存地址中的共享空间转化为自定义的数据结构体。并且将共享空间中的结构体中的written标识符置为0，表示这个数据块可以进行写操作。

这里用到了sprintf()函数，这里简单介绍：

函数原型：`int sprintf(char *string, char *format [,argument,...])`

- 函数参数解析：string-指向字符数组的指针，该数组存储了C字符串；format-格式化的字符串；argument-根据语法格式替换format中%标签。
- sprintf是将format指向的字符串从string[0]的位置依次放入（覆盖），当format指向的字符串长度比string字符数组小时，string数组中未被覆盖的值将保持。

这里将共享内存的id以某种形式放入到cmd_str字符串中。

然后调用system()函数，该函数简介如下：

- 函数原型：`int system(const char *command)`。
- system()会调用fork()产生子进程，由子进程来调用/bin/sh-c string来执行参数string字符串所代表的命令，此命令执行完后随即返回原调用的进程。

在这里，system被用来查看共享内存的信息。在终端上可以看到输出：`0x2709431a 32830      wuzhen     666        4100       1` 

之后该共享内存被删除。



当修改了后面读写文件之后，输出结果如下：

![2022-03-20 15-39-07 的屏幕截图.png](https://s2.loli.net/2022/03/20/DuYO4VNdW3vCZ2h.png)

紧接着，程序使用execv函数在一个进程中执行另一个进程。它可以根据指定的文件名或者目录名找到可执行文件，并用它来取代原调用进程的数据段、代码段和堆栈段。函数原型为：`int execv(const char *path, char *const argv[])`

随后产生另一个进程执行`alg.8-2-shmread`，该程序的执行为打印共享空间的IPC、存储空间的ID和共享空间在实际内存的地址，并且该程序会输出在共享内存中的文本数据。

在执行完`alg.8-2-shmread`进程之后，父进程又创建了一个新的进程执行`alg.8-3-shmwrite`。该程序主要是将从键盘外设输入的信息，转到共享缓冲区中，然后写入共享内存中，共享内存保存输入的数据。

最后在执行完全部进程后，将共享空间释放，最后退出。



### `alg.8-2-shmread.c:`

在这个程序中，调用的函数有：

- `int sscanf(const char *str, const char *format,......)`

  说明：该函数会将参数str的字符串根据参数format字符串来转换格式并格式化数据。转换后的结果存于对应的参数内，成功则返回参数树木，失败则返回0。例如：`sscanf("zhoue3456 ", "%4s", str)`则表示将字符串“zhoue3456”中的前四个字符放到str中。

- `int shmget(key_t  key, size_t  size, int  flag)`：

  key-标识符的规则；size-共享存储段的字节数；flag-读写的权限；返回值-成功返回共享存储的ID，失败则返回-1。

- `int strncmp(const char *str1, const char *str2, size_t n)`:

  str1-要进行比较的第一个字符串；str2-要进行比较的第二个字符串；n-要比较的最大字符数。该函数的返回值如下：若返回值<0,则表示str1小于str2;若返回值>0，则表示str2小于str1;若返回值等于0则表示str1等于str2。（根据ASCII比较）

#### 程序运行分析：

该程序将argv[1]中的内容以16进制的形式合成IPC键值，然后利用shmget()函数创建4*1024大小的共享存储空间，并且返回ID到shmid当中。之后`shmptr = shmat(shmid, 0, 0)`返回共享存储空间在内存中的实际地址。随后，程序打印共享存储空间的id和实际地址。随后进入while循环中，当存储空间中的written标识符为0时，该进程就一直睡眠直到标识符改为1。当标识符变为1时，就打印共享存储空间存储的文本字符。最后，当共享存储空间里面的内容为“end”的时候就退出该进程。该程序的主要作用，是读取写进程写进共享存储空间的字符串信息。



### `alg.8-3-shmwrite.c`:

在这个程序中，调用的函数有：

- `int sscanf(const char *str, const char *format,......)`

  说明：该函数会将参数str的字符串根据参数format字符串来转换格式并格式化数据。转换后的结果存于对应的参数内，成功则返回参数树木，失败则返回0。例如：`sscanf("zhoue3456 ", "%4s", str)`则表示将字符串“zhoue3456”中的前四个字符放到str中。

- `int shmget(key_t  key, size_t  size, int  flag)`：

  key-标识符的规则；size-共享存储段的字节数；flag-读写的权限；返回值-成功返回共享存储的ID，失败则返回-1。

- `void *shmat（int shmid，const void *shmaddr,int shmflg）`：

  第一个参数shmid是shmget返回的标识符，第二个参数一般指定为0，以便由内核选择地址。第三个参数如果在flag中指定了SHM_RDONLY位，则以只读方式连接此段，否则以读写的方式连接此
  段。 shmat返回值是该段所连接的实际地址，如果出错返回 -1。

- `char* fgets(char * s, int n,FILE *stream)`：

  第一个参数s指向存储读如数据的缓冲区的地址，n从流中读入n-1个字符stream指向读取的流。若读入成功，则返回缓冲区的地址，若读如错误或者到了结尾，则返回NULL。

- `char *strncpy(char *dest, const char *src, size_t n)`：

  第一个参数dest指向用于村粗复制内容的目标数组，src要复制的字符串,n要从源中复制的字符数组。该函数返回最终复制的字符串。

- `int shmdt(const void *shmaddr)`:

  函数的参数shmaddr为连接的共享内存起始地址。函数用来断开与共享内存附加点的地址，禁止本进程访问次片共享内存。若成功则返回0，否则返回-1。

#### 程序运行分析：

首先，程序先创建一个缓冲区buffer来存储输入的字符串，之后开创一个共享内存，返回的在内存中的实际地址存放在shmid之中。随后打印该共享存储空间的ID和实际地址。随后进入while循环，程序先判断written标识符是否处于可写状态，若不可写则睡眠。随后调用fgets函数将键盘输入的字符串放到缓冲区buffer中。strncpy函数将写入缓冲区的字符转移到共享存储空间中。若读入的字符是“end”则结束。该程序的主要目的是将键盘输入的数据存储进入共享存储空间中。





### `alg.8-5-shmproducer.c`:

在一开始gcc将该代码翻译成为可执行文件的时候，出现如下错误：

![2022-03-20 17-23-15 的屏幕截图.png](https://s2.loli.net/2022/03/20/raPsJoL7plyKUmS.png)

经过查询资料，可知将链接改为gcc -o alg.8-5-shmproducer alg.8-5-shmproducer.c -lrt即可成功。

调用的函数：

- `int shm_open(const char *name, int oflag, mode_t mode)`：

  用于策划部共建或者打开共享内存文件。第一个参数name-要打开或者策划部共建的共享内存文件名，oflag打开的文件操作属性：O_CREAT、O_RDWR、O_EXCL的按位或运算组合；mode文件共享模式，例如 0777。成功则返回大于零的值否则返回-1。

- `void mmap(void *addr, size_t length, int prot, int flags,int fd, off_t offset)`：

  将打开的文件映射到内存，一般是将shm_open打开的文件映射到内存，当然也可以将硬盘上的用open函数打开的文件映射到内存。这个函数只是将文件映射到内存中，使得我们用操作内存指针的方式来操作文件数据。第一个参数addr-要将文件映射到的内存地址，一般应该传递NULL来由Linux内核指定;第二个参数length-要映射的文件数据长度；第三个参数prot-映射的内存区域的操作权限（保护属性），包括PROT_READ、PROT_WRITE、PROT_READ|PROT_WRITE;第四个参数flags-标志位参数，包括：MAP_SHARED、MAP_PRIVATE与MAP_ANONYMOUS。
              MAP_SHARED:  建立共享，用于进程间通信，如果没有这个标志，则别的进程即使能打开文件，也看不到数据。
              MAP_PRIVATE: 只有进程自己用的内存区域
              MAP_ANONYMOUS:匿名映射区

  fg用来建立映射区的文件描述符，用 shm_open打开或者open打开的文件；offset：映射文件相对于文件头的偏移位置，应该按4096字节对齐。返回值，成功返回映射的内存地址指针，可以用这个地址指针对映射的文件内容进行读写操作。

  

#### 程序运行分析：

在这个程序中，要特别注意**shm_open()**函数的用法。在Linux中共享内存是通过tmpfs这个文件系统来实现的，tmpfs文件系统的目录为/dev/shm，这个函数打开或者操作的文件都是位于/dev/shm目录下的，并且该文件不能携带路径。所以在计算机内找到该文件夹，并且在其中创建一个文本文档后，运行该程序截图如下：

![2022-03-20 17-55-40 的屏幕截图.png](https://s2.loli.net/2022/03/20/ExXATD6qGc9tQO8.png)

该程序在Linux的共享内存中打开相应的文件作为分享的信息。之后用mmap()函数，将打开的文件映射到内存之中。然后对mmap返回的指针所指向的内存空间进行操作。在这个程序中`sprintf(shmptr,"%s",message_0)`将message_0中的字符串复制到对应的内存空间中。最后打印复制到内存中的字符串。





### `alg.8-6-shmconsumer.c` :

程序涉及的关键函数与上一个实验大致一样，此处不做讨论。

与上一个实验类似，为了让这个程序运行，首先将一个文本文件（里面包含数字串“123”）放到/dev/shm目录下，然后运行：

![2022-03-20 18-09-27 的屏幕截图.png](https://s2.loli.net/2022/03/20/lDEobJ7gNrLyQ3X.png)

最后该程序打印出来了原来文本文件里面的内容。

#### 程序运行分析：

该程序首先打开/dev/shm文件夹下面的文件然后创建fd文件描述符，然后用mmap()将相应的内存地址返回到shmptr中存储。最后打印在文件里面的字符串。





### `alg.8-4-shmpthreadcon.c`:

该程序调用的函数：

- `int ftruncate(int fd, off_t length)`：

  函数说明：ftruncate()会将参数fd指定的文件大小改为参数length指定的大小。参数fd为已打开的文件描述词，而且必须是以写入模式打开的文件。如果原来的文件件大小比参数length大，则超过的部分会被删去。

- `int wait(int *status)`：

  父进程一旦调用了wait就立即阻塞自己，由wait自动分析是否当前进程的某个子进程已经退出，如果让它找到了这样一个已经变成僵尸的子进程，wait就会收集这个子进程的信息，并把它彻底销毁后返回；如果没有找到这样一个子进程，wait就会一直阻塞在这里，直到有一个出现为止。当父进程忘了用wait()函数等待已终止的子进程时,子进程就会进入一种无父进程的状态,此时子进程就是僵尸进程。wait()要与fork()配套出现,如果在使用fork()之前调用wait(),wait()的返回值则为-1,正常情况下wait()的返回值为子进程的PID。

- `int shm_unlink(const char *name)`：

  参数name-共享内存区的名字，返回值：成功返回0，否则返回-1。该函数删除一个共享内存区对象的名字，删除一个名字仅仅防止后续的 open,mq_open 或 sem_open调用取得成功。

#### 程序运行截图：

![2022-03-20 20-13-03 的屏幕截图.png](https://s2.loli.net/2022/03/20/P8YlIZ9WMDcRzBs.png)

#### 程序运行分析：

首先，程序利用shm_open函数打开文件然后创建fd描述符。之后ftruncate()函数将fd指定的文件大小改为`TEXT_NUM*sizeof(struct shared_struct)`。接着`childpid1 = vfork()`创建子进程。在父进程创建的子进程中，执行`alg.8-5-shmproducer`程序，该进程打印produced message: Hello World!之后就结束。之后又创建另一个子进程`childpid2 = vfork()`。然后子进程`alg.8-6-shmconsumer`执行输出`consumed message: Hello World!`。最后回到父进程中利用wait()函数杀死执行完毕的子进程。在这个过程中，先进行`alg.8-5-shmproducer `在共享内存中写入字符串“Hello World!”，然后`alg.8-6-shmconsumer`又将在共享内存中的字符串输出。在这个过程当中实现了进程间的通信。并且最后调用`shm_unlink()`函数，使得任何一个知道该名字的进程都可以移除这个共享空间。



## 将共享空间组织成优先队列

### FIFOqueuestruct.h文件

该文件主要定义了共享空间的结构体，里面包含了先进先出的循环队列。

代码如下：

```c
#define TEXT_SIZE 20 /* = PAGE_SIZE, size of each message */
#define QUEUE_SIZE 1 //the numbers of struct
#define QUEUE_LEN 20 // the length of FIFOqueue in one shared memory 
struct student_massage {
    char number[20]; // students' id
    char name[20]; // students' name
    char grade[10]; // students' grade
};

//realize the FIFOqueue through list
struct shared_struct {
    int front;//the head of the queue
    int rear;//the end of the queue
    struct student_massage my_queue[QUEUE_LEN]; //the FIFOqueue
    int written; // the queue is writable when written is 0.the queue is readable when the written is 1.
    int flag_write; //the sign to decide whether the write process is working, it's 0 initially.
};


#define PERM S_IRUSR|S_IWUSR|IPC_CREAT


```

`struct student_massage`结构体包含了学生的各种信息。`struct student_massage my_queue[QUEUE_LEN]`是了一个存学生信息结构体的先进先出队列。`int written;`用来控制是读进程对该队列进行操作还是写进程对该队列进行操作。



### mywrite.c(写进程)：

该进程的主要作用是在共享空间中写入若干个学生的基本信息。

```c
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
    key_t key; //define the IPC key of the shared memory

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
```



### myread.c(读进程)：

该程序的主要作用在于读取FIFO队列里面开头的信息。

```c
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
    key_t key; //define the IPC key of the shared memory

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
```



### myshmcon.c(主程序)：

用于创建两个子进程。

```c
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
    key_t key; //define the IPC key of the shared memory

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
```



## 共享空间改为FIFO队列运行结果：

![2022-03-21 22-41-18 的屏幕截图.png](https://s2.loli.net/2022/03/21/N3dDqHlI7rjM6AQ.png)

一开始运行该程序，首先显示共享空间的信息。然后显示了在两个子进程中共享空间的信息。如果要往FIFO队列中加入学生信息，则按下0，否则按下1（在这个程序中，直接按下1会使得进程直接退出结束）。

![2022-03-21 22-45-02 的屏幕截图.png](https://s2.loli.net/2022/03/21/OsMpuS4rkejmZQD.png)

在选择输入两个学生的信息之后，会进入到读进程之中。读进程会首先打印最先进入队列的学生的信息，然后将该学生信息弹出。

![2022-03-21 22-49-37 的屏幕截图.png](https://s2.loli.net/2022/03/21/qoFv32ElUduABcn.png)

当弹出2个学生信息之后，FIFO队列中学生的信息个数为0。若要结束读进程，则按下1，否则按下0。这里按下0。

![2022-03-21 22-51-34 的屏幕截图.png](https://s2.loli.net/2022/03/21/LJIQx4hFBTgMavf.png)

按下0后，会询问是否需要继续往FIFO队列里面继续添加学生信息，若选择继续添加，则会回到写进程往队列添加信息。在选择不继续添加之后，由于队列已经没有元素，故直接退出进程。





## 思考：

在这次实验的改进代码部分，用到了先进先出的循环队列，并且涉及并发进程中共享空间的操作。改进的程序用在结构体内设置了一个标志，当其为1时则一个进程操作，为0时候则另一个进程操作。这个操作，使得两个并发的 进程分开来操作共享空间。当一个在写数据时候，另一个读进程不能读取数据，当读进程进行读操作时候，写进程不能写操作。
