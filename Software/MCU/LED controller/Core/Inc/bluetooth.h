#ifndef _BLUETOOTH_H_
#define _BLUETOOTH_H_

#include "main.h"

#define RX_SIZE		1
#define BUFF_SIZE	5

typedef struct
{
	char rx_data[RX_SIZE];
	char buff[BUFF_SIZE];
	uint8_t rx_len;
} bluetooth_t;

typedef struct
{
	uint8_t red, green, blue;
	float brightness;
} latest_data_t;

void BT_listen(UART_HandleTypeDef *huart1, bluetooth_t *bt);
void bt_rx_parse(bluetooth_t *bt);
uint8_t str_color_to_int(bluetooth_t *bt);

#endif /*_BLUETOOTH_H_*/
