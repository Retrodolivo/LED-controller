#include "bluetooth.h"

extern Color_t color_rx;
extern UART_HandleTypeDef huart1;

enum Current_color
{
	Red, Green, Blue
} current_color;


extern float brightness_temp;

/*
	Enable UART interrupt upon every received byte
*/
void BT_listen(UART_HandleTypeDef *huart1, bluetooth_t *bt)
{
	HAL_UART_Receive_IT(huart1, (uint8_t*)bt->rx_data, 1);
}
/*
	list of bluetooth commands:
	"ON)" - turn on the leds
	"OFF)" - turn of the leds
	"x.x.x)" - set color; x - decimal code RGB[0 .. 255]. For example: "245.2.24)"
*/
void bt_rx_parse(bluetooth_t *bt)
{
	if(bt->rx_data[0] >= '0' && bt->rx_data[0] <= '9')
	{
		bt->buff[bt->rx_len] = bt->rx_data[0];
		bt->rx_len++;			
	}
	if(bt->rx_data[0] == 'N')
	{
		/*set last brightness value got from com port*/
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
				color_rx.red = str_color_to_int(bt);
				current_color = Green;
				break;
				
			case Green:
				color_rx.green = str_color_to_int(bt);
				current_color = Blue;
				break;
				
			case Blue:
				color_rx.blue = str_color_to_int(bt);
				set_color(color_rx);
				current_color = Red;
				break;
		}
	}
	/*listen next data byte*/
	BT_listen(&huart1, bt);
}


uint8_t str_color_to_int(bluetooth_t *bt)
{
	uint8_t color_val = 0;
	
	for(uint8_t j = bt->rx_len; j != 0; j--)
	{
		if(bt->rx_len == 3)
		{
			if(j == 3)
				color_val = (bt->buff[bt->rx_len - j] - '0') * 100;
			if(j == 2)
				color_val += (bt->buff[bt->rx_len - j] - '0') * 10;
			if(j == 1)
				color_val += bt->buff[bt->rx_len - j] - '0';
		}
		if(bt->rx_len == 2)
		{
			if(j == 2)
				color_val = (bt->buff[bt->rx_len - j] - '0') * 10;
			if(j == 1)
				color_val += bt->buff[bt->rx_len - j] - '0';
		}
		if(bt->rx_len == 1)
				color_val = bt->buff[bt->rx_len - j] - '0';
	}
	bt->rx_len = 0;
	
	return color_val;	
}
