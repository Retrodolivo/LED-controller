#ifndef _VCP_H_
#define _VCP_H_

#include "main.h"

#define VCP_RX_DATA_SIZE		50
#define NUMBER_OF_CMDS			5
#define CMD_LENGHT					20

typedef struct
{
	char cmd[NUMBER_OF_CMDS][CMD_LENGHT];
	uint8_t rx_data[VCP_RX_DATA_SIZE];
	uint8_t rx_len;
	char cmd_stop_byte;
}vcp_t;

void VCP_init(vcp_t *vcp);
void vcp_rx_parse(vcp_t *vcp, uint8_t *rx_byte);

#endif /*_VCP_H_*/

