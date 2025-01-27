idf_component_register(SRCS "llamacli.c" "espwifi.c"
                    PRIV_REQUIRES nvs_flash esp_wifi esp_http_client
                    INCLUDE_DIRS ".")

target_compile_options(${COMPONENT_LIB} PRIVATE -Wno-error=format)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wno-error=format")