def reduce_to_single_digit(number):
    while number > 9 and number not in [11, 22, 33]:  # Keep master numbers
        number = sum(int(digit) for digit in str(number))
    return number

def calculate_life_path_number(birthdate):
    digits = [int(char) for char in birthdate if char.isdigit()]
    return reduce_to_single_digit(sum(digits))

def calculate_birthday_number(birthdate):
    birth_day = int(birthdate.split('-')[2])
    return reduce_to_single_digit(birth_day)

def calculate_destiny_number(full_name):
    letter_to_number = {char: (ord(char) - 96) % 9 or 9 for char in 'abcdefghijklmnopqrstuvwxyz'}
    total = sum(letter_to_number[char] for char in full_name.lower() if char.isalpha())
    return reduce_to_single_digit(total)

def calculate_soul_urge_number(full_name):
    vowels = 'aeiou'
    letter_to_number = {char: (ord(char) - 96) % 9 or 9 for char in 'abcdefghijklmnopqrstuvwxyz'}
    total = sum(letter_to_number[char] for char in full_name.lower() if char in vowels)
    return reduce_to_single_digit(total)

def get_numerology_description(calculation, number):
    descriptions = {
        "Life Path Number": (
            "The Life Path Number represents your life's purpose and the lessons you are here to learn.",
            {
                1: "You are a natural leader, independent, and ambitious.",
                2: "You are cooperative, diplomatic, and seek harmony.",
                3: "You are creative, expressive, and bring joy to others.",
                4: "You are disciplined, practical, and value stability.",
                5: "You are adventurous, dynamic, and love freedom.",
                6: "You are nurturing, responsible, and family-oriented.",
                7: "You are introspective, analytical, and spiritual.",
                8: "You are ambitious, goal-oriented, and business-minded.",
                9: "You are compassionate, humanitarian, and idealistic."
            }
        ),
        "Birthday Number": (
            "The Birthday Number reveals a special talent or skill you bring into this life.",
            {
                1: "You are self-reliant and thrive in pioneering efforts.",
                2: "You excel in teamwork and fostering relationships.",
                3: "Your charm and wit inspire others.",
                4: "You have a gift for building and organizing.",
                5: "Your versatility and adaptability bring unique insights.",
                6: "You bring care and responsibility to those around you.",
                7: "Your curiosity drives deep exploration and understanding.",
                8: "You possess natural authority and business acumen.",
                9: "Your compassion and vision inspire change."
            }
        ),
        "Destiny Number": (
            "The Destiny Number reveals your ultimate goals and the direction you are destined to follow.",
            {
                1: "You are destined to be a trailblazer and innovator.",
                2: "You are meant to create balance and partnerships.",
                3: "Your destiny involves creativity and communication.",
                4: "You are here to establish order and systems.",
                5: "Your path involves exploration and transformation.",
                6: "You are destined to nurture and heal others.",
                7: "You seek truth, knowledge, and spiritual growth.",
                8: "You are destined for leadership and material success.",
                9: "Your path is about giving and making a global impact."
            }
        ),
        "Soul Urge Number": (
            "The Soul Urge Number reveals your inner desires and what truly motivates you.",
            {
                1: "You desire independence and personal achievement.",
                2: "You are driven by harmony and emotional connections.",
                3: "You long for creative expression and joy.",
                4: "You value security and hard work.",
                5: "You crave freedom and new experiences.",
                6: "You are motivated by love, care, and family.",
                7: "You seek inner peace and spiritual enlightenment.",
                8: "You are driven by power and financial stability.",
                9: "You desire to help others and make a difference."
            }
        )
    }

    if calculation in descriptions:
        short_description, number_meanings = descriptions[calculation]
        specific_meaning = number_meanings.get(number, "You have a unique path that combines diverse qualities.")
        return f"{short_description}\n{specific_meaning}"
    else:
        return "Description not available for this calculation."
