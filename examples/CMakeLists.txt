find_package(Qt5 REQUIRED COMPONENTS Core)

add_executable(example main.cpp)
target_link_libraries(example PRIVATE Qt5::Core)
target_compile_features(example PRIVATE cxx_std_20)
