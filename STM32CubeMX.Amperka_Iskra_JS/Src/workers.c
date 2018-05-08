/**
  ******************************************************************************
  * @file   workers.c
  * @author Evgeny P. Kurbatov
  * @brief  Workers module
  ******************************************************************************
  */

#include "usbd_cdc_if.h"
#include "adc.h"

#include "main.h"
#include "ringbuffer.h"
#include "workers.h"



/*
 * Communication buffer between interruption handler and main loop.
 */

uint8_t Transmit(char* Buf, uint16_t Len)
{
  uint8_t result;

  do
    result = CDC_Transmit_FS((uint8_t*) Buf, Len);
  while (result == USBD_BUSY);
  /*
  do
    result = CDC_Transmit_FS((uint8_t*) Buf, 0);
  while (result == USBD_BUSY);
  */

  return result;
}



/*
 * Use union as a DMA transfer buffer.
 * The idea is stolen from @xedas, see https://geektimes.ru/post/263210/
 */

#define DMA_BUFFER_SIZE_U32 16384
#define DMA_BUFFER_SIZE_U16 (DMA_BUFFER_SIZE_U32*2)
#define DMA_BUFFER_SIZE_U8  (DMA_BUFFER_SIZE_U32*4)

#define DMA_BUFFER_SIZE_HALF_U32 (DMA_BUFFER_SIZE_U32>>1)
#define DMA_BUFFER_SIZE_HALF_U16 (DMA_BUFFER_SIZE_U16>>1)
#define DMA_BUFFER_SIZE_HALF_U8  (DMA_BUFFER_SIZE_U8>>1)

volatile union
{
  uint32_t u32[DMA_BUFFER_SIZE_U32];
  uint16_t u16[DMA_BUFFER_SIZE_U16];
  uint8_t  u8[DMA_BUFFER_SIZE_U8];
} DMABuffer;



/*
 * Make a single ADC measurement
 */

void Worker_ExecuteCommand_ADC(char *CmdArg1, char *CmdArg2, char *CmdArg3)
{
  /* Measure */
  HAL_ADC_Start(&hadc1);
  HAL_ADC_PollForConversion(&hadc1, 100);
  DMABuffer.u16[0] = HAL_ADC_GetValue(&hadc1);
  HAL_ADC_Stop(&hadc1);

  /* Transmit */
  Transmit((char *) &(DMABuffer.u16[0]), 4);
}



/*
 * Make ADC measurements continuously and store it in a circular buffer via DMA
 */

extern RingBufferTypeDef RxRingBuffer;

/* Flag */
volatile bool ADCDMA_DataIsReady;
/* Pointer to the data to transmit */
volatile char *ADCDMA_DataBuffer;
/* Length of the transmitted data block in bytes */
volatile uint32_t ADCDMA_DataLength;



void Worker_ExecuteCommand_ADCDMA(char *CmdArg1, char *CmdArg2, char *CmdArg3)
{
  /*
   * Init
   */

  ADCDMA_DataIsReady == false;

  uint32_t DMABufferLength;
  sscanf(CmdArg1, "%li", &DMABufferLength);

  ADCDMA_DataLength = (DMABufferLength >> 1) * sizeof(uint16_t);

  HAL_ADC_Start_DMA(&hadc1, (uint32_t *) (DMABuffer.u16), DMABufferLength);


  /*
   * Execution loop
   */

  while (1)
  {

    if (RingBuffer_IsEmpty(&RxRingBuffer) == false)
    {
      /*
       * Parse command
       */

      #define TOKEN_SIZE 16
      char CmdName[TOKEN_SIZE];
      for (uint32_t i=0; i < TOKEN_SIZE; i++)
      {
	CmdName[i] = RingBuffer_Remove(&RxRingBuffer);
	if (CmdName[i] == '\0')
	  break;
      }


      /*
       * Execute command
       */

      if (!strcasecmp(CmdName, "GET"))
      {
	while (ADCDMA_DataIsReady == false);
	
	Transmit((char *) ADCDMA_DataBuffer, ADCDMA_DataLength);

	ADCDMA_DataIsReady == false;
	continue;
      }
      if (!strcasecmp(CmdName, "STOP"))
      {
	Transmit("OK", 3);

	ADCDMA_DataIsReady == false;
	break;
      }

    }

  }


  /*
   * Done
   */

  HAL_ADC_Stop_DMA(&hadc1);
}



void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef *hadc)
{
  ADCDMA_DataBuffer = (char *) &(DMABuffer.u16[0]);
  ADCDMA_DataIsReady = true;
}



void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *hadc)
{
  ADCDMA_DataBuffer = (char *) &(DMABuffer.u16[DMA_BUFFER_SIZE_HALF_U16]);
  ADCDMA_DataIsReady = true;
}
