import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont 
import datetime
from datetime import date
from variables import *

font_size = 15
myfont = ImageFont.truetype('arial.ttf', font_size)

#Format date to string, ir order to fit pandas syntax
def format_date(date):
    formated_date = str(date)

    if "-" in formated_date:
        formated_date = formated_date.split("-")
        formated_date = formated_date[2] + "/" + formated_date[1] + "/" + formated_date[0]
        formated_date = str(formated_date)
        formated_date = " " + formated_date

    else:
        formated_date = (f" {formated_date}")

    return formated_date

#Get the day of the week
def get_weekday(working_date):
    weekday = working_date.strip()
    weekday = weekday.split("/")
    
    year = int(weekday[2])

    #Remove the leading 0 to fit the datetime library parameters
    day = int(weekday[0])
    month = int(weekday[1])

    current_date = date(year,month,day)
    weekday = current_date.weekday() #It returns a number between 0 and 6. 0 = monday 6 = sunday
    return weekday

#Format yaware stat to fit the datetime library,
def formated_yaware(hours_minutes):
    if len(hours_minutes) > 1:
        hours_minutes = hours_minutes.split(".")

        working_hours = int(hours_minutes[0])
        working_minutes = int(hours_minutes[1])
        yaware = datetime.timedelta(hours=working_hours, minutes=working_minutes)

    else:
        working_hours = int(hours_minutes[0])
        yaware = datetime.timedelta(hours=working_hours)

    formated_yaware = yaware
    return formated_yaware

#Format the Yaware stat if it's longer than 24 hours
def yaware_over_24_hours(yaware_stat):
    yaware_seconds = yaware_stat.total_seconds()
    yaware_hours = int(yaware_seconds // 3600)  # Get total hours
    yaware_minutes = int((yaware_seconds % 3600) // 60)  # Get remaining minutes
    yaware_minutes = str(yaware_minutes)

    #Add a 0 just to make it look better, it goes from "7:4:00" to "7:40:00"
    if len(yaware_minutes) == 1:
        yaware_minutes += "0"

    yaware = (f"{yaware_hours}:{yaware_minutes}:00")
    return yaware


#Get the date of monday of a given date
def get_monday_date(date_):
    weekday = get_weekday(date_) 

    day_month_year = date_.split("/")
    day = int(day_month_year[0])
    monday_day = day - weekday

    month = int(day_month_year[1])
    year = int(day_month_year[2])

    monday_date = date(year, month, monday_day)

    return monday_date


#Check if the manager worked in a given date:
def worked_or_not(date_, manager):

    filtered_df = df[df['date'].isin([date_]) & (df['name'].isin([manager]))]
    stats = filtered_df[['calls']].values.tolist()
    stats = sum(stats,[]) #flatten the list
    return stats

#Calculate week targets
def week_targets(working_date, manager):
    #Get the date of monday from the week in the given date
    initial_date = get_monday_date(working_date)

    #Get the weekday
    weekday = get_weekday(working_date)  #It gives us a number between 0 and 6, where 0 = monday and 6 = sunday
    weekday += 1 #Add 1 to loop properly

    calls = [] #The length of this list will help us calculate the week targets
    for _ in range(weekday):
        #Check if the manager has worked in the current date
        formated_date = format_date(initial_date)
        worked = worked_or_not(formated_date, manager)
        
        if not worked:
            initial_date += datetime.timedelta(days=1)
            continue
        
        #Extract the data from the CSV file
        filtered_df = df[df['date'].isin([formated_date]) & (df['name'].isin([manager]))]
        stats = filtered_df[['calls']].values.tolist()
        stats = sum(stats,[]) #flatten the list
        
        calls_stats = stats[0]
        calls.append(calls_stats)

        initial_date += datetime.timedelta(days=1)

    if calls: #If the manager has any data for the given dates
        worked_days = len(calls) 

        #Calculate the week targets
        target_calls = str(daily_calls_target * worked_days) #
        target_uniques = str(daily_uniques_target * worked_days)
        target_minutes = str(daily_minutes_target * worked_days)

        target_yaware = daily_yaware_target * worked_days
        yaware_seconds = target_yaware.total_seconds()

        yaware_hours = int(yaware_seconds // 3600)  # Get total hours
        yaware_minutes = int(yaware_seconds % 3600) // 60  # Get remaining minutes
        
        #Add a 0 to single minutes to make it look better
        yaware_minutes = str(yaware_minutes)
        if len(yaware_minutes) == 1:
            yaware_minutes += "0"

        target_yaware = str(f"{yaware_hours}:{yaware_minutes}:00")

        targets = {
            "target calls" : target_calls,
            "target uniques" : target_uniques,
            "target minutes" : target_minutes,
            "target yaware" : target_yaware
        }

        return targets
  

#Get the total stats (the ones with blue background)
def total_result(working_date,manager): 
    #Get the day of monday from the week in the given date
    initial_date = get_monday_date(working_date)

    #Get the weekday
    weekday = get_weekday(working_date)  #It gives us a number between 0 and 6, where 0 = monday and 6 = sunday
    weekday += 1 #Add 1 to loop properly

    calls = 0
    unique_calls = 0
    minutes = 0
    yaware = datetime.timedelta(hours=0, minutes=0)

    for _ in range(weekday):
        #Check if the manager has worked in the current date
        formated_date = format_date(initial_date)
        worked = worked_or_not(formated_date, manager)
        if not worked:
            initial_date += datetime.timedelta(days=1)
            continue

        #Extract data for the given date and manager
        filtered_df = df[df['date'].isin([formated_date]) & (df['name'].isin([manager]))]
        stats = filtered_df[['calls','unique_calls',"minutes","yaware"]].values.tolist()
        stats = sum(stats,[]) #flatten the list
        
        calls += int(stats[0])
        unique_calls += int(stats[1])
        minutes += int(stats[2])
        
        #Format yaware stat and sum it up
        hours_minutes = str(stats[3])
        yaware += formated_yaware(hours_minutes)

        initial_date += datetime.timedelta(days=1) #Go to the next day
    

    if calls: #If the manager worked in the given dates
        calls = str(calls)
        unique_calls = str(unique_calls)
        minutes = str(minutes)

        #We need to format the Yaware stat if the hours are longer than 24 hours:
        if "day" or "days" in str(yaware):
            yaware = yaware_over_24_hours(yaware)
        else:
            yaware = str(yaware)

        weekly_stats = {
            "calls" : calls,
            "unique_calls" : unique_calls,
            "minutes" : minutes,
            "yaware" : yaware
        }

        return weekly_stats


#Get the color of the indicator circle
def indicator_circle(working_date, manager):
    #Check if the manager has worked in the given date
    formated_date = format_date(working_date)
    worked = worked_or_not(formated_date, manager)

    if worked:

        targets = week_targets(working_date, manager)
        week_results = total_result(working_date, manager)
        month_stats = month_results(working_date, manager)
        
        #Targets
        target_calls = targets["target calls"]
        target_uniques = targets["target uniques"]
        target_minutes = targets["target minutes"]

        target_yaware = targets["target yaware"]
        target_yaware = target_yaware.split(":")
        target_yaware = str(f"{target_yaware[0]}.{target_yaware[1]}")

        month_yaware_target = month_stats["month yaware target"]
        month_yaware_target = month_yaware_target.split(":")
        month_yaware_target = str(f"{month_yaware_target[0]}.{month_yaware_target[1]}")

        #Results
        calls = week_results["calls"]
        unique_calls = week_results["unique_calls"]
        minutes = week_results["minutes"]
        yaware = week_results["yaware"]
        yaware = yaware.split(":")
        yaware = str(f"{yaware[0]}.{yaware[1]}")

        month_yaware_result = month_stats["month yaware result"]
        month_yaware_result = month_yaware_result.split(":")
        month_yaware_result = str(f"{month_yaware_result[0]}.{month_yaware_result[1]}")
        

        if int(calls) >= int(target_calls):
            calls_circle = "green_circle"
        else:
            calls_circle = "red_circle"

        if int(unique_calls) >= int(target_uniques):
            uniques_circle = "green_circle"
        else:
            uniques_circle = "red_circle"

        if int(minutes) >= int(target_minutes):
            minutes_circle = "green_circle"
        else:
            minutes_circle = "red_circle"

        if float(yaware) >= float(target_yaware):
            yaware_circle = "green_circle"
        else:
            yaware_circle = "red_circle"

        if float(month_yaware_result) >= float(month_yaware_target):
            month_yaware_circle = "green_circle"
        else:
            month_yaware_circle = "red_circle"


        circle_indicators = {
            "calls circle" : calls_circle,
            "uniques circle" : uniques_circle,
            "minutes circle" : minutes_circle,
            "yaware circle" : yaware_circle,
            "month yaware circle" : month_yaware_circle
        }

        return circle_indicators



#Get the month results
def month_results(working_date, manager):
    day_month_year = working_date.split("/")

    day = int(day_month_year[0])
    month = int(day_month_year[1])
    year = int(day_month_year[2])

    initial_date = date(year, month, 1) #First day of the month 

    month_yaware_result = datetime.timedelta(hours=0, minutes=0)
    yaware_month = [] #This list will help us get how many days the manager has worked in the current month

    for _ in range(day):    
        #Check if the manager has worked in the current date
        formated_date = format_date(initial_date)
        worked = worked_or_not(formated_date, manager)
        if not worked:
            initial_date += datetime.timedelta(days=1)
            continue

        #Get how many days the manager has worked in the current week until the given date
        filtered_df = df[df['date'].isin([formated_date]) & (df['name'].isin([manager]))]
        stats = filtered_df[['yaware']].values.tolist()
        stats = sum(stats,[]) #flatten the list

        #Append to a list so we get how many days the manager worked
        yaware_stats = stats[0]
        yaware_month.append(yaware_stats)

        #Sum up the hours
        hours_minutes = str(stats[0])
        month_yaware_result += formated_yaware(hours_minutes)

        initial_date += datetime.timedelta(days=1)


    if yaware_month: #If the manager has any data for the given dates
        worked_days = len(yaware_month)

        month_yaware_target = worked_days * daily_yaware_target
        month_yaware_target_seconds = month_yaware_target.total_seconds()
        month_yaware_target_hours = int(month_yaware_target_seconds // 3600)  # Get total hours
        month_yaware_target_minutes = int(month_yaware_target_seconds % 3600) // 60  # Get remaining minutes
    
        #Add a 0 to single minutes to make it look better
        month_yaware_target_minutes = str(month_yaware_target_minutes)
        if len(month_yaware_target_minutes) == 1:
            month_yaware_target_minutes += "0"

        month_yaware_target = str(f"{month_yaware_target_hours}:{month_yaware_target_minutes}:00")
              
        #We need to format the yaware result if it's longer than 24 hours
        if "day" or "days" in str(month_yaware_result):
            month_yaware_result = yaware_over_24_hours(month_yaware_result)
            
        worked_days = str(worked_days)
        month_yaware_result = str(month_yaware_result)

        #create dictionary
        month_stats = {
            "month worked days" : worked_days,
            "month yaware target" : month_yaware_target,
            "month yaware result" : month_yaware_result
        }


        #return dictionary
        return(month_stats)


#Get the worked dates in the given week, we are gonna write them on the top of our template
def worked_dates(working_date, manager):
    initial_date = get_monday_date(working_date)

    #Get the weekday
    weekday = get_weekday(working_date)  #It gives us a number between 0 and 6, where 0 = monday and 6 = sunday
    weekday += 1 #Add 1 to loop properly

    worked_dates = []
    
    for i in range(weekday):
        
        formated_date = format_date(initial_date)
        worked = worked_or_not(formated_date, manager)

        if worked:
            #Extract data for the given date and manager
            filtered_df = df[df['date'].isin([formated_date]) & (df['name'].isin([manager]))]
            stats = filtered_df[["date"]].values.tolist()
            stats = sum(stats,[]) #flatten the list
        
            
            #If the manager worked in the given date, get the data
            worked_date = str(stats[0])
            worked_date = worked_date.strip()

            #Remove the year and keep the month and day
            worked_date = worked_date.split("/")
            worked_month = months[f"{worked_date[1]}"]

            worked_date = (f"{worked_date[0]}-{worked_month}")
            worked_weekday = weekdays[f"{i}"]

            worked_dates.append(f"{worked_date}/{worked_weekday}")

            initial_date += datetime.timedelta(days=1) #Go to the next day

        else:
            initial_date += datetime.timedelta(days=1) #Go to the next day

    return worked_dates
    

#Get the stats of each worked day in the given week
def daily_results(working_date, manager):
    
    daily_stats = {
        "calls": [],
        "unique_calls" : [],
        "minutes" : [],
        "yaware": []
    }

    initial_date = get_monday_date(working_date)
    #Get the weekday
    weekday = get_weekday(working_date)  #It gives us a number between 0 and 6, where 0 = monday and 6 = sunday
    weekday += 1 #Add 1 to loop properly
    
    for i in range(weekday):

        #Format the date
        formated_date = format_date(initial_date)
        worked = worked_or_not(formated_date, manager)
        if worked:
            #Extract data for the given date and manager
            filtered_df = df[df['date'].isin([formated_date]) & (df['name'].isin([manager]))]
            stats = filtered_df[["calls","unique_calls","minutes","yaware"]].values.tolist()
            stats = sum(stats,[]) #flatten the list

            calls = str(int(stats[0]))
            unique_calls = str(int(stats[1]))
            minutes = str(int(stats[2]))

            daily_stats["calls"].append(calls)
            daily_stats["unique_calls"].append(unique_calls)
            daily_stats["minutes"].append(minutes)

            #Format the yaware just to make it look better
            yaware = str(stats[3])
            
            hours_minutes = yaware.split(".")
            hours = str(hours_minutes[0])
            minutes = str(hours_minutes[1])

            if len(minutes) == 1:
                minutes += "0"
                yaware = (f"{hours}:{minutes}:00")
            
            else:
                yaware = (f"{hours}:{minutes}:00")

            daily_stats["yaware"].append(yaware)


            initial_date += datetime.timedelta(days=1)

        else:
            initial_date += datetime.timedelta(days=1) #Go to the next day

    return daily_stats

#Paste the date over the templat and save it as a image
def write_stats(working_date, manager):

    #If the manager didn't the work in the give date, it means he has finished the weeek
    #So we don't need to generate a follow up for him/her, because its follow-up has been generated in previous days

    formated_date = format_date(working_date)
    worked = worked_or_not(formated_date, manager)

    if worked:

        targets = week_targets(working_date, manager)
        week_results = total_result(working_date, manager)
        circle_indicators = indicator_circle(working_date, manager)
        month_stats = month_results(working_date, manager)
        week_worked_dates = worked_dates(working_date, manager)
        daily_stats = daily_results(working_date, manager)
        
        
        #Targets
        target_calls = targets["target calls"]
        target_uniques = targets["target uniques"]
        target_minutes = targets["target minutes"]
        target_yaware = targets["target yaware"]

        #Week results
        calls = week_results["calls"]
        unique_calls = week_results["unique_calls"]
        minutes = week_results["minutes"]
        yaware = week_results["yaware"]

        #Target circles indicators
        calls_circle = circle_indicators["calls circle"]
        uniques_circle = circle_indicators["uniques circle"]
        minutes_circle = circle_indicators["minutes circle"]
        yaware_circle = circle_indicators["yaware circle"]
        month_yaware_circle = circle_indicators["month yaware circle"]

        #Month results
        month_worked_days = month_stats["month worked days"]
        month_yaware_target = month_stats["month yaware target"]
        month_yaware_result = month_stats["month yaware result"]

    

        #Write over template
        template = Image.open(rf"{directory}\template.jpg")
        write = ImageDraw.Draw(template)

        #Write manager name
        name_width = write.textlength(manager, font=myfont)
        name_x_position = name_x + round((name_cell_width - name_width)/2)
        name_y_position = name_y + round((name_cell_height - font_size)/2)
        write.text((name_x_position, name_y_position), manager, font = myfont, fill=(0, 0, 0))

        #Write calls target
        target_calls_width = write.textlength(target_calls, font=myfont)
        target_calls_x_position = targets_x + round((target_cell_width - target_calls_width)/2)
        target_calls_y_position = targets_calls_y + round((target_cell_height - font_size)/2)
        write.text((target_calls_x_position, target_calls_y_position), target_calls, font = myfont, fill=(0, 0, 0))

        #Write uniques target
        target_uniques_width = write.textlength(target_uniques, font=myfont)
        target_uniques_x_position = targets_x + round((target_cell_width - target_uniques_width)/2)
        target_uniques_y_position = targets_uniques_y + round((target_cell_height - font_size)/2)
        write.text((target_uniques_x_position, target_uniques_y_position), target_uniques, font = myfont, fill=(0, 0, 0))

        #Write minutes target
        target_minutes_width = write.textlength(target_minutes, font=myfont)
        target_minutes_x_position = targets_x + round((target_cell_width - target_minutes_width)/2)
        target_minutes_y_position = targets_minutes_y + round((target_cell_height - font_size)/2)
        write.text((target_minutes_x_position, target_minutes_y_position), target_minutes, font = myfont, fill=(0, 0, 0))

        #Write yaware target
        target_yaware_width = write.textlength(target_yaware, font=myfont)
        target_yaware_x_position = targets_x + round((target_cell_width - target_yaware_width)/2)
        target_yaware_y_position = targets_yaware_y + round((target_cell_height - font_size)/2)
        write.text((target_yaware_x_position, target_yaware_y_position), target_yaware, font = myfont, fill=(0, 0, 0))
        
        #Write calls stats
        calls_width = write.textlength(calls, font=myfont)
        calls_x_position = summed_first_row_x + round((total_result_cell_width - calls_width)/2)
        calls_y_position = calls_y + round((total_result_cell_height - font_size)/2)
        write.text((calls_x_position, calls_y_position), calls, font = myfont, fill=(255, 255, 255))

        #Write unique calls stats
        unique_calls_width = write.textlength(unique_calls, font=myfont)
        unique_calls_x_position = summed_first_row_x + round((total_result_cell_width - unique_calls_width)/2)
        unique_calls_y_position = uniques_y + round((total_result_cell_height - font_size)/2)
        write.text((unique_calls_x_position, unique_calls_y_position), unique_calls, font = myfont, fill=(255, 255, 255))

        #Write minutes stats
        minutes_width = write.textlength(minutes, font=myfont)
        minutes_x_position = summed_first_row_x + round((total_result_cell_width - minutes_width)/2)
        minutes_y_position = minutes_y + round((total_result_cell_height - font_size)/2)
        write.text((minutes_x_position, minutes_y_position), minutes, font = myfont, fill=(255, 255, 255))

        #Write yaware stats
        yaware_width = write.textlength(yaware, font=myfont)
        yaware_x_position = summed_first_row_x + round((total_result_cell_width - yaware_width)/2)
        yaware_y_position = yaware_y + round((total_result_cell_height - font_size)/2)
        write.text((yaware_x_position, yaware_y_position), yaware, font = myfont, fill=(255, 255, 255))



        #Paste circle indicators
        calls_circle_image = Image.open(rf'{directory}\{calls_circle}.png')
        uniques_circle_image = Image.open(rf'{directory}\{uniques_circle}.png')
        minutes_circle_image = Image.open(rf'{directory}\{minutes_circle}.png')
        yaware_circle_image = Image.open(rf'{directory}\{yaware_circle}.png')
        month_yaware_circle_image = Image.open(rf'{directory}\{month_yaware_circle}.png')


        template.paste(calls_circle_image, (circles_x, calls_circle_y), mask = calls_circle_image)
        template.paste(uniques_circle_image, (circles_x, uniques_circle_y), mask = uniques_circle_image)
        template.paste(minutes_circle_image, (circles_x, minutes_circle_y), mask = minutes_circle_image)
        template.paste(yaware_circle_image, (circles_x, yaware_circle_y), mask = yaware_circle_image)
        template.paste(month_yaware_circle_image, (month_circle_x, month_circle_y), mask = month_yaware_circle_image)


        #Write month stats
        month_worked_days_width = write.textlength(month_worked_days, font=myfont)
        month_worked_days_x_position = worked_days_x + round((month_cell_width - month_worked_days_width)/2)
        month_worked_days_y_position = month_y + round((month_cell_height - font_size)/2)
        write.text((month_worked_days_x_position, month_worked_days_y_position), month_worked_days, font = myfont, fill=(0, 0, 0))

        month_yaware_target_width = write.textlength(month_yaware_target, font=myfont)
        month_yaware_target_x_position = month_yaware_target_x + round((month_cell_width - month_yaware_target_width)/2)
        month_yaware_target_y_position = month_y + round((month_cell_height - font_size)/2)
        write.text((month_yaware_target_x_position, month_yaware_target_y_position), month_yaware_target, font = myfont, fill=(0, 0, 0))

        month_yaware_result_width = write.textlength(month_yaware_result, font=myfont)
        month_yaware_result_x_position = month_yaware_result_x + round((month_cell_width - month_yaware_result_width)/2)
        month_yaware_result_y_position = month_y + round((month_cell_height - font_size)/2)
        write.text((month_yaware_result_x_position, month_yaware_result_y_position), month_yaware_result, font = myfont, fill=(0, 0, 0))


        #Write dates
        date_x, weekday_x = 488, 488
        for week_worked_date in week_worked_dates:
            week_worked_date = week_worked_date.split("/")

            worked_date = week_worked_date[0] #12-mar, 13-mar...
            worked_weekday = week_worked_date[1] #Mon, Tue, Wed... 

            worked_date_width = write.textlength(worked_date, font=myfont)
            worked_date_x_position = date_x + round((date_cell_width - worked_date_width)/2)
            worked_date_y_position = date_y + round((date_cell_height - font_size)/2)
            write.text((worked_date_x_position, worked_date_y_position), worked_date, font = myfont,fill=(0, 0, 0))

            worked_weekday_width = write.textlength(worked_weekday, font=myfont)
            worked_weekday_x_position = weekday_x + round((weekday_cell_width - worked_weekday_width)/2)
            worked_weekday_y_position = weekday_y + round((weekday_cell_height - font_size)/2)
            write.text((worked_weekday_x_position, worked_weekday_y_position), worked_weekday, font = myfont,fill=(0, 0, 0))

            date_x += 62
            weekday_x += 62
            

        #Write daily stats
        daily_x = 488
        daily_y = 115
        for i in range(len(daily_stats["calls"])):
        
            daily_calls = daily_stats["calls"][i]
            daily_uniques = daily_stats["unique_calls"][i]
            daily_minutes = daily_stats["minutes"][i]
            daily_yaware = daily_stats["yaware"][i]


            daily_calls_width = write.textlength(daily_calls, font=myfont)
            daily_calls_x_position = daily_x + round((daily_cell_width - daily_calls_width)/2)
            daily_calls_y_position = daily_y + round((daily_cell_height - font_size)/2)
            write.text((daily_calls_x_position, daily_calls_y_position), daily_calls, font = myfont,fill=(0, 0, 0))

            daily_y += 31
            
            daily_uniques_width = write.textlength(daily_uniques, font=myfont)
            daily_uniques_x_position = daily_x + round((daily_cell_width - daily_uniques_width)/2)
            daily_uniques_y_position = daily_y + round((daily_cell_height - font_size)/2)
            write.text((daily_uniques_x_position, daily_uniques_y_position), daily_uniques, font = myfont,fill=(0, 0, 0))

            daily_y += 31

            daily_minutes_width = write.textlength(daily_minutes, font=myfont)
            daily_minutes_x_position = daily_x + round((daily_cell_width - daily_minutes_width)/2)
            daily_minutes_y_position = daily_y + round((daily_cell_height - font_size)/2)
            write.text((daily_minutes_x_position, daily_minutes_y_position), daily_minutes, font = myfont,fill=(0, 0, 0))

            daily_y += 31

            daily_yaware_width = write.textlength(daily_yaware, font=myfont)
            daily_yaware_x_position = daily_x + round((daily_cell_width - daily_yaware_width)/2)
            daily_yaware_y_position = daily_y + round((daily_cell_height - font_size)/2)
            write.text((daily_yaware_x_position, daily_yaware_y_position), daily_yaware, font = myfont,fill=(0, 0, 0))

            daily_y = 115
            daily_x += 62

        template.save(rf"{directory}\follow ups\{date_}\{manager}.png")





working_date = ('11/03/2024')

#Create folder
date_ = working_date.replace("/","_")
directory = os.getcwd()
date_folder = os.path.isdir(rf'{directory}\follow ups\{date_}')
if date_folder == False:
    os.mkdir(rf'{directory}\follow ups\{date_}')
    

df = pd.read_csv(rf'{directory}\data.csv')
managers = df['name'].unique()

for manager in managers:
    write_stats(working_date, manager)
