import datetime
#Daily targets
daily_calls_target = 130 
daily_uniques_target = 110
daily_minutes_target = 60
daily_yaware_target = datetime.timedelta(hours=7, minutes=30)

#Manager name position
name_x = 20
name_y = 85
name_cell_width = 189
name_cell_height = 20


#Dates position
date_x = 488
date_y = 60
date_cell_width = 60
date_cell_height = 26

weekday_x = 488
weekday_y = 84
weekday_cell_width = 60
weekday_cell_height = 20
dates_cells_gap =2


#Targets position
targets_x = 292
target_cell_width = 81
target_cell_height = 27

targets_calls_y = 115
targets_uniques_y = 146
targets_minutes_y = 178
targets_yaware_y = 209


#Summed stats position (the ones with blue background)
total_result_cell_height = 27
total_result_cell_width = 81
total_result_cells_gap = 4
summed_first_row_x = 372

calls_y = 115
uniques_y = 146
minutes_y = 178
yaware_y = 209


#Daily stats position (the ones with white background)
daily_x = 488
daily_y = 115

daily_cell_width = 59
daily_cell_height = 27


#Color indicators position (the circles)
circles_x = 460

calls_circle_y = 120
uniques_circle_y = 150
minutes_circle_y = 182
yaware_circle_y = 215

#Month stats position
month_y = 285

worked_days_x = 208
month_yaware_target_x = 292
month_yaware_result_x = 372

month_cell_width = 82
month_cell_height = 27

month_circle_x = 460
month_circle_y = 290


#Months & weekdays variables
months = {
    "01" : "jan",
    "02" : "fev",
    "03" : "mar",
    "04" : "abr",
    "05" : "mai",
    "06" : "jun",
    "07" : "jul",
    "08" : "ago",
    "09" : "set",
    "10" : "out",
    "11" : "nov",
    "12" : "dez"
}

weekdays = {
    "0" : "seg",
    "1" : "ter",
    "2" : "qua",
    "3" : "qui",
    "4" : "sex",
    "5" : "sab",
    "6" : "dom"
}

