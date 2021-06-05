### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }
    
def validate_data(year, intent_request):
    """
    Validates the data provided by the user.
    """

    # Validate that the the year is below 2020
    if year is not None:
        year = parse_int(
            year
        )
        if year > 2020:
            return build_validation_result(
                False,
                "year",
                "Sorry! The maximum year for this service is 2020. Please try again.",
            )

    # Validate the year is above 2016
    if year is not None:
        year = parse_int(
            year
        )  # Since parameters are strings it's important to cast values
        if year < 2016:
            return build_validation_result(
                False,
                "year",
                "Sorry! The minimum year is 2016. Please try again.",
            )
            
    # A True results is returned if year valid
    return build_validation_result(True, None, None)

### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }

def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response

### Intents Handlers ###
# get_best_show intent handler
def get_best_show(intent_request):
    """
    Performs dialog management and fulfillment for GetBestShow intent.
    """

    year = get_slots(intent_request)["year"]
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.

        ### VALIDATION CODE STARTS HERE ###
        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data(year, intent_request)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )
        ### VALIDATION CODE ENDS HERE ###

        # Fetch current session attibutes
        output_session_attributes = intent_request["sessionAttributes"]

        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the initial investment recommendation
    # sets the recommendations key and value pair
    best_show_year = {
    2020: "Middleditch & Schwartz",
    2019: "Our Planet",
    2018: "Sacred Games & The Haunting",
    2017: "The Vietnam War",
    2016: "Stranger Things",
    }
    # returns value for best_show & best_show_title  using risk_level as key
    best_show = [best_show_year[key] for key in best_show_year if key == year]
    best_show_title = best_show_year[int(year)]
    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": f"""Based on our data, it seems that in the year {year}, the tv show titled {best_show_title} received the highest IMDb score.
            """.format(
                year, best_show
            ),
        },
    )

# get_best_show intent handler
def get_top_five(intent_request):
    """
    Performs dialog management and fulfillment for GetBestShow intent.
    """

    year = get_slots(intent_request)["year"]
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.

        ### VALIDATION CODE STARTS HERE ###
        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data(year, intent_request)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )
        ### VALIDATION CODE ENDS HERE ###

        # Fetch current session attibutes
        output_session_attributes = intent_request["sessionAttributes"]

        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the initial investment recommendation
    # sets the recommendations key and value pair
    top_five_year = {
    2020: [
        ['Middleditch & Schwartz', 8.7],
        ['The Midnight Gospel', 8.4],
        ['Cheer', 8.2],
        ['The Trials of Gabriel Fernandez', 8.2],
        ['Unorthodox', 8.1]
    ],
    2019: [
        ['Our Planet', 9.3],
        ['When They See Us', 8.9],
        ['The Dark Crystal: Age of Resistance', 8.5],
        ['Love, Death & Robots', 8.5],
        ['After Life', 8.5]
    ],
    2018: [
        ['Sacred Games', 8.7],
        ['The Haunting', 8.7],
        ['Pose', 8.6],
        ['Hilda', 8.6],
        ['Queer Eye', 8.5]
    ],
    2017: [
        ['The Vietnam War', 9.1],
        ['Dark', 8.7],
        ['Anne with an E', 8.6],
        ['Mindhunter', 8.6],
        ['Time: The Kalief Browder Story', 8.5]
    ],
    2016: [
        ['Stranger Things', 8.8],
        ['The Crown', 8.7],
        ['Last Chance U', 8.5],
        ['American Crime Story', 8.4],
        ['Lucifer', 8.2]
    ],
    }
    # returns value for best_show & best_show_title  using risk_level as key
    top_five = [top_five_year[key] for key in top_five_year if key == int(year)]
    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": f"""Based on our data, it seems that in the year {year},
            the tv shows titled {top_five[0][0][0]}, {top_five[0][1][0]}, 
            {top_five[0][2][0]}, {top_five[0][3][0]}, and {top_five[0][4][0]} 
            were the top five series receiving the highest IMDb score.
            """.format(
                year, top_five
            ),
        },
    )

# get_best_show intent handler
def get_imdb_score(intent_request):
    """
    Performs dialog management and fulfillment for GetBestShow intent.
    """

    series_title = get_slots(intent_request)["SeriesTitle"]
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.

        ### VALIDATION CODE STARTS HERE ###
        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data(series_title, intent_request)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )
        ### VALIDATION CODE ENDS HERE ###

        # Fetch current session attibutes
        output_session_attributes = intent_request["sessionAttributes"]

        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the initial investment recommendation
    # sets the recommendations key and value pair
    imdb_list = {
        'Breaking Bad': 9.5,
        'Our Planet': 9.3,
        'Avatar: The Last Airbender': 9.2,
        'Sherlock': 9.1,
        'The Vietnam War': 9.1,
        'Fullmetal Alchemist: Brotherhood': 9.1,
        'The Twilight Zone': 9.0,
        'The Office': 8.9,
        'When They See Us': 8.9,
        'Peaky Blinders': 8.8,
        'Black Mirror': 8.8,
        'Stranger Things': 8.8,
        'One-Punch Man': 8.8,
        'Attack on Titan': 8.8,
        'Narcos': 8.8,
        "Monty Python's Flying Circus": 8.8,
        'The West Wing': 8.8,
        'Twin Peaks': 8.8,
        'Sacred Games': 8.7,
        'The Haunting': 8.7,
        'House of Cards': 8.7,
        'BoJack Horseman': 8.7,
        'Gomorrah': 8.7,
        'The Crown': 8.7,
        'Arrested Development': 8.7,
        'Dark': 8.7,
        'Better Call Saul': 8.7,
        'Middleditch & Schwartz': 8.7,
        'Making a Murderer': 8.6,
        'Rake': 8.6,
        'Star Trek: The Next Generation': 8.6,
        'Pose': 8.6,
        'Hilda': 8.6,
        'Anne with an E': 8.6,
        "Chef's Table": 8.6,
        'Parks and Recreation': 8.6,
        'Dexter': 8.6,
        'Mad Men': 8.6,
        "Marvel's Daredevil": 8.6,
        'Shameless': 8.6,
        'Mindhunter': 8.6,
        'Community': 8.5,
        'Mystery Science Theater 3000': 8.5,
        'Last Chance U': 8.5,
        'Mushi-Shi': 8.5,
        'Time: The Kalief Browder Story': 8.5,
        "Marvel's The Punisher": 8.5,
        'The Dark Crystal: Age of Resistance': 8.5,
        'Love, Death & Robots': 8.5,
        'The IT Crowd': 8.5,
        'Neon Genesis Evangelion': 8.5,
        'After Life': 8.5,
        'Queer Eye': 8.5,
        'Narcos: Mexico': 8.4,
        "Schitt's Creek": 8.4,
        'Heartland': 8.4,
        'Ash vs Evil Dead': 8.4,
        'The Last Kingdom': 8.4,
        'Rilakkuma and Kaoru': 8.4,
        'Supernatural': 8.4,
        'Top Boy': 8.4,
        'Outlander': 8.4,
        'Ozark': 8.4,
        'Kingdom': 8.4,
        'Broadchurch': 8.4,
        'Derry Girls': 8.4,
        'The Midnight Gospel': 8.4,
        'The Mechanism': 8.4,
        'The Dragon Prince': 8.4,
        'Halt and Catch Fire': 8.4,
        'Call the Midwife': 8.4,
        'Unbelievable': 8.4,
        'Money Heist': 8.4,
        'The Inbetweeners': 8.4,
        'American Crime Story': 8.4,
        'Abstract: The Art of Design': 8.4,
        'November 13: Attack on Paris': 8.3,
        'Star Trek': 8.3,
        'Fauda': 8.3,
        'Locked Up': 8.3,
        'Godless': 8.3,
        'Grace and Frankie': 8.3,
        'The Witcher': 8.3,
        'Sense8': 8.3,
        'Last Tango in Halifax': 8.3,
        'The Good Wife': 8.3,
        'Extras': 8.3,
        'Sex Education': 8.3,
        'Longmire': 8.3,
        'Rectify': 8.3,
        'Atypical': 8.3,
        'Five Came Back': 8.3,
        'Master of None': 8.3,
        'Hell on Wheels': 8.3,
        'The Originals': 8.2,
        'The Chef Show': 8.2,
        'Cheer': 8.2,
        'Queer as Folk': 8.2,
        'One Day at a Time': 8.2,
        'Jonathan Strange & Mr Norrell': 8.2,
        'American Vandal': 8.2,
        'HAPPY!': 8.2,
        'The Walking Dead': 8.2,
        'The Kominsky Method': 8.2,
        'Wild Wild Country': 8.2,
        'Bobby Kennedy for President': 8.2,
        'Penny Dreadful': 8.2,
        'Lucifer': 8.2,
        'Castlevania': 8.2,
        'The Trials of Gabriel Fernandez': 8.2,
        'Bates Motel': 8.2,
        'Club de Cuervos': 8.2,
        'The Good Place': 8.2,
        'Unorthodox': 8.1,
        'Dead to Me': 8.1,
        'Altered Carbon': 8.1,
        'The Keepers': 8.1,
        'Ripper Street': 8.1,
        'Bodyguard': 8.1,
        'Family Guy': 8.1,
        'Voltron: Legendary Defender': 8.1,
        'Documentary Now!': 8.1,
        'Manhunt': 8.1,
        'On My Block': 8.1,
        'Lovesick': 8.1,
        "TURN: Washington's Spies": 8.1,
        'Galavant': 8.1,
        "Don't F**k with Cats: Hunting an Internet Killer": 8.1,
        'The End of the F***ing World': 8.1,
        'Gilmore Girls': 8.1,
        'Dirty Money': 8.1,
        'Orange Is the New Black': 8.1,
        'The Tudors': 8.1,
        'The Toys That Made Us': 8.1,
        'Dogs': 8.1,
        'How to Get Away with Murder': 8.1,
        'Absolutely Fabulous': 8.1,
        'The Black Donnellys': 8.1,
        'Hyperdrive': 8.1,
        'Never Have I Ever': 8.0,
        'F is for Family': 8.0,
        'Mystery Science Theater 3000: The Return': 8.0,
        'Bloodline': 8.0,
        'The Blacklist': 8.0,
        'Marco Polo': 8.0,
        'Big Mouth': 8.0,
        "Marvel's Jessica Jones": 8.0,
        'GLOW': 8.0,
        'Lilyhammer': 8.0,
        'Into the Badlands': 8.0,
        "Inside Bill's Brain: Decoding Bill Gates": 8.0,
        'Flint Town': 8.0,
        'Derek': 8.0,
        'The Sinner': 8.0,
        'Cold Justice': 7.9,
        'Waco': 7.9,
        'The OA': 7.9,
        'Good Girls': 7.9,
        'iZombie': 7.9,
        'Weeds': 7.9,
        'Carole & Tuesday': 7.9,
        'The Fosters': 7.9,
        'Queen of the South': 7.9,
        'Russian Doll': 7.9,
        'Burn Notice': 7.9,
        "I'm Sorry": 7.9,
        'The Umbrella Academy': 7.9,
        'My Next Guest Needs No Introduction With David Letterman': 7.9,
        'The Staircase': 7.9,
        'Versailles': 7.9,
        'The Borgias': 7.9,
        'Carmen Sandiego': 7.9,
        'Star Trek: Deep Space Nine': 7.9,
        'The Spy': 7.9,
        'Episodes': 7.8,
        'Soul Eater': 7.8,
        'Diagnosis': 7.8,
        'Crazy Ex-Girlfriend': 7.8,
        'Portlandia': 7.8,
        '3Below: Tales of Arcadia': 7.8,
        'Imposters': 7.8,
        'American Crime': 7.8,
        'Ugly Delicious': 7.8,
        'Star Trek: Voyager': 7.8,
        '13 Reasons Why': 7.8,
        'A Series of Unfortunate Events': 7.8,
        'Maniac': 7.8,
        'YOU': 7.8,
        'Tiger King: Murder, Mayhem and Madness': 7.8,
        'Gotham': 7.8,
        'Santa Clarita Diet': 7.8,
        'Alias Grace': 7.8,
        'NCIS': 7.8,
        'Jane the Virgin': 7.8,
        'Chewing Gum': 7.7,
        'All American': 7.7,
        'Lost Girl': 7.7,
        'The Flash': 7.7,
        'New Girl': 7.7,
        'Once Upon a Time': 7.7,
        'Hollywood': 7.7,
        'Scandal': 7.7,
        'The Curious Creations of Christine McConnell': 7.7,
        'Messiah': 7.7,
        'The Vampire Diaries': 7.7,
        'Hart of Dixie': 7.7,
        'Nurse Jackie': 7.7,
        'Damnation': 7.7,
        'Limitless': 7.7,
        'Doctor Foster': 7.7,
        'Seven Seconds': 7.7,
        'The 100': 7.7,
        'Love': 7.7,
        'Dead Set': 7.7,
        'The Final Table': 7.7,
        'Spinning Out': 7.7,
        'Arrow': 7.6,
        'Kantaro: The Sweet Tooth Salaryman': 7.6,
        'Unbreakable Kimmy Schmidt': 7.6,
        'Chilling Adventures of Sabrina': 7.6,
        'The Devil Next Door': 7.6,
        'I Am Not Okay with This': 7.6,
        'Outer Banks': 7.6,
        'Bordertown': 7.6,
        'Evil Genius': 7.6,
        'Special': 7.6,
        "Grey's Anatomy": 7.6,
        'Rhythm + Flow': 7.6,
        'Elite': 7.6,
        'Madam Secretary': 7.6,
        'Dark Tourist': 7.6,
        'Surviving R. Kelly': 7.6,
        'Dark Matter': 7.5,
        'Mars': 7.5,
        'London Spy': 7.5,
        'Designated Survivor': 7.5,
        'Reign': 7.5,
        'The Assets': 7.5,
        'Frequency': 7.5,
        'The Circle': 7.5,
        'Haven': 7.5,
        'The Confession Tapes': 7.5,
        "Marvel's Agents of S.H.I.E.L.D.": 7.5,
        'Bad Blood': 7.5,
        'Everything Sucks!': 7.5,
        'Marianne': 7.5,
        'Star Trek: Enterprise': 7.5,
        'The Politician': 7.5,
        'Shooter': 7.5,
        "It's Bruno!": 7.5,
        'Pretty Little Liars': 7.4,
        'A.D. The Bible Continues': 7.4,
        'Self Made: Inspired by the Life of Madam C.J. Walker': 7.4,
        'Lady Dynamite': 7.4,
        'Young & Hungry': 7.4,
        'I Think You Should Leave with Tim Robinson': 7.4,
        'White Gold': 7.4,
        'Tuca & Bertie': 7.4,
        'The Innocent Man': 7.4,
        'The Night Shift': 7.4,
        'Black Earth Rising': 7.4,
        'The Confession Killer': 7.4,
        'W/ Bob & David': 7.4,
        'Glitch': 7.4,
        'Gossip Girl': 7.4,
        'Nailed It!': 7.4,
        'Wynonna Earp': 7.4,
        'Locke & Key': 7.4,
        '3%': 7.4,
        'Marcella': 7.4,
        'Colony': 7.4,
        'Secret City': 7.4,
        'Killer Inside: The Mind of Aaron Hernandez': 7.4,
        'Seis Manos': 7.3,
        'Selection Day': 7.3,
        'HAPPYish': 7.3,
        'Battle Creek': 7.3,
        'She-Ra and the Princesses of Power': 7.3,
        'Star-Crossed': 7.3,
        "Marvel's The Defenders": 7.3,
        'Gentefied': 7.3,
        "Marvel's Luke Cage": 7.3,
        'The Frankenstein Chronicles': 7.3,
        'Hawaii Five-0': 7.3,
        'Lost in Space': 7.3,
        'The Joel McHale Show with Joel McHale': 7.3,
        'Safe': 7.3,
        'The Stranger': 7.3,
        'The 4400': 7.3,
        'American Odyssey': 7.3,
        'Raising Dion': 7.2,
        'Disenchantment': 7.2,
        'Final Fantasy XIV: Dad of Light': 7.2,
        'Jericho': 7.2,
        'Flaked': 7.2,
        'Watership Down': 7.2,
        'Bonding': 7.2,
        'Into the Night': 7.2,
        'Chelsea Does': 7.2,
        'Living with Yourself': 7.2,
        'B: The Beginning': 7.2,
        'The Hollow': 7.2,
        'No Tomorrow': 7.2,
        'The Shannara Chronicles': 7.2,
        'Frontier': 7.2,
        'Containment': 7.2,
        'Trinkets': 7.1,
        'Hemlock Grove': 7.1,
        'Rebellion': 7.1,
        'Rotten': 7.1,
        'Aquarius': 7.1,
        'Dirty John': 7.1,
        'Rapture': 7.1,
        'GHOUL': 7.1,
        'Charmed': 7.1,
        'Mr. Iglesias': 7.1,
        'The Eddy': 7.0,
        'Paradise PD': 7.0,
        'Girlboss': 7.0,
        'Wanderlust': 7.0,
        'The Chalet': 7.0,
        'The Good Cop': 7.0,
        'Beauty and the Beast': 7.0,
        'The Windsors': 7.0,
        'Riverdale': 7.0,
        'The Society': 7.0,
        'Great News': 7.0,
        'Wormwood': 7.0,
        'The Order': 6.9,
        'How to Fix a Drug Scandal': 6.9,
        'Cooked With Cannabis': 6.9,
        'Gypsy': 6.9,
        'Easy': 6.9,
        'Sick Note': 6.8,
        'The Honeymoon Stand Up Special': 6.8,
        'Trigger Warning with Killer Mike': 6.8,
        'Huge in France': 6.8,
        'The Mysteries of Laura': 6.8,
        'Marseille': 6.8,
        'Helix': 6.8,
        '1983': 6.8,
        "DC's Legends of Tomorrow": 6.8,
        'Dracula': 6.8,
        'Knightfall': 6.8,
        'Fuller House': 6.8,
        'Baby': 6.8,
        'Zoo': 6.8,
        'Friends from College': 6.8,
        'Hot Girls Wanted: Turned On': 6.7,
        'Collateral': 6.7,
        'Breakfast, Lunch & Dinner': 6.7,
        'Glee': 6.7,
        "She's Gotta Have It": 6.7,
        'Disjointed': 6.7,
        'Quantico': 6.7,
        'Daybreak': 6.7,
        'Private Practice': 6.6,
        'Traitors': 6.6,
        'Powder': 6.6,
        'Tidying Up with Marie Kondo': 6.6,
        'Insatiable': 6.6,
        'Taken': 6.6,
        'Freud': 6.6,
        'The Messengers': 6.5,
        "Marvel's Iron Fist": 6.5,
        'The New Legends of Monkey': 6.5,
        'Requiem': 6.5,
        'Chambers': 6.5,
        'Life Sentence': 6.5,
        'Typewriter': 6.5,
        'Black Summer': 6.4,
        'The Family': 6.4,
        'Power Rangers': 6.4,
        'Cleverman': 6.4,
        'Wu Assassins': 6.4,
        'Dating Around': 6.4,
        'Behind Enemy Lines': 6.4,
        'Family Reunion': 6.3,
        "Cooper Barrett's Guide to Surviving Life": 6.3,
        'The Rain': 6.3,
        'Kiss Me First': 6.3,
        'Supergirl': 6.3,
        'Dear White People': 6.2,
        'White Lines': 6.2,
        'Black Lightning': 6.1,
        'Roswell, New Mexico': 6.1,
        'October Faction': 6.1,
        'Chelsea': 6.1,
        'Haters Back Off': 6.0,
        'Baby Daddy': 6.0,
        'Champions': 6.0,
        'Between': 6.0,
        'Love is Blind': 6.0,
        'Nightflyers': 5.9,
        'Valor': 5.9,
        'The Letter for the King': 5.9,
        'Westside': 5.8,
        'Queen Sono': 5.8,
        'Neo Yokio': 5.8,
        'No Good Nick': 5.8,
        'The In-Laws': 5.7,
        'The Comedy Lineup': 5.7,
        'Pacific Heat': 5.7,
        'The Mr. Peabody & Sherman Show': 5.6,
        'The Mist': 5.4,
        'Sid the Science Kid': 5.4,
        'The Break with Michelle Wolf': 5.2,
        'Fast & Furious Spy Racers': 5.2,
        'Prank Encounters': 5.0,
        'Another Life': 4.9,
        'Brews Brothers': 4.8,
        'The I-Land': 4.5,
        'All About the Washingtons': 4.2,
        'Troy: Fall of a City': 3.8,
        'Bill Nye Saves the World': 3.6,
        'The Goop Lab': 2.3
    }
    # returns value for best_show & best_show_title  using risk_level as key
    imdb_score = [value for key, value in imdb_list.items() if series_title == key]
    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": f"""Based on our data, it seems that in the tv show titled {series_title},
            has an IMDb score of {imdb_score} .
            """.format(
                series_title, imdb_score
            ),
        },
    )
    
### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "GetBestShow":
        return get_best_show(intent_request)
    
    if intent_name == "GetTopFive":
        return get_top_five(intent_request)
        
    if intent_name == "GetIMDbScore":
        return get_imdb_score(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")
    
### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)

