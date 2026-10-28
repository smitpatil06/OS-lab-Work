#include<stdio.h>

void main ()
{   
    int A=0;
    printf("enter the howmany of PR,AT,BT:");
    scanf("%d",&A);
    int Pr[A]; 
    int AT[A];
    int BT[A];
    for (int i = 0;i<A;i++)
    {
    printf("enter the value of PR:");
        scanf("%d",Pr[i]);
    printf("enter the value of AT:");
        scanf("%d",AT[i]);
    printf("enter the value of BT:");
        scanf("%d",BT[i]);2
    }
    
}