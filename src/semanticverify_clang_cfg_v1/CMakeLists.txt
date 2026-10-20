cmake_minimum_required(VERSION 3.16)
project(semanticverify_clang_cfg_v1 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(LLVM 14 REQUIRED CONFIG)

# Ubuntu 22.04's ClangConfig.cmake does not publish compatible
# package-version metadata. Clang_DIR and both compilers are pinned
# explicitly by the qualification command below.
find_package(Clang REQUIRED CONFIG)

if(NOT LLVM_PACKAGE_VERSION VERSION_EQUAL "14.0.0")
  message(FATAL_ERROR
    "Qualification requires LLVM 14.0.0; found ${LLVM_PACKAGE_VERSION}")
endif()

message(STATUS "LLVM_PACKAGE_VERSION=${LLVM_PACKAGE_VERSION}")
message(STATUS "LLVM_DIR=${LLVM_DIR}")
message(STATUS "Clang_DIR=${Clang_DIR}")

add_executable(svf_clang_cfg_v1 main.cpp)

target_include_directories(svf_clang_cfg_v1 PRIVATE
  ${LLVM_INCLUDE_DIRS}
  ${CLANG_INCLUDE_DIRS}
)
target_compile_definitions(svf_clang_cfg_v1 PRIVATE ${LLVM_DEFINITIONS})

if(TARGET clang-cpp)
  target_link_libraries(svf_clang_cfg_v1 PRIVATE clang-cpp)
  if(TARGET LLVM)
    target_link_libraries(svf_clang_cfg_v1 PRIVATE LLVM)
  endif()
else()
  target_link_libraries(svf_clang_cfg_v1 PRIVATE
    clangTooling
    clangFrontend
    clangSerialization
    clangAST
    clangAnalysis
    clangBasic
    clangLex
  )
  if(COMMAND llvm_map_components_to_libnames)
    llvm_map_components_to_libnames(SVF_LLVM_LIBS Support Option Core)
    target_link_libraries(svf_clang_cfg_v1 PRIVATE ${SVF_LLVM_LIBS})
  endif()
endif()

enable_testing()
