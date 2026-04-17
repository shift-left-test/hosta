add_host_library(cpputest STATIC
  SOURCES
    src/CppUTest/CommandLineArguments.cpp
    src/CppUTest/CommandLineTestRunner.cpp
    src/CppUTest/JUnitTestOutput.cpp
    src/CppUTest/MemoryLeakDetector.cpp
    src/CppUTest/MemoryLeakWarningPlugin.cpp
    src/CppUTest/SimpleMutex.cpp
    src/CppUTest/SimpleString.cpp
    src/CppUTest/SimpleStringInternalCache.cpp
    src/CppUTest/TeamCityTestOutput.cpp
    src/CppUTest/TestFailure.cpp
    src/CppUTest/TestFilter.cpp
    src/CppUTest/TestHarness_c.cpp
    src/CppUTest/TestMemoryAllocator.cpp
    src/CppUTest/TestOutput.cpp
    src/CppUTest/TestPlugin.cpp
    src/CppUTest/TestRegistry.cpp
    src/CppUTest/TestResult.cpp
    src/CppUTest/TestTestingFixture.cpp
    src/CppUTest/Utest.cpp
    src/Platforms/Gcc/UtestPlatform.cpp
  INCLUDE_DIRECTORIES PUBLIC ${CMAKE_CURRENT_LIST_DIR}
  COMPILE_OPTIONS PUBLIC -DCPPUTEST_MEM_LEAK_DETECTION_DISABLED
)
