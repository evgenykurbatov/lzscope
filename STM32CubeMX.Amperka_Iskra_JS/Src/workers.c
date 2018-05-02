/**
  ******************************************************************************
  * @file   workers.c
  * @author Evgeny P. Kurbatov
  * @brief  Workers module
  ******************************************************************************
  */

#include "usbd_cdc_if.h"

#include "main.h"
#include "ringbuffer.h"
#include "workers.h"



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
} DMABuf;



/*
 * Buffer and pointers for command parser
 */

#define CMD_BUFFER_SIZE RX_RING_BUFFER_DATA_SIZE
char CmdBuf[CMD_BUFFER_SIZE];
char *CmdName, *CmdArg1, *CmdArg2, *CmdArg3;



void Worker_ExecuteCommand(RingBufferTypeDef *RingBuf)
{
  /* Copy ring buffer into the command buffer. */
  for (uint32_t i=0; i < CMD_BUFFER_SIZE-1; i++)
    CmdBuf[i] = RingBuffer_Remove(RingBuf);
  CmdBuf[CMD_BUFFER_SIZE-1] = '\0';

  CmdName = strtok(CmdBuf, " ");
  CmdArg1 = strtok(NULL, " ");
  CmdArg2 = strtok(NULL, " ");
  CmdArg3 = strtok(NULL, " ");

  if (!strcasecmp(CmdName, "STATUS"))
  {
    Worker_ExecuteCommand_STATUS();
    return;
  }
  /*
  if (!strcasecmp(CmdName, "GPIO"))
  {
    Worker_ExecuteCommand_GPIO();
    return;
  }
  */
}



void Worker_ExecuteCommand_STATUS(void)
{
  Transmit("STATUS\n", 7);
  Transmit("OK\n", 3);
}
