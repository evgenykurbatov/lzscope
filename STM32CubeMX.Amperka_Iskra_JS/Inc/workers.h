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



uint8_t Transmit(char*, uint16_t);

void Worker_ExecuteCommand_ADC(char*, char*, char*);

void Worker_ExecuteCommand_ADCDMA(char*, char*, char*);
void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef*);
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef*);

#endif /* __WORKERS_H */
