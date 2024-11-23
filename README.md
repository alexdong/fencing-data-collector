The website will be used to capture details of every touch in a fencing bout.

It'll be used for two main purposes:
1. on a tablet by a referee during a fencing bout. So the UI should be simple
   and easy to use. The buttons should be big enough to be clicked with a
   finger. 
2. by a coach to export csv data for further analysis.

The website contains the main pages:
1. list: which lists all the bouts order by time. there is an option to filter
   by club. Export button to export the data to csv.
2. bout details page: which allows a ref to enter detailed bout data.

The bout details page has three parts:
1. top part collects the context. For each bout, it only needs to be entered
   once.  details like club, fencers, etc should be remembered for the next
   bout.
2. middle part shows a start and stop button. When stop is clicked, we show the
   bottom form. When start is clicked, show the seconds elapsed since the start
   button was clicked. 
3. bottom part is a MacDonald menu ordering system where the ref can quickly
   enter the details for each touch.

Philosophy:
- This is a hobby project so please keep everything bare minimum. 
- Most of the time, I only have a couple of hours per week to work on this. 
- Make sure everything should be logged, tested and monitored. 

Stack:
- Tech: flask, peewee + sqlite, jinja2 and htmx 
- Dev: aider, ruff, pytest
- Hosting: AWS Beanstalk free-tier + Cloudwatch
