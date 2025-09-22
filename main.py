#GarudaTalon V1.0 Copyright Mallard-Dash 2025
#Main-file

def mainmenu():
    while True:
        print("***Main-Menu***\n",
        "1.---START-MONITORING---\n",
        "2.---ACTIVE-MONITORING---\n",
        "3.---SET-ALARM---\n",
        "4.---ACTIVE-ALARMS\n",
        "5.---START-SURVEY-MODE---\n",
        "6.---EXIT-PROGRAM---\n")
        mm_choice = (input("Enter a number between 1-6: "))

        if mm_choice == 1:
                print("START-MONITORING")
                import start_monitoring
        elif mm_choice == 2:
                print("ACTIVE-MONITORING")
                import active_monitoring
        elif mm_choice == 3:
                print("SET-ALARM")
                import set_alarm
        elif mm_choice == 4:
                print("ACTIVE-ALARMS")
                import active_alarms
        elif mm_choice == 5:
                print("START-SURVEY-MODE")
                import survey_mode
        elif mm_choice == 6:
                print("Exiting...bye!")
                break
        else:
               print("Invalid choice! Enter a number between 1-6.")
        
mainmenu()