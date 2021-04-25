#ifndef _LED_H_
#define _LED_H_

#include "main.h"

typedef struct
{
	uint8_t red, green, blue;	
} Color_t;


void pwm_init(void);
void set_color(Color_t color, float brightness);

#endif /*_LED_H_*/
