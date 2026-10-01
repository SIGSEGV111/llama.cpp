%global debug_package %{nil}

Name:           llama-cpp-intel
Summary:        llama.cpp with Intel SYCL backend for Arc Pro B60
Group:          Productivity/Scientific/Other
Distribution:   openSUSE
License:        MIT
URL:            https://github.com/ggml-org/llama.cpp
ExclusiveArch:  x86_64
Conflicts:      llama-cpp
Conflicts:      llama-cpp-cpu
Conflicts:      llama-cpp-nvidia

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  libopenssl-devel
BuildRequires:  intel-oneapi-toolkit
BuildRequires:  intel-opencl

%description
llama.cpp and its command-line tools with only the Intel SYCL compute backend,
targeted at Intel Arc Pro B60 / Battlemage. The CPU, CUDA, Vulkan and BLAS
backends are disabled.

%prep
%autosetup

%build
source /opt/intel/oneapi/setvars.sh --include-intel-llvm
make build-intel

%install
rm -rf -- "%{buildroot}"
DESTDIR="%{buildroot}" cmake --install build_dir/intel
manifest="%{_builddir}/%{name}.files"
cd "%{buildroot}"
find \( -type f -or -type l \) | cut -c 2- > "${manifest}"
test -s "${manifest}"

%check
test -x "%{buildroot}%{_bindir}/llama-server"
test -e "%{buildroot}%{_bindir}/libggml-sycl.so"
test -z "$(find '%{buildroot}%{_bindir}' -maxdepth 1 -name 'libggml-cpu*.so' -print -quit)"
test ! -e "%{buildroot}%{_bindir}/libggml-cuda.so"
test ! -e "%{buildroot}%{_bindir}/libggml-vulkan.so"
test ! -e "%{buildroot}%{_bindir}/libggml-blas.so"

%files -f %{_builddir}/%{name}.files
%license LICENSE

%changelog
