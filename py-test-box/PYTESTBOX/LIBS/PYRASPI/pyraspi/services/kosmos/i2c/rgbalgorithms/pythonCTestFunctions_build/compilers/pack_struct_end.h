
/******************************************************************************
 Copyright (C) 2013 LOGITECH
-------------------------------------------------------------------------------

Restore default padding
*******************************************************************************/

#ifndef PACK_STRUCT_END_H
#define PACK_STRUCT_END_H

#ifndef __CC_ARM
#error "Structure-packing directive for ARM C compiler (CC)"
#endif

#undef PACK_STRUCT_START_H

#pragma pack(8)

#endif /* PACK_STRUCT_END_H */
