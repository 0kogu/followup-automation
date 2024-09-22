# Follow up automation

This follow up generator extracts the account managers stats in the week of the inserted date, paste it over a template and store in a folder for that given date.

Here's a demonstration of it: https://youtu.be/rnLV8VfgmQo

The used data was created with [another project of mine](https://github.com/0kogu/Account-managers-analysis)


## Features

- **Smart Storing**: If the user inserts a date which only some managers work. saturday for example, a folder for that date will be created and it will store follow ups only for those who worked from tuesday to saturday, because the follow ups for manager who from monday to friday has been fully filled the day before and it was stored in the folder of the previous date.
- **Color indicator**: It displays a color indicator for each stat, green if the goal was achieved, red if it was not.
- **Dates**: It displays the worked dates in the week.

  ![image](https://github.com/user-attachments/assets/3b8c0e5b-ce36-4d88-83fe-f369081ac854)


## Technologies

- **Python**
- **Pandas** to read CSV files and extract data
- **Datetime** for hours and dates manipulation
- **Pillow** for image editing


## Future enhancements

- Scheduling the script running in the cloud
- Use Telegram API to automate the distribuiton of follow ups


## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/0kogu/followup-automation.git
   cd followup-automation
