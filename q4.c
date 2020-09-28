#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<sys/wait.h>
#include<signal.h>
#include<string.h>

void Ler_Pipe(int fd)
{
    int i;
    char mensagem[200];
    i = -1;
    do{
        i++;
        read(fd,mensagem+i,1);
    }while(mensagem[i]!='\0');
    printf("%s",mensagem);
    usleep(1000);
    printf("nova linha adicionada");
}
int main()
{
    int pid[2];
    int fd[2];
    //Cria o Pipe
    pipe(fd);
    //Cria o processo
    pid[0] = fork();
    if(pid[0]==0)
    {
        //Codigo do primeiro filho
        Escreve_Pipe(fd[1],"FILHO1: Quando o vento passa, é a bandeira que se move.\n");
    }
    else
    {
        //Codigo do pai, após o primeiro
        //filho ser criado
        pid[1] = fork();
        if(pid[1]==0)
        {
            //Codigo do segundo filho
            Ler_Pipe(fd[0]);
            Escreve_Pipe(fd[1],"FILHO2: Não, é o vento que se move.\n");
        }
        else
        {

            //Codigo do pai, após o segundo
            //filho ser criado
            //Espera os filhos se comunicarem
            usleep(10000);
            Ler_Pipe(fd[0]);
            puts("PAI: Os dois se enganam. É a mente dos senhores que se move.");

        }
    }
    return 0;
}
