#include<stdio.h>
#include<wiringPi.h>

// GPIO Number
#define M1_A 7 // 4
#define M1_B 0 // 17
#define M2_A 2 // 27
#define M2_B 3 // 22

#define Motor1 1
#define Motor2 2

#define Dir_STOP 0 // Stop
#define Dir_Forward 1
#define Dir_Backward 2

void runMotor(int motor, int direction);

int main(void)
{
	int data;
	if(wiringPiSetup () == -1)
		return 1;

	pinMode(M1_A, OUTPUT);
	pinMode(M1_B, OUTPUT);
	pinMode(M2_A, OUTPUT);
	pinMode(M2_B, OUTPUT);

	while(1)
	{
		printf("Press Key, you can I:Forward, J:Left, L:Right, ,:Rear, K:Stop\n");
		scanf("%c", &data);
		if(data == ',')
		{
			printf("Rear\n");
			runMotor( Motor1, Dir_Forward );
                        runMotor( Motor2, Dir_Forward );
		}
		else if(data == 'i' || data == 'I')
		{
			printf("Front\n");
			runMotor( Motor1, Dir_Backward );
                        runMotor( Motor2, Dir_Backward );
		}
		else if(data == 'j' || data == 'J')
		{
			printf("Left\n");
			runMotor( Motor1, Dir_Forward );
		}
		else if(data == 'l' || data == 'L')
		{
			printf("Right\n");
			runMotor( Motor2, Dir_Forward );
		}
		else if(data == 'k' || data == 'K')
		{
			printf("Stoped\n");
			runMotor( Motor1, Dir_STOP );
			runMotor( Motor2, Dir_STOP );
		}
	}
	return 0;
}

// If you need more motor, add this case section.
void runMotor(int motor, int direction)
{
	switch (motor){
		case Motor1:
			if ( direction == Dir_Forward )
			{
				digitalWrite(M1_A, 0);
				digitalWrite(M1_B, 0);
				usleep(300);
				digitalWrite(M1_A, 1);
				digitalWrite(M1_B, 0);
			}
			else if( direction == Dir_Backward )
			{
				digitalWrite(M1_A, 0);
				digitalWrite(M1_B, 0);
				usleep(300);
				digitalWrite(M1_A, 0);
				digitalWrite(M1_B, 1);
			}
			else
			{
				digitalWrite(M1_A, 0);
				digitalWrite(M1_B, 0);
			}
			break;
		case Motor2:
			if ( direction == Dir_Forward )
			{
				digitalWrite(M2_A, 0);
				digitalWrite(M2_B, 0);
				usleep(300);
				digitalWrite(M2_A, 1);
				digitalWrite(M2_B, 0);
			}
			else if( direction == Dir_Backward )
			{
				digitalWrite(M2_A, 0);
				digitalWrite(M2_B, 0);
				usleep(300);
				digitalWrite(M2_A, 0);
				digitalWrite(M2_B, 1);
			}
			else
			{
				digitalWrite(M2_A, 0);
				digitalWrite(M2_B, 0);
			}
			break;
		default:
			break;
	}
}
