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

%description
llama.cpp and its command-line tools, built with the CUDA backend enabled.
The CUDA device code is compiled for NVIDIA Compute Capability 8.6
(RTX 3000 / Ampere).

%prep
%autosetup

%build
cmake \
	-S . \
	-B build_dir \
	-DGGML_CUDA=ON \
	-DGGML_NATIVE=OFF \
	-DCMAKE_CUDA_ARCHITECTURES=86 \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
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

cmake --build build_dir --parallel %{?_smp_build_ncpus}

%install
rm -rf -- "%{buildroot}"

DESTDIR="%{buildroot}" cmake --install build_dir

manifest="%{_builddir}/%{name}.files"

find "%{buildroot}" \
	\( -type f -o -type l \) \
	-printf '/\%P\n' \
	| LC_ALL=C sort \
	> "${manifest}"

test -s "${manifest}"

%check
test -x "%{buildroot}%{_bindir}/llama-server"
test -e "%{buildroot}%{_libdir}/libggml-cuda.so"

%files -f %{_builddir}/%{name}.files
%license LICENSE

%changelog
