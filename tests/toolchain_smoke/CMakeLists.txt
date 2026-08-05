cmake_minimum_required(VERSION 3.16)

project(svf_clang_smoke LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(LLVM 14 REQUIRED CONFIG)
find_package(Clang REQUIRED CONFIG)

add_definitions(${LLVM_DEFINITIONS})

add_executable(svf_clang_smoke main.cpp)

target_include_directories(
  svf_clang_smoke
  PRIVATE
  ${LLVM_INCLUDE_DIRS}
  ${CLANG_INCLUDE_DIRS}
)

target_link_libraries(
  svf_clang_smoke
  PRIVATE
  clangTooling
  clangAnalysis
)
