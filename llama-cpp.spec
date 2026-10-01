%global debug_package %{nil}

Name:           llama-cpp
Summary:        llama.cpp built with NVIDIA CUDA support for RTX 3000 GPUs
Group:          Productivity/Scientific/Other
Distribution:   openSUSE
License:        MIT
URL:            https://github.com/ggml-org/llama.cpp
ExclusiveArch:  x86_64

# These are needed when rebuilding the generated source RPM.
# Add the RPM name of your CUDA toolkit here if your CUDA installation is
# managed by RPM on the build hosts.
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  libopenssl-devel
BuildRequires:  libopenblas_openmp-devel

%description
llama.cpp and its command-line tools, built with the CUDA backend enabled.
The CUDA device code is compiled for NVIDIA Compute Capability 8.6
(RTX 3000 / Ampere).

%prep
%autosetup

%build
make build

%install
rm -rf -- "%{buildroot}"
DESTDIR="%{buildroot}" cmake --install build_dir
manifest="%{_builddir}/%{name}.files"
cd "%{buildroot}"
find \( -type f -or -type l \) | cut -c 2- > "${manifest}"
test -s "${manifest}"

%check
test -x "%{buildroot}%{_bindir}/llama-server"
test -e "%{buildroot}%{_libdir}/libggml-cuda.so"

%files -f %{_builddir}/%{name}.files
%license LICENSE

%changelog
