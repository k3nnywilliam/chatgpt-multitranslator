from chatgpt_utils.translate_utils import Translator
import logging

if __name__ == "__main__":
    questions_ls = ["Do you know Mike Tyson", "What is Mike Tyson's age?", "Where does he live now?"]
    language_option = ["German", "Dutch", "French", "Danish", "Indonesian"]
    language_option = ', '.join(language_option)
    translator = Translator()
    answers_ls =[]
    logging.info(f"Submitting {len(questions_ls)} questions...")
    logging.info(f"Translating to: {language_option}")
    logging.info("Awaiting responses...")
    answers_ls = translator.split_chat_processing(questions_ls, language_option)
    parsed_responses = translator.parse_responses(answers_ls)
    logging.info(f"reply: {parsed_responses}")