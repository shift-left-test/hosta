if(CMAKE_TESTING_ENABLED)
  do_host_compile(C unity_o
    SOURCE ${PROJECT_SOURCE_DIR}/unity/unity.c
    TARGET "unity"
    INCLUDE_DIRECTORIES ../unity
    COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS}
  )
endif()

add_host_test(relative_path_test
  SOURCES ../src/calc.c ../test/unity_test_main.c
  OBJECTS "${unity_o}"
  INCLUDE_DIRECTORIES ${CMAKE_CURRENT_LIST_DIR}/../src ../unity
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS}
  LINK_OPTIONS ${HOST_LINK_OPTIONS}
)
