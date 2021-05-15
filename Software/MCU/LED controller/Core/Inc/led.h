#ifndef _LED_H_
#define _LED_H_

#include "main.h"

typedef struct
{
	uint8_t red, green, blue;
	float brightness;
} Color_t;


void pwm_init(void);
void set_color(Color_t color);

#endif /*_LED_H_*/
