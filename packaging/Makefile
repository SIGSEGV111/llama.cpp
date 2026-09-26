STD_MAKE_LIB_DIR ?= submodules/std-make-lib

STD_PROFILE := package-only
CI_ENABLE := 1

RPM_PACKAGE_IDS := MAIN
RPM_MAIN_NAME := llama-cpp-cuda
RPM_MAIN_SPEC := packaging/llama-cpp-cuda.spec
RPM_MAIN_BUILD_DEPS := build
RPM_MAIN_EASY_RPM_FLAGS := --prebuilt

# Makefile and Makefile.common are added by std-make-lib automatically.
# Do not recursively include the complete std-make-lib submodule in Source0.
RPM_MAIN_SOURCE_FILES := $(filter-out Makefile $(STD_MAKE_LIB_DIR),$(shell git ls-files))

include $(STD_MAKE_LIB_DIR)/Makefile.common

CMAKE ?= cmake
BUILD_DIR ?= build_dir
JOBS ?= $(shell nproc)

# RTX 3090 = Compute Capability 8.6.
# "-real" emits native device code only and avoids PTX for other/future GPUs.
CUDA_ARCHITECTURES ?= 86-real

RPM_LIBDIR ?= $(shell rpm --eval '%{_lib}' 2>/dev/null || printf 'lib64')

CMAKE_ARGS := \
	-DGGML_CUDA=ON \
	-DGGML_NATIVE=OFF \
	-DCMAKE_CUDA_ARCHITECTURES="$(CUDA_ARCHITECTURES)" \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=/usr \
	-DCMAKE_INSTALL_LIBDIR="$(RPM_LIBDIR)" \
	-DBUILD_SHARED_LIBS=ON \
	-DLLAMA_BUILD_COMMON=ON \
	-DLLAMA_BUILD_TOOLS=ON \
	-DLLAMA_BUILD_SERVER=ON \
	-DLLAMA_BUILD_APP=ON \
	-DLLAMA_TOOLS_INSTALL=ON \
	-DLLAMA_BUILD_TESTS=OFF \
	-DLLAMA_BUILD_EXAMPLES=OFF \
	-DLLAMA_BUILD_UI=OFF \
	-DLLAMA_USE_PREBUILT_UI=OFF

.PHONY: all configure build clean

all: build

configure:
	$(CMAKE) -S . -B "$(BUILD_DIR)" $(CMAKE_ARGS)

build: configure
	$(CMAKE) --build "$(BUILD_DIR)" --parallel "$(JOBS)"

clean:
	rm -rf -- "$(BUILD_DIR)" "$(GEN_DIR)"
	rm -f -- $(RPM_ARTIFACTS)
