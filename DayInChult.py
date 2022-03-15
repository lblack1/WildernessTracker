import random as r
import os
import time
from colorama import Fore

r.seed(time.time())
trackables = {}
encounter_rolls = [None, None, None, None]
Morning_Thresh = 15
Afternoon_Thresh = 15
Evening_Thresh = 15
Night_Thresh = 17
weather = {
	1: "Clear day, gentle breeze",
	2: "Light rain, no wind",
	3: "Hazy overcast, patches of fog",
	4: "Clear sky, strong wind",
	5: "Dark overcast, moderate rain",
	6: "High heat, slow wind",
	7: "Rapidly shifting between heavy rain and high heat",
	8: "Intense rain all day"
}

def print_trackables():
	print("Current Trackables")
	for k,v in trackables.items():
		print("\t- {}: {}".format(k, v))

def print_encounters():
	print("Morning: {}".format(encounter_rolls[0]))
	print("Afternoon: {}".format(encounter_rolls[1]))
	print("Evening: {}".format(encounter_rolls[2]))
	print("Night: {}".format(encounter_rolls[3]))

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')
	return

def opt_loop():
	while True:
		print()
		print(Fore.GREEN + "Today is day {}".format(str(trackables["days_since_start"])) + Fore.WHITE)
		print("Select an option")
		print("\t1) Advance day")
		print("\t2) Modify existing trackable")
		print("\t3) Add trackable")
		print("\t4) Print trackables")
		print("\t5) Print today's encounters")
		print("\tq) Quit and save trackables")
		print("\tx) Exit without saving")
		opt = input(" >>> ")
		if opt not in ["1","2","3","4","5","q","x"]:
			print("Invalid option, try again")
		
		if opt == "1":
			for k,v in trackables.items():
				if k != "days_since_start":
					trackables[k] = v - 1
				else:
					trackables[k] = v + 1
			
			# Weather
			weather_today = r.randint(1,8)
			tropical_storm = 1
			if weather_today == 8:
				tropical_storm = r.randint(1,4)

			print()
			print("Today's weather: " + weather[weather_today])
			if tropical_storm == 4:
				print(Fore.RED + "*** TROPICAL STORM ALERT ***" + Fore.WHITE)

			# 4d20s for encounters at morning, afternoon, evening, and overnight
			encounters = [ r.randint(1,20) for x in range(4) ]
			print()
			print(Fore.GREEN + "--- Morning Encounter ---" + Fore.WHITE)
			if encounters[0] > Morning_Thresh:
				encounter_rolls[0] = r.randint(1,100)
				print(Fore.RED + "ENCOUNTER! Roll is {}".format(encounter_rolls[0]) + Fore.WHITE)
			else:
				encounter_rolls[0] = None
				print("No Encounter")

			print()
			print(Fore.GREEN + "--- Afternoon Encounter ---" + Fore.WHITE)
			if encounters[1] > Afternoon_Thresh:
				encounter_rolls[1] = r.randint(1,100)
				print(Fore.RED + "ENCOUNTER! Roll is {}".format(encounter_rolls[1]) + Fore.WHITE)
			else:
				encounter_rolls[1] = None
				print("No Encounter")

			print()
			print(Fore.GREEN + "--- Evening Encounter ---" + Fore.WHITE)
			if encounters[2] > Evening_Thresh:
				encounter_rolls[2] = r.randint(1,100)
				print(Fore.RED + "ENCOUNTER! Roll is {}".format(encounter_rolls[2]) + Fore.WHITE)
			else:
				encounter_rolls[2] = None
				print("No Encounter")
			
			print()
			print(Fore.GREEN + "--- Night Encounter ---" + Fore.WHITE)
			if encounters[3] > Night_Thresh:
				encounter_rolls[3] = r.randint(1,100)
				print(Fore.RED + "ENCOUNTER! Roll is {}".format(encounter_rolls[3]) + Fore.WHITE)
			else:
				encounter_rolls[3] = None
				print("No Encounter")
			
		elif opt == "2":
			print()
			print("Select trackable:")
			print_trackables()
			print()
			selected = input(" >>> ")
			try:
				trackables[selected]
			except IndexError:
				print(Fore.YELLOW + "Trackable not found; check spelling" + Fore.WHITE)
				continue
			new_val = int(input("New trackable value: "))
			trackables[selected] = new_val
		
		elif opt == "3":
			print()
			new_track = input("New trackable name: ")
			try:
				new_t_val = int(input("Trackable value: "))
			except ValueError:
				print("That's not a number numnuts")
			trackables[new_track] = new_t_val

		elif opt == "4":
			print()
			print_trackables()
		
		elif opt == "5":
			print()
			print_encounters()

		elif opt == "q":
			with open("ChultTracker.txt", "w") as f:
				for k,v in trackables.items():
					f.write("{}:{}\n".format(k,v))
			
			with open("EncounterRolls.txt", "w") as f:
				for x in encounter_rolls:
					f.write(str(x) + "\n")

			break
			
		elif opt == "x":
			break




if __name__ == "__main__":
	try:
		with open("ChultTracker.txt", "r") as f:
			for line in f.readlines():
				key, val = line.strip().split(":")
				trackables[key] = int(val)
		
		if os.path.exists("EncounterRolls.txt"):
			with open("EncounterRolls.txt", "r") as f:
				encounter_rolls = [int(x) if x != "None\n" else None for x in f.readlines()]
		
		clear()
		print("---- Chult Tracker v1 ----")
		print()
		print_trackables()
		
		opt_loop()

		print("Okay bye")

	except KeyboardInterrupt:
		with open("ChultTracker.txt", "w") as f:
			for k,v in trackables.items():
				f.write("{}:{}\n".format(k,v))
		exit()