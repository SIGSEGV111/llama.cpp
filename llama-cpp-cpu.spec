%global debug_package %{nil}

Name:           llama-cpp-cpu
Summary:        llama.cpp with CPU, Vulkan and OpenBLAS backends
Group:          Productivity/Scientific/Other
Distribution:   openSUSE
License:        MIT
URL:            https://github.com/ggml-org/llama.cpp
ExclusiveArch:  x86_64
Conflicts:      llama-cpp
Conflicts:      llama-cpp-nvidia
Conflicts:      llama-cpp-intel

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  libopenssl-devel
BuildRequires:  libopenblas_openmp-devel
BuildRequires:  vulkan-devel
BuildRequires:  shaderc
BuildRequires:  spirv-headers

%description
llama.cpp and its command-line tools with CPU, Vulkan and OpenBLAS backends.
This package intentionally contains no CUDA or SYCL backend.

%prep
%autosetup

%build
make build-cpu

%install
rm -rf -- "%{buildroot}"
DESTDIR="%{buildroot}" cmake --install build_dir/cpu
manifest="%{_builddir}/%{name}.files"
cd "%{buildroot}"
find \( -type f -or -type l \) | cut -c 2- > "${manifest}"
test -s "${manifest}"

%check
test -x "%{buildroot}%{_bindir}/llama-server"
test -n "$(find '%{buildroot}%{_bindir}' -maxdepth 1 -name 'libggml-cpu*.so' -print -quit)"
test -e "%{buildroot}%{_bindir}/libggml-vulkan.so"
test -e "%{buildroot}%{_bindir}/libggml-blas.so"

%files -f %{_builddir}/%{name}.files
%license LICENSE

%changelog
