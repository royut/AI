from hazm import Normalizer, sent_tokenize, word_tokenize, POSTagger, DependencyParser, Stemmer

# Initialize NLP components
normalizer = Normalizer()
tagger = POSTagger(model='resources-0.5/postagger.model')
stemmer = Stemmer()


# Define a function to extract information from Persian text
def extract_info(text):
    age = None
    education = None
    experience = None

    # Normalize the text
    normalized_text = normalizer.normalize(text)

    # Tokenize and tag the text
    sentences = sent_tokenize(normalized_text)
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tagged_words = tagger.tag(tokens)

        # Extract information based on POS tagging
        for word, tag in tagged_words:
            if tag.startswith('N') and 'سن' in word:  # 'سن' means 'age' in Persian
                age = word
            elif tag.startswith('N') and 'تحصیلات' in word:  # 'تحصیلات' means 'education' in Persian
                education = word
            elif tag.startswith(
                    'N') and 'سابقه' in word and 'کاری' in word:  # 'سابقه کاری' means 'work experience' in Persian
                experience = word

    return age, education, experience


# Example text input in Persian
text = "علی 30 ساله با دکتری در رشته علوم کامپیوتر و 5 سال سابقه کار در توسعه نرم‌افزار است."

# Extract information from the Persian text
age, education, experience = extract_info(text)

# Print the extracted information
print("Age:", age)
print("Education:", education)
print("Experience:", experience)
