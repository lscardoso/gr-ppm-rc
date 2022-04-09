find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_PPM_ANALOG_RC gnuradio-PPM_Analog_RC)

FIND_PATH(
    GR_PPM_ANALOG_RC_INCLUDE_DIRS
    NAMES gnuradio/PPM_Analog_RC/api.h
    HINTS $ENV{PPM_ANALOG_RC_DIR}/include
        ${PC_PPM_ANALOG_RC_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_PPM_ANALOG_RC_LIBRARIES
    NAMES gnuradio-PPM_Analog_RC
    HINTS $ENV{PPM_ANALOG_RC_DIR}/lib
        ${PC_PPM_ANALOG_RC_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-PPM_Analog_RCTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_PPM_ANALOG_RC DEFAULT_MSG GR_PPM_ANALOG_RC_LIBRARIES GR_PPM_ANALOG_RC_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_PPM_ANALOG_RC_LIBRARIES GR_PPM_ANALOG_RC_INCLUDE_DIRS)
