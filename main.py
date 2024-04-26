from hazm import Normalizer, sent_tokenize, word_tokenize, POSTagger

# Initialize NLP components
normalizer = Normalizer()
tagger = POSTagger(model='pos_tagger.model')


def extract_age(text):
    age = None

    normalized_text = normalizer.normalize(text)

    sentences = sent_tokenize(normalized_text)
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tagged_words = tagger.tag(tokens)

        for word, tag in tagged_words:
            if tag.startswith('NUM') and word.isdigit():
                if 10 <= int(word) <= 100:  # Assume valid age range
                    age = int(word)
                    break

    return age


def extract_education_field(text):
    education_level = None
    field_of_study = None

    normalized_text = normalizer.normalize(text)

    sentences = sent_tokenize(normalized_text)
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tagged_words = tagger.tag(tokens)

        for word, _ in tagged_words:
            if word in ["دبستان", "راهنمایی", "دبیرستان", "لیسانس", "کارشناسی", "فوق لیسانس", "کارشناسی ارشد", "دکتری"]:
                education_level = word
                break

        found_education_level = False
        for i, (word, tag) in enumerate(tagged_words):
            if found_education_level and ('N' in tag or tag == 'CON') and 'رشته' in word:
                if word == "و" and tag == "CON" and i != len(tagged_words) - 1:
                    break
                field_of_study_tokens = []
                for j in range(i, len(tagged_words)):
                    field_word, field_tag = tagged_words[j]
                    if field_word == "و" and field_tag == "CCONJ" and j != i:
                        break
                    field_of_study_tokens.append(field_word)
                field_of_study = " ".join(field_of_study_tokens)
                break
            elif word == education_level:
                found_education_level = True

    return education_level, field_of_study


def extract_work_history(text):
    work_history = None

    normalized_text = normalizer.normalize(text)

    sentences = sent_tokenize(normalized_text)
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tagged_words = tagger.tag(tokens)

        last_word = ''
        last_tag = ''
        for i, (word, tag) in enumerate(tagged_words):
            if ('N' in tag or tag == 'V') and ('تجربه' in last_word or 'سابقه' in last_word) and 'کار' in word:
                if i < len(tagged_words) - 1:
                    work_history_tokens = []
                    for j in range(i + 1, len(tagged_words)):
                        work_word, work_tag = tagged_words[j]
                        if work_tag.startswith('N') or work_tag.startswith('V') or work_tag.startswith('AJ'):
                            work_history_tokens.append(work_word)
                        elif work_word == "در":
                            continue
                        else:
                            break
                    work_history = " ".join(work_history_tokens)
                    break
            last_word = word
            last_tag = tag

    return work_history


# Example text input in Persian
# text = "علی 30 ساله با دکتری در رشته علوم کامپیوتر و 5 سال سابقه کار در توسعه نرم‌افزار است."
# text = "علی مدرک کارشناسی رشته علوم کامپیوتر و تجربه کار در حوزه نرم‌افزار دارد."
text = input('Enter a sentence: ')

# Extract info
age = extract_age(text)
education_level, field_of_study = extract_education_field(text)
work_history = extract_work_history(text)
purpose = None

# Check and prompt for missing data
while not age:
    input_str = input("Age not found in the text. Enter age:")
    if input_str.isdigit() and 10 <= int(input_str) <= 100:
        age = int(input_str)
    else:
        print("Invalid age. Please enter a valid age between 10 and 100.")

if not education_level:
    input_str = input("Education Level not found in the text. Enter your education level:")
    education_level, field_of_study = extract_education_field(input_str)

if not work_history:
    input_str = input("Work History not found in the text. Enter your work history:")
    work_history = extract_work_history(input_str)

if not purpose:
    input_str = input("Purpose not found in the text. Are reaching out for general inquiries or do you have specific pathway in mind?")
    purpose = input_str

# Print extracted information
print("Age:", age)
print("Education Level:", education_level)
print("Field of Study:", field_of_study)
print("Work History:", work_history)
print("Purpose:", purpose)
