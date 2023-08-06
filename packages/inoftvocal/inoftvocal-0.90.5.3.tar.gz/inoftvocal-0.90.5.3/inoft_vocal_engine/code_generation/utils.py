def prettify_speech_text(text: str) -> str:
    new_text = str()
    last_char_index_to_have_been_added_new_line = 0
    for i_char, char in enumerate(text):
        if i_char > last_char_index_to_have_been_added_new_line + 115:
            if char == " ":
                new_text += (char + "/n")
                last_char_index_to_have_been_added_new_line = i_char
            else:
                new_text += char
        else:
            new_text += char
    return new_text

def to_class_name(text: str) -> str:
    import inflect

    new_text = ""
    current_digit_sequence = ""
    number_last_char_index = None
    for i, char in enumerate(text):
        # We add a - when adding numbers, so that they will be considered as separate
        # element in the class name, and that their first letter will be capitalized.
        if str(char).isdigit():
            current_digit_sequence += char
            if i+1 == len(text):
                new_text += ("-" + inflect.engine().number_to_words(current_digit_sequence))
                current_digit_sequence = ""
        else:
            if current_digit_sequence != "":
                new_text += ("-" + inflect.engine().number_to_words(current_digit_sequence))
                current_digit_sequence = ""
                number_last_char_index = i

            if number_last_char_index is not None and number_last_char_index == i:
                char = char.capitalize()
            new_text += char

    formatted_output_text = ""
    half_text_elements = new_text.replace(",", "").split("-")
    final_text_elements = list()
    for text_element in half_text_elements:
        for splitted_element in text_element.split(" "):
            final_text_elements.append(splitted_element)

    for text_element in final_text_elements:
        formatted_output_text += ((text_element[0].capitalize() if len(text_element) > 0 else "") +
                                  (text_element[1:] if len(text_element) > 1 else ""))

    return formatted_output_text
