#include "bluetooth.h"


void BT_listen(UART_HandleTypeDef *huart1, char *BT_buff, uint8_t buff_size)
{
	HAL_UART_Receive_IT(huart1, (uint8_t*)BT_buff, buff_size);
}

