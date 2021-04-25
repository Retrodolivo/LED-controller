#include "led.h"

extern TIM_HandleTypeDef htim2;

void pwm_init(void)
{
	HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);
  HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_2);
  HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_3);
	
	TIM2->CCR1 = 0;
	TIM2->CCR2 = 0;
	TIM2->CCR3 = 0;
}

void set_color(Color_t color, float brightness)
{
	TIM2->CCR1 = color.red * brightness;
	TIM2->CCR2 = color.green * brightness;
	TIM2->CCR3 = color.blue * brightness;
}

