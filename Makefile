STD_MAKE_LIB_DIR ?= submodules/std-make-lib

CI_ENABLE := 1

RPM_PACKAGE_IDS := MAIN
RPM_MAIN_NAME := llama-cpp
RPM_MAIN_SPEC := llama-cpp.spec
RPM_MAIN_BUILD_DEPS := build
RPM_MAIN_EASY_RPM_FLAGS := --prebuilt

# Makefile and Makefile.common are added by std-make-lib automatically.
# Do not recursively include the complete std-make-lib submodule in Source0.
RPM_MAIN_SOURCE_FILES := .

include $(STD_MAKE_LIB_DIR)/Makefile.common

CMAKE ?= cmake
BUILD_DIR ?= build_dir
JOBS ?= $(shell nproc)

RPM_LIBDIR ?= $(shell rpm --eval '%{_lib}' 2>/dev/null || printf 'lib64')
ONEAPI_ENV := source /opt/intel/oneapi/setvars.sh --include-intel-llvm >/dev/null 2>&1

CMAKE_ARGS := \
	-DCMAKE_C_COMPILER=icx \
	-DCMAKE_CXX_COMPILER=icpx \
	-DGGML_SYCL=ON \
	-DGGML_CUDA=ON \
	-DGGML_VULKAN=ON \
	-DGGML_NATIVE=ON \
	-DGGML_SYCL_F16=ON \
	-DGGML_SYCL_TARGET=INTEL \
	-DGGML_SYCL_DEVICE_ARCH=bmg_g21 \
	-DCMAKE_CUDA_ARCHITECTURES=86-real \
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
	-DLLAMA_USE_PREBUILT_UI=OFF \
	-DGGML_OPENMP=ON \
	-DGGML_BLAS=ON \
	-DGGML_BLAS_VENDOR=Intel10_64lp \
	-DGGML_CCACHE=OFF \
	-DGGML_BACKEND_DL=ON

.PHONY: all configure build clean

all: build

configure:
	$(ONEAPI_ENV) && $(CMAKE) -S . -B "$(BUILD_DIR)" $(CMAKE_ARGS)

build: configure
	$(ONEAPI_ENV) && $(CMAKE) --build "$(BUILD_DIR)" --parallel "$(JOBS)"

clean:
	rm -rf -- "$(BUILD_DIR)" "$(GEN_DIR)"
	rm -f -- $(RPM_ARTIFACTS)
