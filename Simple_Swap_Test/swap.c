#include <stdio.h>
#include <string.h>
#include <strings.h>



void swap(int A[], int i, int j)
{
    int temp = 0;

    /*if(strcmp(A, "\0") == 0 )
    {
        printf("Empty Array!\n");
        return;
    }
    else
    {
        
    } */
    if (i == j)
    {
        return;
    }


    if (A[i] != 0)
    {
        if (A[j] == 0)
        {
            temp = A[i];
            A[i] = A[j];
            A[j] = temp;
        }
        else
        {
            swap(A, i, --j);
        }
    }
    else
    {
        swap(A,++i, j);
    }
}


int main(int argc, char const *argv[])
{
    //char A[6] = "BPBPB";
    //A[5] = 0;
    
    //* 0 = Brown amd 1 = Purple
    int A[5] = {0,1,0,1,0};
    //int A[5] = {1,1,0,1,1};


    swap(A, 0, 4);

    printf("Array = A[ ");
    for(int i=0; i < 5; i++)
    {
        if(i != 4)
        {
            printf("%d, ", A[i]);
        }
        else
        {
            printf("%d ]\n", A[i]);
        }
    }

    printf("Finito\n");

    return 0;
}
