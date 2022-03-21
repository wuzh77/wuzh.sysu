#define TEXT_SIZE 20 /* = PAGE_SIZE, size of each message  */
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

