

#include <pthread.h>
#include <stdio.h>

  
// maximum number of threads
#define MAX_THREAD 4

#define MAX 100
  
//array declaration and sum of array
int a[100];
int sum[4] = { 0 };
int part = 0;

void* sum_array(void* arg)
{
  
    // Each thread computes sum of 1/4th of array
    int thread_part = part++;
  
    for (int i = thread_part * (MAX / 4); i < (thread_part + 1) * (MAX / 4); i++)
        sum[thread_part] += a[i];
}
  

int main()
{	for (int i=0;i<100;i++){
	a[i]=i+1;
	}
  
  
    pthread_t threads[MAX_THREAD];
  
    // Creating 4 threads
    for (int i = 0; i < MAX_THREAD; i++)
        pthread_create(&threads[i], NULL, sum_array, (void*)NULL);
  
    // joining 4 threads i.e. waiting for all 4 threads to complete
    for (int i = 0; i < MAX_THREAD; i++)
        pthread_join(threads[i], NULL);
  
    // adding sum of all 4 parts
    int total_sum = 0;
    for (int i = 0; i < MAX_THREAD; i++)
        total_sum += sum[i];
  
    printf ("sum is %d \n", total_sum);
  
    return 0;
}
