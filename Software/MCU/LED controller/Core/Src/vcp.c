#include "vcp.h"
#include "usbd_cdc_if.h"

Color_t color_rx = 		{.red = 0, .green = 0, .blue = 0, .brightness = 1};

extern RTC_HandleTypeDef hrtc;
RTC_TimeTypeDef sTime = {0};
RTC_DateTypeDef DateToUpdate = {0};
RTC_AlarmTypeDef sAlarm = {0};

float brightness_temp;

void VCP_init(vcp_t *vcp)
{
	/*fill vcp struct*/
	strcpy(vcp->cmd[0], "led on");
	strcpy(vcp->cmd[1], "led off");
	strcpy(vcp->cmd[2], "C");
	strcpy(vcp->cmd[3], "B");
	strcpy(vcp->cmd[4], "T");
	strcpy(vcp->cmd[5], "A");
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
			color_rx.brightness = brightness_temp;
			set_color(color_rx);
			CDC_Transmit_FS((uint8_t *)vcp->cmd[0], strlen(vcp->cmd[0]));
		}
		if(strcmp((char *)vcp->rx_data, vcp->cmd[1]) == 0)
		{
			color_rx.brightness = 0;
			set_color(color_rx);
			CDC_Transmit_FS((uint8_t *)vcp->cmd[1], strlen(vcp->cmd[1]));
		}
		if(vcp->rx_data[0] == vcp->cmd[2][0])
		{
			color_rx.red = vcp->rx_data[1];
			color_rx.green = vcp->rx_data[2];
			color_rx.blue = vcp->rx_data[3];
			set_color(color_rx);
			CDC_Transmit_FS((uint8_t *)vcp->cmd[2], strlen(vcp->cmd[2]));
		}
		if(vcp->rx_data[0] == vcp->cmd[3][0])
		{
			color_rx.brightness = to_float(vcp->rx_data[1]);
			set_color(color_rx);
			CDC_Transmit_FS((uint8_t *)vcp->cmd[3], strlen(vcp->cmd[3]));
			brightness_temp = color_rx.brightness;
		}			
		if(vcp->rx_data[0] == vcp->cmd[4][0])
		{
			DateToUpdate.Year = vcp->rx_data[1];
			DateToUpdate.Month = vcp->rx_data[2];
			DateToUpdate.Date = vcp->rx_data[3];
			sTime.Hours = vcp->rx_data[4];
			sTime.Minutes = vcp->rx_data[5];
			sTime.Seconds = vcp->rx_data[6];
			
			HAL_RTC_SetDate(&hrtc, &DateToUpdate, RTC_FORMAT_BIN);
			HAL_RTC_SetTime(&hrtc, &sTime, RTC_FORMAT_BIN);
			CDC_Transmit_FS((uint8_t *)vcp->cmd[4], strlen(vcp->cmd[4]));			
		}
		if(vcp->rx_data[0] == vcp->cmd[5][0])
		{
			sAlarm.AlarmTime.Hours = vcp->rx_data[1];
			sAlarm.AlarmTime.Minutes = vcp->rx_data[2];
			sAlarm.AlarmTime.Seconds = vcp->rx_data[3];
			HAL_RTC_SetAlarm_IT(&hrtc, &sAlarm, RTC_FORMAT_BIN);
			CDC_Transmit_FS((uint8_t *)vcp->cmd[5], strlen(vcp->cmd[5]));	
		}
		/*Clear vcp rx buffer*/
		for(uint8_t i = 0; i < vcp->rx_len; i++)
			vcp->rx_data[i] = 0;
		vcp->rx_len = 0;
	}
}

float to_float(char cdata) 
{
	float fdata = (float)cdata / 100;
	return fdata;
}


