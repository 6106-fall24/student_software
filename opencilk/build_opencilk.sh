#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
  opencilk_url="https://github.com/OpenCilk/opencilk-project/releases/download/opencilk%2Fv2.1/opencilk-2.1.0-x86_64-linux-gnu-ubuntu-22.04.tar.gz"
  cheetah_url="https://github.com/OpenCilk/cheetah.git"

  echo "Verifying cmake install"
  if ! which cmake; then
    echo "cmake does not exist. Installing cmake..."
    apt-get install cmake
  fi

  echo "Downloading OpenCilk binaries"
  mkdir build
  curl -L $opencilk_url | tar -zxv --strip-components=1 -C build

  opencilk_path=$(pwd)/build

  echo "Creating link clang-6106"
  sudo ln -sf $opencilk_path/bin/clang /usr/bin/clang-6106

  echo "Pulling cheetah runtime"
  git clone $cheetah_url cheetah

  cheetah_path=$(pwd)/cheetah

  echo "Turning off AVX flag"
  sed -i '25d' $cheetah_path/cmake/config-ix.cmake

  cores=8

  echo "Building cheetah runtime with $cores cores"
  cd build/lib/clang/16/
  cmake -DCMAKE_C_COMPILER=$opencilk_path/bin/clang -DCMAKE_BUILD_TYPE=Release -DLLVM_CMAKE_DIR=$opencilk_path -DCHEETAH_DIRECTORY_PER_TARGET=ON $cheetah_path
  cmake --build . -- -j$cores
fi