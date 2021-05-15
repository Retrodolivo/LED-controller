#include "bluetooth.h"

extern Color_t color_rx;
extern UART_HandleTypeDef huart1;

enum Current_color
{
	Red, Green, Blue
} current_color;

extern float brightness_temp;

void BT_listen(UART_HandleTypeDef *huart1, bluetooth_t *bt)
{
	HAL_UART_Receive_IT(huart1, (uint8_t*)bt->rx_data, 1);
}

void bt_rx_parse(bluetooth_t *bt)
{
	if(bt->rx_data[0] >= '0' && bt->rx_data[0] <= '9')
	{
		bt->buff[bt->rx_len] = bt->rx_data[0];
		bt->rx_len++;			
	}
	if(bt->rx_data[0] == 'N')
	{
		color_rx.brightness = brightness_temp;
		set_color(color_rx);
	}
	if(bt->rx_data[0] == 'F')
	{
		color_rx.brightness = 0;
		set_color(color_rx);
	}
	if(bt->rx_data[0] == '.' || (bt->rx_data[0] == ')' && current_color == Blue))
	{
		switch(current_color)
		{
			case Red:
				for(uint8_t j = bt->rx_len; j != 0; j--)
				{
					if(j == 3)
						color_rx.red += (bt->buff[bt->rx_len - j] - '0') * 100;
					if(j == 2)
						color_rx.red += (bt->buff[bt->rx_len - j] - '0') * 10;
					if(j == 1)
						color_rx.red += bt->buff[bt->rx_len - j] - '0';	
				}
				bt->rx_len = 0;
				current_color = Green;
				break;
				
			case Green:
				for(uint8_t j = bt->rx_len; j != 0; j--)
				{
					if(j == 3)
						color_rx.green += (bt->buff[bt->rx_len - j] - '0') * 100;
					if(j == 2)
						color_rx.green += (bt->buff[bt->rx_len - j] - '0') * 10;
					if(j == 1)
						color_rx.green += bt->buff[bt->rx_len - j] - '0';	
				}
				bt->rx_len = 0;
				current_color = Blue;
				break;
				
			case Blue:
				for(uint8_t j = bt->rx_len; j != 0; j--)
				{
					if(j == 3)
						color_rx.blue += (bt->buff[bt->rx_len - j] - '0') * 100;
					if(j == 2)
						color_rx.blue += (bt->buff[bt->rx_len - j] - '0') * 10;
					if(j == 1)
						color_rx.blue += bt->buff[bt->rx_len - j] - '0';	
				}
				set_color(color_rx);
				color_rx.red = color_rx.green = color_rx.blue = 0;
				bt->rx_len = 0;
				current_color = Red;
				break;
		}
	}			
	BT_listen(&huart1, bt);
}

