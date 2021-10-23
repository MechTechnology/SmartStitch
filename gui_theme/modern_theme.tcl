source gui_theme/light.tcl

option add *tearOff 0

ttk::style theme use "modern-light"

array set colors {
    -fg             "#000000"
    -bg             "#ffffff"
    -disabledfg     "#737373"
    -disabledbg     "#ffffff"
    -selectfg       "#ffffff"
    -selectbg       "#737373"
}

ttk::style configure . \
    -background $colors(-bg) \
    -foreground $colors(-fg) \
    -troughcolor $colors(-bg) \
    -focuscolor $colors(-selectbg) \
    -selectbackground $colors(-selectbg) \
    -selectforeground $colors(-selectfg) \
    -insertcolor $colors(-fg) \
    -insertwidth 1 \
    -fieldbackground $colors(-selectbg) \
    -font {"Segoe Ui" 10} \
    -borderwidth 1 \
    -relief flat

tk_setPalette background [ttk::style lookup . -background] \
    foreground [ttk::style lookup . -foreground] \
    highlightColor [ttk::style lookup . -focuscolor] \
    selectBackground [ttk::style lookup . -selectbackground] \
    selectForeground [ttk::style lookup . -selectforeground] \
    activeBackground [ttk::style lookup . -selectbackground] \
    activeForeground [ttk::style lookup . -selectforeground]

ttk::style map . -foreground [list disabled $colors(-disabledfg)]

option add *font [ttk::style lookup . -font]
option add *Menu.selectcolor $colors(-fg)