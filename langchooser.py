import json
from googletrans import Translator

class LangChooser():
    """Choose and stores a language setting in a configuration file."""
    DEFAULTS = {
        "default_prompt": "Keep current language settings? 1=Yes 2=No:",
        "from_prompt": "From what language? (e.g.: en-US) Leave empty to show all languages:",
        "to_prompt": "To what language? (e.g.: en-US) Leave empty to show all languages:",
        "from_lang": "uk-UA",
        "to_lang": "en-US",
        "invalid_prompt": "Invalid language. Use ISO 639-1 format. e.g.: en-US"
    }

    with open("languages.json", 'r') as data:
        LANGUAGES = json.load(data)

    def __init__(self, config_file = "langchooser.json"):
        self.from_lang = ""
        self.to_lang = ""
        self.default_prompt = ""
        self.config_file = config_file
        
        # Open config file if exists
        try:
            with open(config_file, 'r') as data:
                config = json.load(data)
                self.default_prompt = config['default_prompt']
                self.from_prompt = config['from_prompt']
                self.to_prompt = config['to_prompt']
                self.from_lang = config['from_lang']
                self.to_lang = config['to_lang']
                self.invalid_prompt = config['invalid_prompt']
        except:
            self.default_prompt = LangChooser.DEFAULTS['default_prompt']
            self.from_prompt = LangChooser.DEFAULTS['from_prompt']
            self.to_prompt = LangChooser.DEFAULTS['to_prompt']
            self.from_lang = LangChooser.DEFAULTS['from_lang']
            self.to_lang = LangChooser.DEFAULTS['to_lang']
            self.invalid_prompt = LangChooser.DEFAULTS['invalid_prompt']

    def prompt(self):
        """Prompt the user for language choice."""

        original_from = self.from_lang
        original_to = self.to_lang

        # Set defaults
        if not self.default_prompt:
            self.default_prompt = LangChooser.DEFAULTS['default_prompt']
            self.from_prompt = LangChooser.DEFAULTS['from_prompt']
            self.to_prompt = LangChooser.DEFAULTS['to_prompt']
            self.from_lang = LangChooser.DEFAULTS['from_lang']
            self.to_lang = LangChooser.DEFAULTS['to_lang']
            self.invalid_prompt = LangChooser.DEFAULTS['invalid_prompt']

        while True:  # Keep settings loop
            print(self.from_lang + " -> " + self.to_lang)
            default_choice = input(self.default_prompt + " ").strip()

            if default_choice.isdigit():
                if default_choice == "1":
                    return True
                elif default_choice == "2":
                    break  # Break out of loop and continue to language chooser
        
        while True:  # Choose from loop
            choice = input(self.from_prompt + " ").strip()

            if not choice:
                self.print_langs()
                continue

            if choice in LangChooser.LANGUAGES.keys():
                self.from_lang = choice
                break  # Break out and continue to next chooser
            else:
                print(self.invalid_prompt)
                continue
        
        while True:  # Choose to loop
            choice = input(self.to_prompt + " ").strip()

            if not choice:
                self.print_langs()
                continue

            if choice in LangChooser.LANGUAGES.keys():
                self.to_lang = choice
                break  # Break out and end prompting
            else:
                print(self.invalid_prompt)
                continue

        # Get proper translation and save settings
        if self.to_lang == LangChooser.DEFAULTS['to_lang']:
            self.default_prompt = LangChooser.DEFAULTS['default_prompt']
            self.from_prompt = LangChooser.DEFAULTS['from_prompt']
            self.to_prompt = LangChooser.DEFAULTS['to_prompt']
            self.invalid_prompt = LangChooser.DEFAULTS['invalid_prompt']
        elif self.to_lang != original_to:
            translator = Translator()
            from_short = self.from_lang.split('-')[0]
            to_short = self.to_lang.split('-')[0]
            self.default_prompt = translator.translate(LangChooser.DEFAULTS['default_prompt'], src=from_short, dest=to_short).text
            self.from_prompt = translator.translate(LangChooser.DEFAULTS['from_prompt'], src=from_short, dest=to_short).text
            self.to_prompt = translator.translate(LangChooser.DEFAULTS['to_prompt'], src=from_short, dest=to_short).text
            self.invalid_prompt = translator.translate(LangChooser.DEFAULTS['invalid_prompt'], src=from_short, dest=to_short).text

        try:
            with open(self.config_file, 'w') as config:
                json.dump(self.__dict__, config, indent=4)
        except:
            with open(self.config_file, 'w') as config:
                json.dump({}, config)
    
    def print_langs(self):
        for lang, props in LangChooser.LANGUAGES.items():
            print(lang, json.dumps(props))
        

if __name__ == "__main__":
    langchooser = LangChooser()
    langchooser.prompt()