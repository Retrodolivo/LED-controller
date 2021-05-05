#include "vcp.h"
#include "usbd_cdc_if.h"

extern Color_t color_rx;
extern Color_t color_none;

void VCP_init(vcp_t *vcp)
{
	/*fill vcp struct*/
	strcpy(vcp->cmd[0], "led on");
	strcpy(vcp->cmd[1], "led off");
	strcpy(vcp->cmd[2], "C");
	strcpy(vcp->cmd[3], "T");
	strcpy(vcp->cmd[4], "A");
	vcp->cmd_stop_byte = '~';
	/*Clear vcp rx buffer*/
	for(uint8_t i = 0; i < VCP_RX_DATA_SIZE; i++) 
		vcp->rx_data[i] = 0;
	vcp->rx_len = 0;	
}

void vcp_rx_parse(vcp_t *vcp, uint8_t *rx_byte)
{
	if(vcp->rx_len < VCP_RX_DATA_SIZE && *rx_byte != vcp->cmd_stop_byte)
	{
		vcp->rx_data[vcp->rx_len] = *rx_byte;
		vcp->rx_len++;
	}
	else
	{
		if(strcmp((char *)vcp->rx_data, vcp->cmd[0])== 0)
		{ 
			set_color(color_rx, 1);
			CDC_Transmit_FS((uint8_t *)vcp->cmd[0], strlen(vcp->cmd[0]));
		}
		if(strcmp((char *)vcp->rx_data, vcp->cmd[1]) == 0)
		{
			set_color(color_rx, 0);
			CDC_Transmit_FS((uint8_t *)vcp->cmd[1], strlen(vcp->cmd[1]));
		}
		if(vcp->rx_data[0] == vcp->cmd[2][0])
		{
			color_rx.red = vcp->rx_data[1];
			color_rx.green = vcp->rx_data[2];
			color_rx.blue = vcp->rx_data[3];
			set_color(color_rx, 1);
			CDC_Transmit_FS((uint8_t *)vcp->cmd[2], strlen(vcp->cmd[2]));
		}
		for(uint8_t i = 0; i < vcp->rx_len; i++)
			vcp->rx_data[i] = 0;
		vcp->rx_len = 0;
	}
}


