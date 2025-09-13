if(CONFIG_ZMK_DISPLAY)
    zephyr_library_include_directories(${CMAKE_SOURCE_DIR}/include)
    
    if(CONFIG_NICE_VIEW_WIDGET_STATUS)
        target_sources(app PRIVATE
            widgets/util.c
            widgets/bolt.c
            custom_status_screen.c
        )

        if(NOT CONFIG_ZMK_SPLIT OR CONFIG_ZMK_SPLIT_ROLE_CENTRAL)
            target_sources(app PRIVATE
                widgets/status.c
                widgets/bongocatart.c
                widgets/modifiers_sym.c
            )
        else()
            target_sources(app PRIVATE
                widgets/peripheral_status.c
                widgets/art.c
            )
        endif()
    endif()

    target_include_directories(app PRIVATE include)
endif()
