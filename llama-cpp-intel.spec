%global debug_package %{nil}
%{!?oneapi_compiler_version:%global oneapi_compiler_version 2026.2}
%{!?oneapi_mkl_version:%global oneapi_mkl_version 2026.2}
%{!?oneapi_dnnl_version:%global oneapi_dnnl_version 2026.1}

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
Requires:       intel-oneapi-compiler-dpcpp-cpp-runtime-%{oneapi_compiler_version}
Requires:       intel-oneapi-mkl-sycl-blas-%{oneapi_mkl_version}
Requires:       intel-oneapi-dnnl-%{oneapi_dnnl_version}
Requires:       libze_intel_gpu1

%if 0%{?easy_rpm_prebuilt} == 0
BuildRequires:  make
BuildRequires:  libopenssl-devel
BuildRequires:  intel-oneapi-compiler-dpcpp-cpp-%{oneapi_compiler_version}
BuildRequires:  intel-oneapi-mkl-devel-%{oneapi_mkl_version}
BuildRequires:  intel-oneapi-mkl-sycl-devel-%{oneapi_mkl_version}
BuildRequires:  intel-oneapi-dnnl-devel-%{oneapi_dnnl_version}
BuildRequires:  level-zero-devel
%endif

%description
llama.cpp and its command-line tools with only the Intel SYCL compute backend,
targeted at Intel Arc Pro B60 / Battlemage. The CPU, CUDA, Vulkan and BLAS
backends are disabled.

%prep
%autosetup

%build
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
. /opt/intel/oneapi/compiler/%{oneapi_compiler_version}/env/vars.sh >/dev/null 2>&1
. /opt/intel/oneapi/mkl/%{oneapi_mkl_version}/env/vars.sh >/dev/null 2>&1
. /opt/intel/oneapi/dnnl/%{oneapi_dnnl_version}/env/vars.sh >/dev/null 2>&1
! ldd -r "%{buildroot}%{_bindir}/libggml-sycl.so" 2>&1 | grep -E 'not found|undefined symbol'

%files -f %{_builddir}/%{name}.files
%license LICENSE

%changelog
