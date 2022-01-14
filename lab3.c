#include <stdio.h>

int pagenumber(int physical_address,int address_space){
int pageno=physical_address/address_space;
return pageno;
}

int startingaddress(int physical_address,int offset){
int start=physical_address-offset;
return start;
}

int offset(int physical_address,int address_space){
int  ofset=physical_address%address_space;
return ofset;}
void testing_case()
{       int address_space=4096;

	int arr[6] = { 268435700, 4193392,26524 ,32764,1024,32 };
	
	int offsetresult[6]={244,3184,1948,4092,1024,32};
	int starting_address[6]={268435456,4190208,24576,28672,0,0};
	int result_page_number[6]={65536,1023,6,7,0,0};
	for (int i=0;i<6;i++)
		{  int page_no=pagenumber(arr[i],address_space);
		       if (page_no==result_page_number[i])
		       {
			printf("Test case # %d of page number  is passed \n",i+1);
			}
			else
			{printf(" Test case of page bnumber for physical address % d is failed\n",arr[i]);}
		  
		}
	printf("*************************************************************************************\n");
	for (int i=0;i<6;i++)
		{      int ofset=offset(arr[i],address_space);
		       if (offsetresult[i]==ofset)
		       {
			printf("Test case # %d of offset is passed \n",i+1);
			}
			else
			{printf(" Test case of offset for physical address % d is failed\n",arr[i]);}
		  
		}
	printf("*************************************************************************************\n");
	for (int i=0;i<6;i++)
		{  int starting=startingaddress(arr[i],offsetresult[i]);
		       if (starting==starting_address[i])
		       {
			printf("Test case # %d of starting address 0x %X is passed \n",i+1,starting);
			}
			else
			{printf(" Test case of starting address for physical address % d is failed\n",arr[i]);}
		  
		}
	printf("*************************************************************************************\n");
 }
int main()
{
int physical_address=19986;
int address_space=4096;

int pageno=pagenumber(physical_address,address_space);
printf("Page Number :%d \n",pageno);

int ofset=offset(physical_address,address_space);
printf("Offset Number :%d \n",ofset);

int start=startingaddress(physical_address,ofset);
printf("Starting Address :0x %X  \n",start);

testing_case();
}

