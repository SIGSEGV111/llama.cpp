%global debug_package %{nil}

Name:           llama-cpp-nvidia
Summary:        llama.cpp with NVIDIA CUDA backend for RTX 3090
Group:          Productivity/Scientific/Other
Distribution:   openSUSE
License:        MIT
URL:            https://github.com/ggml-org/llama.cpp
ExclusiveArch:  x86_64
Conflicts:      llama-cpp
Conflicts:      llama-cpp-cpu
Conflicts:      llama-cpp-intel

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  libopenssl-devel
BuildRequires:  cuda-toolkit-13-4

%description
llama.cpp and its command-line tools with only the NVIDIA CUDA compute backend.
CUDA device code is compiled for Compute Capability 8.6 (RTX 3090 / Ampere).
The CPU, Vulkan, BLAS and SYCL backends are disabled.

%prep
%autosetup

%build
make build-nvidia

%install
rm -rf -- "%{buildroot}"
DESTDIR="%{buildroot}" cmake --install build_dir/nvidia
manifest="%{_builddir}/%{name}.files"
cd "%{buildroot}"
find \( -type f -or -type l \) | cut -c 2- > "${manifest}"
test -s "${manifest}"

%check
test -x "%{buildroot}%{_bindir}/llama-server"
test -e "%{buildroot}%{_libdir}/libggml-cuda.so"
test ! -e "%{buildroot}%{_libdir}/libggml-cpu.so"
test ! -e "%{buildroot}%{_libdir}/libggml-vulkan.so"
test ! -e "%{buildroot}%{_libdir}/libggml-blas.so"
test ! -e "%{buildroot}%{_libdir}/libggml-sycl.so"

%files -f %{_builddir}/%{name}.files
%license LICENSE

%changelog
