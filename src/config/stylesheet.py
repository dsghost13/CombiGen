from config.constants import COLORS as C

add_button_ss =     f"""
                    QPushButton {{
                        color: white;
                        background-color: {C["DARK_GRAY"]};
                        border-color: {C["WHITE"]};
                        border-style: solid;
                        border-width: 1px;
                    }}

                    QPushButton:hover {{
                        background-color: {C["DARK_GREEN"]};
                    }}
                    """

del_button_ss =     f"""
                    QPushButton {{
                        color: white;
                        background-color: {C["DARK_GRAY"]};
                        border-color: {C["WHITE"]};
                        border-radius: 10px;
                        border-style: solid;
                        border-width: 1px;
                    }}

                    QPushButton:hover {{
                        background-color: {C["DARK_RED"]};
                    }}
                    """

dropdown_ss =       f"""
                    QComboBox {{
                        background-color: {C["DARK_GRAY"]};
                        border: 1px solid {C["WHITE"]};
                        border-radius: 0px;
                    }}

                    QComboBox QAbstractItemView {{
                        background-color: {C["DARKER_GRAY"]};          
                        selection-background-color: {C["DARK_GRAY"]}; 
                    }}
                    """

gen_button_ss =     f"""
                    QPushButton {{
                        color: white;
                        background-color: {C["LIGHT_BLUE"]};
                        border-color: {C["WHITE"]};
                        border-radius: 10px;
                        border-style: solid;
                        border-width: 1px;
                        font-size: 15px;
                    }}

                    QPushButton:hover {{
                        background-color: {C["MEDIUM_BLUE"]};
                    }}

                    QPushButton:pressed {{
                        background-color: {C["DARK_BLUE"]};
                        border-color: {C["WHITE"]};
                        border-radius: 10px;
                        border-style: solid;
                        border-width: 1px;
                    }}
                    """

pareto_axis_ss =    f"""
                    QPushButton {{ 
                        border-color: {C["WHITE"]};
                        border-radius: 0px;
                        border-style: solid;
                        border-width: 1px;
                    }}

                    QPushButton:hover {{ 
                        background-color: {C["DARK_GRAY"]}; 
                    }}
                    """

pareto_cell_ss =    f"""
                    QPushButton {{ 
                        background-color: {C["DARK_RED"]}; 
                        border-color: {C["WHITE"]};
                        border-radius: 0px;
                        border-style: solid;
                        border-width: 1px;
                    }}

                    QPushButton:hover:!checked {{
                        background-color: {C["LIGHT_RED"]};
                    }}

                    QPushButton:checked {{
                        background-color: {C["DARK_GREEN"]};
                    }}

                    QPushButton:hover:checked {{
                        background-color: {C["LIGHT_GREEN"]};
                    }}
                    """

scroll_area_ss =    f"""
                    QScrollArea {{
                        background: transparent;
                        border: none;
                    }}

                    QScrollArea QWidget {{
                        background: transparent;
                    }}
                    """

section_ss =        f"""
                    background-color: {C["BLACK"]};
                    border-radius: 10px;
                    """

terminal_ss =       """
                    background-color: black;
                    color: white;
                    """

text_entry_ss =     f"""
                    border-color: {C["WHITE"]};
                    border-style: solid;
                    border-width: 1px;
                    """
