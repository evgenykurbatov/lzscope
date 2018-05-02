/**
  ******************************************************************************
  * @file   ringbuffer.h
  * @author Evgeny P. Kurbatov
  * @brief  Ring buffer
  *         Inspired by RingBuffer implementation by Dean Camera (LUFA Library).
  *
  *         NOTE: It's not a thread-safe.
  *
  ******************************************************************************
  */

#ifndef __RINGBUFFER_H
#define __RINGBUFFER_H

#include <stdbool.h>
#include <stdint.h>



typedef struct
{
  uint8_t *Buffer;
  uint32_t Length;
  int32_t Begin;        /* Position of removed byte. */
  int32_t End;          /* Position of inserted byte. */
}
  RingBufferTypeDef;

/**
  * @brief  RingBuffer_Init
  *         Initializes a ring buffer
  * @note   No allocation is performed, it's on the user. The ring buffer is just marked as empty.
  * @param  RingBuf: RingBufferTypeDef data structure
  * @param  Buf: Buffer of data on which the ring buffer is built
  * @param  Len: Length of the buffer, i.e. maximum number of bytes that can be stored
  * @retval None
  */
static inline void RingBuffer_Init(RingBufferTypeDef *RingBuf, uint8_t *Buf, uint32_t Len)
{
  RingBuf->Buffer = Buf;
  RingBuf->Length = Len;
  RingBuf->Begin = 0;
  RingBuf->End = 0;
}

/**
  * @brief  RingBuffer_Reset
  *         Clean a ring buffer
  * @param  RingBuf: RingBufferTypeDef data structure
  * @retval None
  */
static inline void RingBuffer_Reset(RingBufferTypeDef *RingBuf)
{
  RingBuf->Begin = 0;
  RingBuf->End = 0;
}

/**
  * @brief  RingBuffer_GetCount
  *         Retrieves the current number of bytes stored in a particular buffer
  * @param  RingBuf: RingBufferTypeDef data structure
  * @retval Number of bytes not greater than the total buffer's length
  */
static inline uint32_t RingBuffer_GetCount(RingBufferTypeDef *RingBuf)
{
  return ((RingBuf->End - RingBuf->Begin) % RingBuf->Length);
}

/**
  * @brief  RingBuffer_GetFreeCount
  *         Retrieves the current number of free bytes in a particular buffer
  * @param  RingBuf: RingBufferTypeDef data structure
  * @retval Number of bytes not greater than the total buffer's length
  */
static inline uint32_t RingBuffer_GetFreeCount(RingBufferTypeDef *RingBuf)
{
  return (RingBuf->Length - RingBuffer_GetCount(RingBuf));
}

/**
  * @brief  RingBuffer_IsEmpty
  *         Determines if the specified ring buffer contains any data
  * @note   This should be tested before removing data from the buffer, to
  *         ensure that the buffer is not underflow.
  * @param  RingBuf: RingBufferTypeDef data structure
  * @retval Boolean true if the buffer contains no data, false otherwise
  */
static inline bool RingBuffer_IsEmpty(RingBufferTypeDef *RingBuf)
{
  return (RingBuffer_GetCount(RingBuf) == 0);
}

/**
  * @brief  RingBuffer_IsFull
  *         Determines if the specified ring buffer contains any free space
  * @note   This should be tested before storing data to the buffer, to ensure
  *         that the buffer is not overflow.
  * @param  RingBuf: RingBufferTypeDef data structure
  * @retval Boolean true if the buffer contains no free space, false otherwise
  */
static inline bool RingBuffer_IsFull(RingBufferTypeDef *RingBuf)
{
  return (RingBuffer_GetCount(RingBuf) == RingBuf->Length);
}

/**
  * @brief  RingBuffer_Insert
  *         Inserts a byte into the end of the ring buffer
  * @param  RingBuf: RingBufferTypeDef data structure
  * @param  c: Byte to be inserted
  * @retval None
  */
static inline void RingBuffer_Insert(RingBufferTypeDef *RingBuf, uint8_t c)
{
  uint32_t End = RingBuf->End;
  (RingBuf->Buffer)[End] = c;
  RingBuf->End = (++End) % RingBuf->Length;
}

/**
  * @brief  RingBuffer_Remove
  *         Removes a byte from the beginning of the ring buffer
  * @param  RingBuf: RingBufferTypeDef data structure
  * @retval Removed byte
  */
static inline uint8_t RingBuffer_Remove(RingBufferTypeDef *RingBuf)
{
  uint32_t Begin = RingBuf->Begin;
  uint8_t c = (RingBuf->Buffer)[Begin];
  RingBuf->Begin = (++Begin) % RingBuf->Length;
  return c;
}

/**
  * @brief  RingBuffer_Peek
  *         Returns the element stored in the beginning of the ring buffer without removing it
  * @param  RingBuf: RingBufferTypeDef data structure
  * @retval Byte stored in the beginning of the buffer
  */
static inline uint8_t RingBuffer_Peek(RingBufferTypeDef *RingBuf)
{
  return (RingBuf->Buffer)[RingBuf->Begin];
}

#endif /* __RINGBUFFER_H */
