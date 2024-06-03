import re
import zipfile


class TextAnalyzer:
    """Class for text analyzing"""

    Text = ''  # Static attribute

    def __init__(self, text):
        self.text = text
        TextAnalyzer.Text = text

    def count_sentences(self):
        """Method for counting sentences"""
        sentences = re.findall(r'[.!?]\s*', self.text)
        return len(sentences)

    def count_sentence_types(self):
        """Method for counting sentence types"""
        narr_count = len(re.findall(r'[.]\s*', self.text))
        interrog_count = len(re.findall(r'[?]\s*', self.text))
        imper_count = len(re.findall(r'[!]\s*', self.text))
        return narr_count, interrog_count, imper_count

    def average_sentence_length(self):
        """Method for finding average sentence length"""
        sentences = re.split(r'[.!?][\n\s]*', self.text)
        total_char = 0
        total_sen = 0
        for sentence in sentences:
            words = re.findall(r'[a-zA-Z]+\b', sentence)
            total_char += sum(len(word) for word in words)
            if words:
                total_sen += 1

        if total_sen == 0:
            return 0
        average = total_char / total_sen
        return average

    def average_word_length(self):
        """Method for finding average word length"""
        words = re.findall(r'[a-zA-Z]+\b', self.text)
        return sum(len(word) for word in words) / len(words)

    def count_smiles(self):
        """Method for counting smiles"""
        smileys = re.findall(r'[;:]-*[\(\[\)\]]+', self.text)
        return len(smileys)

    def __str__(self):  # Special method
        return self.text


class DatesMixin:
    """Mixin for finding lowercase words"""

    def extract_dates(self):
        """Extracting a list of dates from text (format 05/12/2007)"""
        dates = re.findall(r'(?:0[1-9]|[12][0-9]|3[01])[-](?:0[1-9]|1[012])[-](?:19|20)\d\d', self.text)
        return dates


class MyTextAnalyzer(TextAnalyzer, DatesMixin):
    """Class for text analyzing according to variant"""

    def __init__(self, text):
        super().__init__(text)

    def extract_words_with_vowel_consonant_pattern(self, target_string):
        """Retrieving a list of words from a given string whose last letter is a vowel and the penultimate letter is a consonant"""
        words = re.findall(r'\b[a-zA-Z]*[aeiouy][b-df-hj-np-tv-z]\b', target_string)
        return words

    def extract_words_from_specific_line(self, line_number):
        """Method for extract words from specific line"""
        lines = self.text.split('\n')

        if 1 <= line_number <= len(lines):
            target_string = lines[line_number - 1]  # Выбор указанной строки
            words = self.extract_words_with_vowel_consonant_pattern(target_string)
            return words

        return []

    def count_lowercase_letters(self):
        """Count the number of lowercase letters in the text"""
        lowercase_letters = re.findall(r'[a-z]', self.text)
        return len(lowercase_letters)

    def find_last_word_with_letter_i(self):
        """Finding the last word containing the letter 'i' and its number"""
        words = re.findall(r'(?:0[1-9]|[12][0-9]|3[01])[-](?:0[1-9]|1[012])[-](?:19|20)\d\d|\w+\b', self.text)
        last_word = ''
        last_word_index = -1
        for i, word in enumerate(words):
            if 'i' in word:
                last_word = word
                last_word_index = i
        return f"Word - {last_word}, on pos - {last_word_index}"

    def remove_words_starting_with_i_from_specific_line(self, line_number):
        """Removing words starting with 'i' from a specified string"""
        lines = self.text.split('\n')

        if 1 <= line_number <= len(lines):
            target_string = lines[line_number - 1]

            words = re.findall(r'(?:0[1-9]|[12][0-9]|3[01])[-](?:0[1-9]|1[012])[-](?:19|20)\d\d|\b\w+\b', target_string)
            filtered_words = [word for word in words if not word.startswith('i')]
            filtered_text = ' '.join(filtered_words)
            return filtered_text

        return ""

    @property  # Getter for text
    def text(self):
        return self._text

    @text.setter  # Setter for text
    def text(self, value):
        self._text = value


class Zipper:
    """Class for zipping and getting info from zip"""

    def __init__(self, filename):
        self.filename = filename

    def zip_results(self, results):
        """Method for zipping results"""
        try:
            with zipfile.ZipFile(self.filename, 'w') as zip_file:
                for key, value in results.items():
                    zip_file.writestr(key + '.txt', '\n'.join(map(str, value)))
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_zip_info(self):
        """Method for getting info from zip"""
        try:
            with zipfile.ZipFile(self.filename, 'r') as zip_file:
                for info in zip_file.infolist():
                    file_content = zip_file.read(info.filename).decode('utf-8')
                    print(f"Filename: {info.filename}")
                    print(f"File size: {info.file_size}")
                    print(f"Compressed size: {info.compress_size}")
                    print(f"Compress type: {info.compress_type}")
                    print(f"Content:\n{file_content}\n")
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")


def main():
    """Main function for task2"""
    while True:
        input_filename = "C:/Users/Lenovo/PycharmProjects/Lab4IGI/input.txt"

        output_filename = "C:/Users/Lenovo/PycharmProjects/Lab4IGI/results.zip"

        try:
            with open(input_filename, 'r') as file:
                text = file.read()
                print(text)
        except FileNotFoundError:
            print(f"Error: File '{input_filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        analyzer = MyTextAnalyzer(text)

        dates = analyzer.extract_dates()
        words_with_pattern = analyzer.extract_words_from_specific_line(2)
        word_with_i = analyzer.find_last_word_with_letter_i()
        text_without_i = analyzer.remove_words_starting_with_i_from_specific_line(2)
        count_sentences = analyzer.count_sentences()
        narr_count, interrog_count, imper_count = analyzer.count_sentence_types()
        average_sen_len = analyzer.average_sentence_length()
        average_word_len = analyzer.average_word_length()
        smiles_count = analyzer.count_smiles()

        # turn into dictionary
        results = {
            "dates": dates,
            "words_with_patter": [words_with_pattern],
            "word_with_i": [word_with_i],
            "text_without_i": [text_without_i],
            "count_sentences": [count_sentences],
            "narr_count": [narr_count],
            "interrog_count": [interrog_count],
            "imper_count": [imper_count],
            "average_sen_len": [average_sen_len],
            "average_word_len": [average_word_len],
            "smiles_count ": [smiles_count],
        }
        zipper = Zipper(output_filename)

        zipper.zip_results(results)

        zipper.get_zip_info()
        repeat = input("Do you want to execute program one more time? Type 'yes' if so: ")
        if repeat != 'yes':
            break


if __name__ == "__main__":
    main()