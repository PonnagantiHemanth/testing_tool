# Project name, how the binary, map, etc files will be named
PROJECTNAME = pythonCTestFunctions

# Main project directory, relative to this Makefile directory
PRJDIR = ..

#Binary and object code directory, relative to this Makefile directory
OUTPUTDIR = ./bin

#compiling with gcc on PC platform
CC      = gcc
LD      = gcc

PROJECT = $(OUTPUTDIR)/$(PROJECTNAME)


#Sources
SRC = pythonCTestFunctions_build/test_rgb_algorithms.c \
      pythonCTestFunctions_build/rgb_algorithms.c

#  C source files
CFILES = $(filter %.c, $(SRC))
#  Assembly source files
ASMFILES = $(filter %.s, $(SRC))

# Object filse
COBJ = $(CFILES:.c=.o)
OBJ  = $(COBJ)

# This list is made with trial and error. Run make, find the missing header,
# add the path to the list.

#in this case we compile on Raspberry Pi platform, not stm32
INC = ./                                            \
	  ./pythonCTestFunctions_build/                 \
      ./pythonCTestFunctions_build/mcu/                                        \
      ./pythonCTestFunctions_build/compilers/

INCDIRS  = $(addsuffix *,$(addprefix $(PRJDIR)/, $(INC)))
INCFILES_P = $(shell ls -d $(INCDIRS))
INCFILES = $(filter %.h, $(INCFILES_P))

PYTHON_VER = 3.7m
PYTHON_INC = /usr/local/include/python$(PYTHON_VER)

# Tarongi: shouldn't we enable Thumb2 here ?
# Compile thumb for Cortex M3 with debug info
OPTIMISATION = s 
MCFLAGS = -shared -ggdb  

## Auto create dependencies for each C file, do not taking into account system header files changes : -MMD
## Store the resulting dependencies in Makefile format inside dep/ : -MF dep/$(*F).d
## Fully qualify with 'dir/filename.o:' each of the targets inside the generated dependencies: -MT $@
## Create dummy dependencies to avoid make errors when .h files are removed: -MP
DEPFLAGS = -MMD -MP -MT $@ -MF $(@:.o=.d)
CFLAGS  = $(MCFLAGS) -c -fPIC  -lpython$(PYTHON_VER) $(DEPFLAGS) -O$(OPTIMISATION) -ffunction-sections 
LFLAGS  = $(MCFLAGS) -fPIC  -lpython$(PYTHON_VER)  

# We need to specify a linker script for the linker
#LDSCRIPT = $(PRJDIR)/gcc-arm-gnueabi/stm32_flash_ldscript_appl.ld

TAGFLAGS = --c-kinds=+defgmnstuvx -R

TAGFILES  = $(addprefix $(PRJDIR)/,$(CFILES) $(ASMFILES))
#TAGFILES += $(LDSCRIPT)
TAGFILES += $(INCFILES)

OUTPUTDIRS = $(sort $(dir $(addprefix $(OUTPUTDIR)/,$(OBJ))))

$(PROJECT).so: $(addprefix $(OUTPUTDIR)/,$(OBJ))
	@echo " -> Python/C Test object created: $@"
	@$(LD) $(LFLAGS) $(addprefix $(OUTPUTDIR)/,$(OBJ)) -o $@
	@cp $(PROJECT).so $(PRJDIR)/arm

$(addprefix $(OUTPUTDIR)/,$(COBJ)):$(OUTPUTDIR)/%.o: $(PRJDIR)/%.c  | $(OUTPUTDIRS)
	@echo " -> test object: $@" 
	@$(CC) $(CFLAGS) $(addprefix -I$(PRJDIR)/,$(INC)) -I$(PYTHON_INC) $< -o $@

$(OUTPUTDIRS):
	@mkdir -p $@

clean:
	@rm -fR $(OUTPUTDIR)

.PHONY: clean
