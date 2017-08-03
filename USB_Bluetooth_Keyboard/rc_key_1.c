#include<stdio.h>
#include<wiringPi.h>

#define M1_L 7 // 4
#define M1_R 0 // 17
#define M2_F 2 // 27
#define M2_R 3 // 22

int main(void)
{
	int data;
	if(wiringPiSetup () == -1)
		return 1;

	pinMode(M1_L, OUTPUT);
	pinMode(M1_R, OUTPUT);
	pinMode(M2_F, OUTPUT);
	pinMode(M2_R, OUTPUT);

	while(1)
	{
		scanf("%c", &data);
		if(data == 'q' || data == 'Q')
		{
			digitalWrite(M1_R, 0);
			digitalWrite(M1_L, 1);
			printf("M1_Left M1_R = 0, M1_L = 1\n");
		}
		else if(data == 'a' || data == 'A')
		{
			digitalWrite(M1_L, 0);
			digitalWrite(M1_R, 1);
			printf("M1_Right M1_L = 0 M1_R = 1\n");
		}

		if(data == 'w' || data == 'W')
		{
			digitalWrite(M2_R, 0);
			digitalWrite(M2_F, 1);
			printf("M2_Forward M2_R = 0, M2_F = 1\n");
		}
		else if(data == 's' || data == 'S')
		{
			digitalWrite(M2_F, 0);
			digitalWrite(M2_R, 1);
			printf("M1_Reverse M2_F = 0, M2_R = 1\n");
		}
	}
	return 0;
}

