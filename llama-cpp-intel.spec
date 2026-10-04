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

%if 0%{?easy_rpm_prebuilt} == 0
BuildRequires:  make
BuildRequires:  libopenssl-devel
BuildRequires:  intel-oneapi-compiler-dpcpp-cpp
BuildRequires:  intel-opencl
BuildRequires:  intel-oneapi-mkl-devel
BuildRequires:  intel-oneapi-mkl-sycl-devel
BuildRequires:  intel-oneapi-dnnl-devel
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

%files -f %{_builddir}/%{name}.files
%license LICENSE

%changelog
