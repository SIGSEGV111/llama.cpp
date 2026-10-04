STD_MAKE_LIB_DIR ?= submodules/std-make-lib

CI_ENABLE := 1

RPM_PACKAGE_IDS := CPU NVIDIA INTEL

RPM_CPU_NAME := llama-cpp-cpu
RPM_CPU_SPEC := llama-cpp-cpu.spec
RPM_CPU_BUILD_DEPS := build
RPM_CPU_EASY_RPM_FLAGS := --prebuilt
RPM_CPU_SOURCE_FILES := .

RPM_NVIDIA_NAME := llama-cpp-nvidia
RPM_NVIDIA_SPEC := llama-cpp-nvidia.spec
RPM_NVIDIA_BUILD_DEPS := build
RPM_NVIDIA_EASY_RPM_FLAGS := --prebuilt
RPM_NVIDIA_SOURCE_FILES := .

RPM_INTEL_NAME := llama-cpp-intel
RPM_INTEL_SPEC := llama-cpp-intel.spec
RPM_INTEL_BUILD_DEPS := build
RPM_INTEL_EASY_RPM_FLAGS := --prebuilt
RPM_INTEL_SOURCE_FILES := .

include $(STD_MAKE_LIB_DIR)/Makefile.common

CMAKE ?= cmake
JOBS ?= $(shell nproc)

BUILD_ROOT ?= build_dir
CPU_BUILD_DIR ?= $(BUILD_ROOT)/cpu
NVIDIA_BUILD_DIR ?= $(BUILD_ROOT)/nvidia
INTEL_BUILD_DIR ?= $(BUILD_ROOT)/intel

RPM_LIBDIR ?= $(shell rpm --eval '%{_lib}' 2>/dev/null || printf 'lib64')
ONEAPI_ENV := source /opt/intel/oneapi/setvars.sh --include-intel-llvm >/dev/null 2>&1

CMAKE_COMMON_ARGS := \
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
	-DGGML_CCACHE=OFF \
	-DGGML_BACKEND_DL=ON \
	-DGGML_CPU=ON \
	-DGGML_NATIVE=OFF \
	-DGGML_CPU_ALL_VARIANTS=ON

CMAKE_BACKENDS_OFF := \
	-DGGML_CUDA=OFF \
	-DGGML_VULKAN=OFF \
	-DGGML_SYCL=OFF \
	-DGGML_BLAS=OFF \
	-DGGML_OPENMP=OFF

CPU_CMAKE_ARGS := \
	$(CMAKE_COMMON_ARGS) \
	$(CMAKE_BACKENDS_OFF) \
	-DCMAKE_C_COMPILER=gcc \
	-DCMAKE_CXX_COMPILER=g++ \
	-DGGML_CPU_ALL_VARIANTS=ON \
	-DGGML_VULKAN=ON \
	-DGGML_BLAS=ON \
	-DGGML_BLAS_VENDOR=OpenBLAS \
	-DGGML_OPENMP=ON

NVIDIA_CMAKE_ARGS := \
	$(CMAKE_COMMON_ARGS) \
	$(CMAKE_BACKENDS_OFF) \
	-DCMAKE_C_COMPILER=gcc \
	-DCMAKE_CXX_COMPILER=g++ \
	-DGGML_CUDA=ON \
	-DGGML_CUDA_NCCL=OFF \
	-DCMAKE_CUDA_ARCHITECTURES=86-real

INTEL_CMAKE_ARGS := \
	$(CMAKE_COMMON_ARGS) \
	$(CMAKE_BACKENDS_OFF) \
	-DCMAKE_C_COMPILER=icx \
	-DCMAKE_CXX_COMPILER=icpx \
	-DGGML_SYCL=ON \
	-DGGML_SYCL_F16=ON \
	-DGGML_SYCL_DNN=ON \
	-DGGML_SYCL_TARGET=INTEL \
	-DGGML_SYCL_DEVICE_ARCH=bmg_g21

CI_RPM_ARTIFACTS := \
	$(RPM_CPU_ARCH_FILE) \
	$(RPM_NVIDIA_ARCH_FILE) \
	$(RPM_INTEL_ARCH_FILE)

.PHONY: all build \
	configure-cpu build-cpu \
	configure-nvidia build-nvidia \
	configure-intel build-intel \
	clean

all: build

build: build-cpu build-nvidia build-intel

configure-cpu:
	$(CMAKE) -S . -B "$(CPU_BUILD_DIR)" $(CPU_CMAKE_ARGS)

build-cpu: configure-cpu
	$(CMAKE) --build "$(CPU_BUILD_DIR)" --parallel "$(JOBS)"

configure-nvidia:
	$(CMAKE) -S . -B "$(NVIDIA_BUILD_DIR)" $(NVIDIA_CMAKE_ARGS)

build-nvidia: configure-nvidia
	$(CMAKE) --build "$(NVIDIA_BUILD_DIR)" --parallel "$(JOBS)"

configure-intel:
	$(ONEAPI_ENV) && $(CMAKE) -S . -B "$(INTEL_BUILD_DIR)" $(INTEL_CMAKE_ARGS)

build-intel: configure-intel
	$(ONEAPI_ENV) && $(CMAKE) --build "$(INTEL_BUILD_DIR)" --parallel "$(JOBS)"

clean:
	rm -rf -- "$(BUILD_ROOT)" "$(GEN_DIR)"
	rm -f -- $(RPM_ARTIFACTS)
