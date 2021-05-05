#ifndef _BLUETOOTH_H_
#define _BLUETOOTH_H_

#include "main.h"

void BT_listen(UART_HandleTypeDef *huart1, char *BT_buff, uint8_t buff_size);

#endif /*_BLUETOOTH_H_*/
