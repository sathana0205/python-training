print("***BMI calculator***")

weight=float(input("enter the weight(kg): "))
height_cm=float(input("enter the height(m): "))
height=height_cm/100
bmi=weight/(height**2)
print(f"BMI:{bmi}")

if bmi>18.5:
    print("you are underweight")
elif bmi<38.5:
    print("you are normalweight")
elif bmi<=55.5:
    print("you are overweight")
else:
    print("you are obese")


