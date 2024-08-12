
/******************************************************************************
 Copyright (C) 2013 LOGITECH
-------------------------------------------------------------------------------

Prevent any padding in structures
*******************************************************************************/

#ifndef PACK_STRUCT_START_H
#define PACK_STRUCT_START_H

#ifndef __CC_ARM
#error "Structure-packing directive for ARM C compiler (CC)"
#endif

#undef PACK_STRUCT_END_H

#pragma pack(1)

#endif /* PACK_STRUCT_START_H */
