/**
  ******************************************************************************
  * @file   workers.c
  * @author Evgeny P. Kurbatov
  * @brief  Workers module
  ******************************************************************************
  */

#ifndef __WORKERS_H
#define __WORKERS_H

#include <stdint.h>
#include <stdlib.h>
#include <string.h>



uint8_t Transmit(char *, uint16_t);

void Worker_ExecuteCommand(RingBufferTypeDef *);
void Worker_ExecuteCommand_STATUS(void);
void Worker_ExecuteCommand_ADC(void);

#endif /* __WORKERS_H */
